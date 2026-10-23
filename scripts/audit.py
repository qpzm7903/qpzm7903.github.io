#!/usr/bin/env python3
"""站点结构审计：输出可复现的 JSON 指标。

设计原则
--------
1. 只依赖 Python 标准库（无第三方包），保证任何机器可复现。
2. 所有"内容侧"指标来自 content/ 的 front matter 原文，"渲染侧"指标来自 hugo 构建产物。
3. 指标定义写在 docs/audit-baseline.md，脚本与文档必须一致，改口径要同时改两处。
4. 输出稳定：键排序、无时间戳噪声（generated_at 除外），可安全 diff 两个 commit 的结果。

用法
----
    python3 scripts/audit.py --root <repo> --public <hugo 构建目录>
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

# ---------------------------------------------------------------- 常量/口径

THIN_MD_BYTES = 1500  # 正文 Markdown 小于此值视为"薄内容"
THIN_TAG_POSTS = 3  # 标签页承载文章数少于此值视为"薄标签页"
SAMPLE_POST_LIMIT = 1  # JSON-LD / og:image 抽检篇数（按最新一篇）
JSONLD_DESC_FULLTEXT = 300  # JSON-LD description 超过此长度视为"正文注入"

FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)
FENCE_RE = re.compile(r"```.*?```", re.S)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)[^)]*\)")
HTML_LINK_RE = re.compile(r"""<a\s[^>]*href=["']([^"']+)["']""", re.I)


# ---------------------------------------------------------------- front matter

def read_front_matter(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    return m.group(1) if m else ""


def body_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    return text[m.end():] if m else text


def fm_scalar(fm: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", fm, re.M)
    if not m:
        return None
    value = m.group(1).strip()
    if value in ("", "null", "~"):
        return None
    return value.strip("'\"")


def fm_list(fm: str, key: str) -> list[str]:
    """解析 inline 列表 + block 列表两种写法。"""
    out: list[str] = []
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", fm, re.M)
    if not m:
        return out
    inline = m.group(1).strip()
    if inline.startswith("["):
        return [x.strip().strip("'\"") for x in inline.strip("[]").split(",") if x.strip()]
    if inline:  # 单值当列表
        return [inline.strip("'\"")]
    # block 列表
    for line in fm[m.end():].splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("- "):
            out.append(s[2:].strip().strip("'\""))
        elif not line.startswith((" ", "\t")):
            break  # 回到顶格 = 下一个字段
    return [x for x in out if x]


# ---------------------------------------------------------------- hugo 侧信息

def hugo_list(root: Path) -> list[dict]:
    """hugo list all 输出 CSV，取 path/permalink/kind/section/draft/lastmod。"""
    out = subprocess.run(
        ["hugo", "list", "all"], cwd=root, capture_output=True, text=True, check=True
    ).stdout
    return list(csv.DictReader(out.splitlines()))


def permalink_to_public(public: Path, permalink: str) -> Path:
    rel = unquote(urlparse(permalink).path).lstrip("/")
    return public / rel / "index.html" if rel else public / "index.html"


def norm_path(url: str, base_url: str) -> str | None:
    """把内链规范化为 /posts/xxx 形式；非站内返回 None。"""
    url = url.split("#")[0].split("?")[0].strip()
    if not url:
        return None
    if url.startswith(("mailto:", "javascript:", "data:")):
        return None
    base_host = urlparse(base_url).netloc
    if url.startswith(("http://", "https://")):
        p = urlparse(url)
        if p.netloc != base_host:
            return None
        path = p.path
    elif url.startswith("/"):
        path = url
    else:
        return None
    path = unquote(path).rstrip("/")
    return path or "/"


def is_external(url: str, base_url: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False
    return urlparse(url).netloc != urlparse(base_url).netloc


# ---------------------------------------------------------------- 主流程

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--public", required=True)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--generated-at", default=None)
    ap.add_argument("--hugo-warnings", type=int, default=0)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    public = Path(args.public).resolve()

    hugo_cfg = (root / "hugo.yaml").read_text(encoding="utf-8")
    m = re.search(r'^baseURL:\s*"?([^"\n]+)"?', hugo_cfg, re.M)
    base_url = args.base_url or (m.group(1).strip() if m else "https://qpzm7903.github.io/")

    post_files = sorted((root / "content" / "posts").glob("*.md"))
    concept_files = sorted((root / "content" / "concepts").glob("*.md"))

    # ---- front matter 扫描
    cats: dict[str, int] = {}
    tags: dict[str, int] = {}
    series: dict[str, int] = {}
    coverage = {"description": 0, "lastmod": 0, "slug": 0, "aliases": 0, "series": 0,
                "draft_false": 0, "draft_missing": 0}
    md_sizes: list[int] = []
    dates: list[str] = []
    thin_posts: list[str] = []
    post_meta: dict[str, dict] = {}

    for p in post_files:
        fm = read_front_matter(p)
        rel = str(p.relative_to(root))
        size = p.stat().st_size
        md_sizes.append(size)
        if size < THIN_MD_BYTES:
            thin_posts.append(rel)

        for c in fm_list(fm, "categories"):
            cats[c] = cats.get(c, 0) + 1
        for t in fm_list(fm, "tags"):
            tags[t] = tags.get(t, 0) + 1
        for s in fm_list(fm, "series"):
            series[s] = series.get(s, 0) + 1

        for key in ("description", "lastmod", "slug", "aliases", "series"):
            if fm_scalar(fm, key) or fm_list(fm, key):
                coverage[key] += 1
        draft = fm_scalar(fm, "draft")
        if draft is None:
            coverage["draft_missing"] += 1
        elif draft.lower() == "false":
            coverage["draft_false"] += 1

        date = fm_scalar(fm, "date")
        if date:
            dates.append(date[:10])

        # ---- 链接统计（正文，剔除代码块）
        body = FENCE_RE.sub("", body_of(p))
        internal, external = [], []
        for target in MD_LINK_RE.findall(body) + HTML_LINK_RE.findall(body):
            if is_external(target, base_url):
                external.append(target)
            else:
                np = norm_path(target, base_url)
                if np:
                    internal.append(np)
        post_meta[rel] = {"internal": internal, "external": external, "size": size,
                          "date": (fm_scalar(fm, "date") or "")[:10]}

    concept_links: dict[str, list[str]] = {}
    for p in concept_files:
        rel = str(p.relative_to(root))
        body = FENCE_RE.sub("", body_of(p))
        internal = []
        for target in MD_LINK_RE.findall(body) + HTML_LINK_RE.findall(body):
            np = norm_path(target, base_url)
            if np:
                internal.append(np)
        concept_links[rel] = internal

    # ---- 渲染侧：permalink → 产物
    rows = hugo_list(root)
    page_rows = [r for r in rows if r.get("kind") == "page" and r.get("path", "").startswith("content/")]
    url_by_content = {r["path"]: unquote(urlparse(r["permalink"]).path).rstrip("/") for r in page_rows}

    html_sizes: list[int] = []
    md_by_url: dict[str, int] = {}
    for p in post_files:
        rel = str(p.relative_to(root))
        url = url_by_content.get(rel)
        if not url:
            continue
        out = public / url.lstrip("/") / "index.html"
        if out.exists():
            html_sizes.append(out.stat().st_size)
            md_by_url[url] = p.stat().st_size

    # ---- 入链图 / 孤儿页
    inbound: dict[str, int] = {u: 0 for u in url_by_content.values()}
    for rel, meta in post_meta.items():
        src = url_by_content.get(rel)
        for tgt in meta["internal"]:
            if tgt in inbound and tgt != src:
                inbound[tgt] += 1
    for rel, links in concept_links.items():
        for tgt in links:
            if tgt in inbound:
                inbound[tgt] += 1

    post_urls = [url_by_content[str(p.relative_to(root))] for p in post_files
                 if str(p.relative_to(root)) in url_by_content]
    orphans = sorted(u for u in post_urls if inbound.get(u, 0) == 0)

    all_internal = [n for meta in post_meta.values() for n in meta["internal"]]
    all_external = [n for meta in post_meta.values() for n in meta["external"]]

    # ---- sitemap / RSS / robots
    sitemap_path = public / "sitemap.xml"
    sitemap = {"total": 0, "posts": 0, "tags": 0, "categories": 0, "series": 0, "other": 0}
    if sitemap_path.exists():
        tree = ET.parse(sitemap_path)
        locs = [el.text or "" for el in tree.iter() if el.tag.endswith("loc")]
        sitemap["total"] = len(locs)
        for loc in locs:
            path = unquote(urlparse(loc).path)
            if path.startswith("/posts/"):
                sitemap["posts"] += 1
            elif path.startswith("/tags/"):
                sitemap["tags"] += 1
            elif path.startswith("/categories/"):
                sitemap["categories"] += 1
            elif path.startswith("/series/"):
                sitemap["series"] += 1
            else:
                sitemap["other"] += 1

    rss_path = public / "index.xml"
    rss = {"index_bytes": rss_path.stat().st_size if rss_path.exists() else 0,
           "index_items": 0,
           "per_page_rss_files": len(list((public / "posts").glob("*/index.xml")))}
    if rss_path.exists():
        rss["index_items"] = rss_path.read_text(encoding="utf-8", errors="replace").count("<item>")

    robots_path = public / "robots.txt"
    robots = {"exists": robots_path.exists(),
              "declares_sitemap": False}
    if robots["exists"]:
        robots["declares_sitemap"] = "sitemap" in robots_path.read_text(
            encoding="utf-8", errors="replace").lower()

    # ---- HTML 元数据抽检
    home_html = (public / "index.html").read_text(encoding="utf-8", errors="replace") if (public / "index.html").exists() else ""
    lang_m = re.search(r"<html[^>]*\blang=[\"']([^\"']+)", home_html, re.I)
    og_image = "<meta property=\"og:image\"" in home_html or "property=og:image" in home_html

    sample_url = post_urls[-1] if post_urls else None
    sample_html = ""
    if sample_url:
        sp = public / sample_url.lstrip("/") / "index.html"
        if sp.exists():
            sample_html = sp.read_text(encoding="utf-8", errors="replace")
    jsonld_blocks = re.findall(r'<script type=[\'\"]application/ld\+json[\'\"]>(.*?)</script>',
                               sample_html, re.S)
    jsonld_types = []
    jsonld_issues = []
    for raw in jsonld_blocks:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            jsonld_issues.append("invalid_json")
            continue
        for item in (data if isinstance(data, list) else [data]):
            t = item.get("@type")
            jsonld_types.append(t)
            if t == "BlogPosting":
                if item.get("inLanguage") not in ("zh-cn", "zh-CN", "zh"):
                    jsonld_issues.append(f"inLanguage={item.get('inLanguage')!r}")
                author = item.get("author")
                if isinstance(author, dict) and isinstance(author.get("name"), dict):
                    jsonld_issues.append("author_name_nested")
                if len(str(item.get("description", ""))) > JSONLD_DESC_FULLTEXT:
                    jsonld_issues.append("description_contains_fulltext")
                if "articleBody" in item and len(str(item["articleBody"])) > JSONLD_DESC_FULLTEXT:
                    jsonld_issues.append("articleBody_duplicates_body")

    # ---- 菜单覆盖度
    menu = []
    for name, url in re.findall(r"- identifier:\s*\"[^\"]*\"\s*\n\s*name:\s*\"([^\"]+)\"\s*\n\s*url:\s*\"([^\"]+)\"", hugo_cfg):
        menu.append({"name": name, "url": url})
    coverage_menu = {"entries": len(menu), "category_entries": 0,
                     "posts_covered_by_categories": 0, "ratio": None}
    cat_total = sum(cats.values())
    covered_terms = set()
    for entry in menu:
        mm = re.match(r"/categories/([^/]+)/?$", unquote(entry["url"]))
        if mm:
            coverage_menu["category_entries"] += 1
            covered_terms.add(mm.group(1))
    if cat_total:
        covered = sum(v for k, v in cats.items() if k in covered_terms)
        coverage_menu["posts_covered_by_categories"] = covered
        coverage_menu["ratio"] = round(covered / cat_total, 4)

    # ---- 汇总
    result = {
        "generated_at": args.generated_at,
        "build": {"hugo_warnings": args.hugo_warnings},
        "root": str(root),
        "posts": len(post_files),
        "concept_pages": len(concept_files),
        "content": {
            "thin_posts": {"threshold_bytes": THIN_MD_BYTES, "count": len(thin_posts),
                           "files": thin_posts[:10]},
            "md_bytes": {"median": int(statistics.median(md_sizes)) if md_sizes else 0,
                         "p90": int(statistics.quantiles(md_sizes, n=10)[8]) if len(md_sizes) > 9 else 0,
                         "max": max(md_sizes) if md_sizes else 0},
            "date": {
                "first": min(dates) if dates else None,
                "last": max(dates) if dates else None,
                # 最近两篇的间隔，用于发现"产线断流"（比 posts_last_30d 更抗单篇噪声）
                "last_two_gap_days": _gap_days(dates),
                "posts_last_30d": sum(1 for d in dates if d >= _days_ago(30, dates)),
            },
        },
        "taxonomy": {
            "categories": _term_stats(cats, THIN_TAG_POSTS),
            "tags": _term_stats(tags, THIN_TAG_POSTS),
            "series": _term_stats(series, THIN_TAG_POSTS),
            "menu": menu,
            "menu_coverage": coverage_menu,
        },
        "links": {
            "internal_total": len(all_internal),
            "external_total": len(all_external),
            "internal_per_post_median": round(statistics.median(
                [len(v["internal"]) for v in post_meta.values()]), 2) if post_meta else 0,
            "posts_without_internal_link": sum(1 for v in post_meta.values() if not v["internal"]),
            "orphan_posts": {"count": len(orphans), "ratio": round(len(orphans) / len(post_urls), 4) if post_urls else None,
                             "samples": orphans[:10]},
        },
        "metadata": {
            "coverage": coverage,
            "html_lang": lang_m.group(1) if lang_m else None,
            "og_image_on_home": og_image,
            "jsonld": {"sample_url": sample_url, "types": jsonld_types, "issues": sorted(set(jsonld_issues))},
        },
        "output": {
            "html_bytes_posts": {
                "median": int(statistics.median(html_sizes)) if html_sizes else 0,
                "p90": int(statistics.quantiles(html_sizes, n=10)[8]) if len(html_sizes) > 9 else 0,
                "max": max(html_sizes) if html_sizes else 0,
                "count": len(html_sizes),
            },
            "md_to_html_ratio_median": round(statistics.median(
                [h / md_by_url[u] for u, h in _pairs(url_by_content, post_files, public, root) if md_by_url.get(u)]), 2)
                if html_sizes else None,
            "home_html_bytes": len(home_html.encode()),
            "archives_html_bytes": _size(public / "archives" / "index.html"),
            "sitemap": sitemap,
            "rss": rss,
            "robots": robots,
        },
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


def _days_ago(n: int, dates: list[str]) -> str:
    """以内容里最新日期为基准回推 n 天，避免依赖系统时钟（保证 --ref 可复现）。"""
    from datetime import date, timedelta
    anchor = date.fromisoformat(max(dates))
    return (anchor - timedelta(days=n)).isoformat()


def _gap_days(dates: list[str]) -> int | None:
    from datetime import date
    uniq = sorted({d for d in dates if d})
    if len(uniq) < 2:
        return None
    return (date.fromisoformat(uniq[-1]) - date.fromisoformat(uniq[-2])).days


def _term_stats(counter: dict[str, int], thin_threshold: int) -> dict:
    return {
        "terms": len(counter),
        "single_use": sum(1 for v in counter.values() if v == 1),
        "below_threshold": {"threshold": thin_threshold,
                            "count": sum(1 for v in counter.values() if v < thin_threshold)},
        "top": sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:15],
        "all": dict(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def _size(p: Path) -> int:
    return p.stat().st_size if p.exists() else 0


def _pairs(url_by_content, post_files, public: Path, root: Path):
    for p in post_files:
        rel = str(p.relative_to(root))
        url = url_by_content.get(rel)
        if not url:
            continue
        out = public / url.lstrip("/") / "index.html"
        if out.exists():
            yield url, out.stat().st_size


if __name__ == "__main__":
    raise SystemExit(main())
