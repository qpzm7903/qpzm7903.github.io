#!/usr/bin/env python3
"""P1: 为已废弃的分类 URL 生成"等价内容"重定向页。

背景：GitHub Pages 是纯静态托管，无法下发 301。分类收敛后旧 term URL
（如 /categories/日报/）会变成 404，违反"不得产生新 404"的硬约束，
因此为每个废弃 term 生成一张静态跳转页：
  * <meta http-equiv="refresh"> → 新 term
  * <link rel="canonical">      → 新 term（把信号收敛到新 URL）
  * <meta name="robots" content="noindex">（跳转页本身不该被索引）
  * <a> 兜底链接（禁用 meta refresh 的场景）

用法：python3 scripts/gen-taxonomy-redirects.py [--check]
  --check 只校验现状，不写文件（供 CI 使用）
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static" / "categories"

BASE_URL = "https://qpzm7903.github.io"

# 旧 term → (目标 term, 原因)
REDIRECTS: dict[str, tuple[str, str]] = {
    # 旧"大合集"日报按 PIPELINE「AI 优先」归并
    "日报": ("AI日报", "旧大合集日报，按跨话题去重规则归入 AI 优先"),
    "AI 工具": ("AI日报", "AI 工具类日报归入 AI 日报"),
    # 一次性技术分类统一收敛为「技术」
    "Java 性能分析": ("技术", "一次性分类收敛"),
    "Kubernetes": ("技术", "一次性分类收敛"),
    "实战指南": ("技术", "一次性分类收敛"),
    "架构分析": ("技术", "一次性分类收敛"),
    "技术教程": ("技术", "一次性分类收敛"),
    "工程实践": ("技术", "一次性分类收敛"),
    "技术分析": ("技术", "一次性分类收敛"),
    "工具推荐": ("技术", "一次性分类收敛"),
    "架构设计": ("技术", "一次性分类收敛"),
    "技术管理": ("技术", "一次性分类收敛"),
    "开源项目": ("技术", "一次性分类收敛"),
}

PAGE = """<!doctype html>
<!-- 由 scripts/gen-taxonomy-redirects.py 生成：{old} → {new}（{reason}）。
     静态托管无法下发 301，这里用 meta refresh + canonical 做等价跳转。 -->
<html lang="zh-cn">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target_path}">
<link rel="canonical" href="{target_url}">
<title>{old} → {new}（分类已迁移）</title>
</head>
<body>
<p>分类「{old}」已收敛为「{new}」，正在跳转……</p>
<p><a href="{target_path}">如果没有自动跳转，点这里</a></p>
</body>
</html>
"""


def term_path(term: str) -> str:
    # Hugo 会把 term 名转成小写路径；中文不受影响
    return f"/categories/{term.lower()}/"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    missing, stale = [], []
    for old, (new, reason) in REDIRECTS.items():
        out = STATIC / old / "index.html"
        target = term_path(new)
        expected = PAGE.format(old=old, new=new, reason=reason, target_path=target,
                               target_url=BASE_URL + target)
        if args.check:
            if not out.exists():
                missing.append(f"{old}（缺文件）")
            elif out.read_text(encoding="utf-8") != expected:
                stale.append(f"{old}（内容需重新生成）")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(expected, encoding="utf-8")

    if args.check:
        if missing or stale:
            print(f"❌ 重定向页不完整：missing={missing} stale={stale}", file=sys.stderr)
            return 1
        print(f"✅ {len(REDIRECTS)} 个废弃分类重定向页齐全且内容正确")
        return 0

    print(f"已生成 {len(REDIRECTS)} 个重定向页 → {STATIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
