#!/usr/bin/env python3
"""P1: 分类法收敛 + 连载（series）落地。

规则来源（不是拍脑袋）：
  * 目标分类词表取自 `automation/topics/*.yaml` 的 `category` 字段 + 手写技术长文单独成类
  * `日报`(100 篇) 归入 AI日报：依据 `automation/PIPELINE.md`「跨话题去重：命中多个话题时归入 AI 优先」
  * `工具更新`(163 篇) 保留为分类，产品线用 series 表达（Claude Code / Codex / openclaw 更新）
  * 11 个一次性技术分类（Java 性能分析/Kubernetes/实战指南/…）收敛为 `技术`

用法：
    python3 scripts/migrate-taxonomy.py            # dry-run，打印映射与统计
    python3 scripts/migrate-taxonomy.py --apply    # 写回文件
    python3 scripts/migrate-taxonomy.py --report docs/taxonomy-migration.csv
"""

from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"

# 目标分类（收敛后必须只剩这些值）
TARGET_CATEGORIES = ["AI日报", "工具更新", "技术", "论文日报", "科技日报", "股票日报", "周报"]

# 已是目标分类 → 保持不变
KEEP = set(TARGET_CATEGORIES)

# 旧分类 → 新分类（不含"保持不变"的）
LEGACY_MAP = {
    "日报": ("AI日报", "PIPELINE 跨话题去重规则：命中多话题归入 AI 优先"),
    "AI 工具": ("AI日报", "AI 工具类日报，非产品线连载"),
}

# 产品线连载（文件名前缀 → series 名），优先级高于旧分类
SERIES_BY_PREFIX = [
    ("claude-code-update", "Claude Code 更新"),
    ("codex-update", "Codex 更新"),
    ("openclaw-update", "openclaw 更新"),
]

# 手写技术长文：以下旧分类（都是 1~2 篇的一次性分类）统一收敛到 `技术`
TECH_LEGACY = {
    "Java 性能分析", "Kubernetes", "实战指南", "架构分析", "技术教程",
    "工程实践", "技术分析", "工具推荐", "架构设计", "技术管理", "开源项目",
}

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def fm_list(fm: str, key: str) -> list[str]:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return []
    v = m.group(1).strip()
    if v.startswith("["):
        return [x.strip().strip("'\"") for x in v.strip("[]").split(",") if x.strip()]
    return [v.strip("'\"")] if v else []


def decide(path: Path, cats: list[str]) -> tuple[str, str | None, str]:
    """返回 (目标分类, series, 理由)。"""
    name = path.name
    for prefix, series in SERIES_BY_PREFIX:
        if name.startswith(prefix):
            return "工具更新", series, f"文件名前缀 {prefix} → 产品线连载"
    if cats:
        # 多重旧分类时：优先目标话题分类；含架构/教程类旧分类的手写长文归 技术
        keep_hits = [c for c in cats if c in KEEP]
        if keep_hits:
            return keep_hits[0], None, "已是目标分类"
        tech_hits = [c for c in cats if c in TECH_LEGACY]
        if tech_hits:
            return "技术", None, f"含旧分类 {tech_hits[0]} → 技术（手写技术长文）"
        first = cats[0]
        if first in LEGACY_MAP:
            target, why = LEGACY_MAP[first]
            return target, None, f"旧分类 {first} → {target}（{why}）"
        if first in TECH_LEGACY:
            return "技术", None, f"旧分类 {first} → 技术（一次性分类收敛）"
    return "技术", None, "无分类/未知 → 技术（兜底，需人工复核）"


def rewrite(text: str, target: str, series: str | None) -> str:
    m = FM_RE.match(text)
    if not m:
        raise SystemExit("缺少 front matter")
    fm, body = m.group(1), text[m.end():]

    # 1) 替换 categories（单行 inline 或 block 列表都处理）
    lines = fm.split("\n")
    out: list[str] = []
    i = 0
    replaced = False
    while i < len(lines):
        line = lines[i]
        if re.match(r"^categories:", line):
            out.append(f'categories: ["{target}"]')
            replaced = True
            i += 1
            # 丢弃 block 列表续行
            while i < len(lines) and re.match(r"^\s+-\s", lines[i]):
                i += 1
            continue
        if re.match(r"^series:", line):
            i += 1
            while i < len(lines) and re.match(r"^\s+-\s", lines[i]):
                i += 1
            continue
        out.append(line)
        i += 1
    if not replaced:
        out.append(f'categories: ["{target}"]')

    # 2) series 紧跟在 categories 之后
    if series:
        idx = next(k for k, l in enumerate(out) if re.match(r"^categories:", l))
        out.insert(idx + 1, f'series: ["{series}"]')

    return "---\n" + "\n".join(out) + "\n---\n" + body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    rows = []
    for p in sorted(POSTS.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        cats = fm_list(m.group(1), "categories") if m else []
        target, series, why = decide(p, cats)
        rows.append({"file": str(p.relative_to(ROOT)), "old_categories": "|".join(cats),
                     "new_category": target, "series": series or "", "reason": why,
                     "text": text})

    dist = collections.Counter(r["new_category"] for r in rows)
    unknown = {r["new_category"] for r in rows} - set(TARGET_CATEGORIES)
    if unknown:
        print(f"❌ 出现未登记的目标分类: {unknown}", file=sys.stderr)
        return 2
    if sum(dist.values()) != len(rows):
        print("❌ 分类计数与篇数不符", file=sys.stderr)
        return 2

    print(f"篇数: {len(rows)}")
    print("目标分类分布:")
    for term, n in dist.most_common():
        print(f"  {n:4d}  {term}")
    series_dist = collections.Counter(r["series"] for r in rows if r["series"])
    print("series 分布:", dict(series_dist) or "(无)")
    print("旧分类映射:")
    old_map = collections.Counter(f'{r["old_categories"] or "(无)"} → {r["new_category"]}'
                                 for r in rows)
    for k, v in old_map.most_common():
        print(f"  {v:4d}  {k}")

    if args.report:
        rp = ROOT / args.report
        rp.parent.mkdir(parents=True, exist_ok=True)
        with rp.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["file", "old_categories", "new_category", "series", "reason"])
            w.writeheader()
            for r in rows:
                w.writerow({k: r[k] for k in w.fieldnames})
        print(f"映射表已写入 {rp}")

    if not args.apply:
        print("\n(dry-run，未修改文件；加 --apply 生效)")
        return 0

    changed = 0
    for r in rows:
        new_text = rewrite(r["text"], r["new_category"], r["series"] or None)
        if new_text != r["text"]:
            (ROOT / r["file"]).write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"\n已改写 {changed} 个文件")

    # 幂等性：再跑一次应 0 变更
    again = 0
    for r in rows:
        p = ROOT / r["file"]
        text = p.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        cats = fm_list(m.group(1), "categories") if m else []
        target, series, _ = decide(p, cats)
        if rewrite(text, target, series or None) != text:
            again += 1
    print(f"幂等性检查: 二次运行变更数 = {again}（应为 0）")
    return 0 if again == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
