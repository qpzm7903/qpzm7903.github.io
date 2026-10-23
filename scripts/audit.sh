#!/usr/bin/env bash
# 站点结构审计（可复现基线）
#
#   bash scripts/audit.sh                 # 审计当前工作区
#   bash scripts/audit.sh --ref <commit>  # 审计历史 commit（同一套度量代码）
#
# 约定：
#   * stdout 只输出 JSON（可 `| jq`），日志一律走 stderr
#   * 不写入仓库目录（hugo 产物构建到临时目录），因此可安全在 CI/任意分支执行
#   * --ref 模式用 git worktree + submodule，保证历史版本可构建
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUDIT_PY="$REPO_ROOT/scripts/audit.py"
REF=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ref) REF="${2:?--ref 需要 commit/branch}"; shift 2 ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

TMP_BUILD="$(mktemp -d)"
TMP_WT=""
cleanup() {
  rm -rf "$TMP_BUILD"
  if [[ -n "$TMP_WT" ]]; then
    git -C "$REPO_ROOT" worktree remove --force "$TMP_WT" >/dev/null 2>&1 || rm -rf "$TMP_WT"
  fi
}
trap cleanup EXIT

TARGET_ROOT="$REPO_ROOT"
GENERATED_AT="$(git -C "$REPO_ROOT" log -1 --format=%cI 2>/dev/null || date -u +%FT%TZ)"

if [[ -n "$REF" ]]; then
  TMP_WT="$(mktemp -d)/wt"
  git -C "$REPO_ROOT" worktree add --detach "$TMP_WT" "$REF" >&2
  git -C "$TMP_WT" submodule update --init --recursive >&2
  TARGET_ROOT="$TMP_WT"
  GENERATED_AT="$(git -C "$TMP_WT" log -1 --format=%cI)"
  echo "[audit] 目标: $REF ($(git -C "$TMP_WT" rev-parse --short HEAD))" >&2
else
  echo "[audit] 目标: 当前工作区 ($(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo 'no-git'))" >&2
fi

echo "[audit] hugo build → $TMP_BUILD" >&2
HUGO_LOG="$TMP_BUILD/hugo.log"
# 与 CI 保持一致的构建参数，否则体积类指标不可比
( cd "$TARGET_ROOT" && hugo --minify --buildFuture --cleanDestinationDir -d "$TMP_BUILD/site" ) >"$HUGO_LOG" 2>&1 || {
  echo "[audit] hugo 构建失败：" >&2
  tail -30 "$HUGO_LOG" >&2
  exit 1
}

WARN_COUNT="$(grep -c 'WARN' "$HUGO_LOG" || true)"
echo "[audit] hugo 警告数: $WARN_COUNT" >&2

python3 "$AUDIT_PY" \
  --root "$TARGET_ROOT" \
  --public "$TMP_BUILD/site" \
  --generated-at "$GENERATED_AT" \
  --hugo-warnings "$WARN_COUNT"
