#!/usr/bin/env python3
import csv
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = ROOT / "public"
CONTENT_POSTS_DIR = ROOT / "content" / "posts"


def run_hugo_list_all() -> str:
    result = subprocess.run(
        ["hugo", "list", "all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def permalink_to_output_path(permalink: str) -> Path:
    parsed = urlparse(permalink)
    rel = parsed.path.lstrip("/")
    if not rel:
        return PUBLIC_DIR / "index.html"
    return PUBLIC_DIR / rel / "index.html"


def main() -> int:
    if not CONTENT_POSTS_DIR.exists():
        print("[verify] content/posts 不存在，跳过。")
        return 0

    content_files = sorted(str(p.relative_to(ROOT)) for p in CONTENT_POSTS_DIR.glob("*.md"))
    listed = set()
    missing_outputs = []

    output = run_hugo_list_all()
    reader = csv.DictReader(output.splitlines())

    for row in reader:
        path = row.get("path", "")
        kind = row.get("kind", "")
        permalink = row.get("permalink", "")
        draft = row.get("draft", "").lower() == "true"

        if not path.startswith("content/posts/"):
            continue
        if kind != "page":
            continue
        if draft:
            continue

        listed.add(path)
        if not permalink:
            missing_outputs.append((path, "<empty permalink>"))
            continue

        out_path = permalink_to_output_path(permalink)
        if not out_path.exists():
            missing_outputs.append((path, str(out_path.relative_to(ROOT))))

    missing_from_list = [p for p in content_files if p not in listed]

    print(f"[verify] markdown posts: {len(content_files)}")
    print(f"[verify] hugo listed pages: {len(listed)}")

    if missing_from_list:
        print("[verify] 以下文章未出现在 `hugo list all` 中：", file=sys.stderr)
        for item in missing_from_list:
            print(f"  - {item}", file=sys.stderr)

    if missing_outputs:
        print("[verify] 以下文章缺少对应生成页面：", file=sys.stderr)
        for src, out in missing_outputs:
            print(f"  - {src} -> {out}", file=sys.stderr)

    if missing_from_list or missing_outputs:
        return 1

    print("[verify] 所有 posts 页面都已成功生成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
