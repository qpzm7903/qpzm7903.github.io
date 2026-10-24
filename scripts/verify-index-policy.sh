#!/usr/bin/env bash
# P2 索引策略校验：robots.txt / sitemap 抽样 / 薄 term 页是否混入 sitemap
#
#   bash scripts/verify-index-policy.sh --dir  /tmp/hugo-build     # 校验本地构建产物
#   bash scripts/verify-index-policy.sh --base https://qpzm7903.github.io
#
# 退出码非 0 表示策略被破坏，可直接作为 CI 断言。
set -uo pipefail

MODE=""; BASE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)  MODE=dir;  BASE="$2"; shift 2 ;;
    --base) MODE=http; BASE="${2%/}"; shift 2 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done
[[ -z "$MODE" ]] && { echo "用法: $0 --dir <build> | --base <url>" >&2; exit 2; }

fail=0
say()  { printf '%s\n' "$*"; }
pass() { printf '  ✅ %s\n' "$*"; }
bad()  { printf '  ❌ %s\n' "$*"; fail=$((fail+1)); }

to_path() { # $1 = 绝对 URL 或 path → /path（已 percent-decode）
  local u="$1"
  u="${u#http://}"; u="${u#https://}"
  [[ "$u" == */* ]] && u="/${u#*/}" || u="/"
  python3 -c 'import sys,urllib.parse;print(urllib.parse.unquote(sys.argv[1]))' "$u"
}

fetch() { # $1 = path
  if [[ "$MODE" == "http" ]]; then
    curl -sS -m 25 "$BASE$1"
  else
    cat "$BASE$1/index.html" 2>/dev/null || cat "$BASE$1" 2>/dev/null
  fi
}

status() { # $1 = path -> HTTP 状态码（dir 模式下用文件存在性代替）
  if [[ "$MODE" == "http" ]]; then
    curl -s -o /dev/null -m 25 -w '%{http_code}' "$BASE$1"
  else
    if [[ -f "$BASE$1/index.html" || -f "$BASE$1" ]]; then echo 200; else echo 404; fi
  fi
}

say "== 1. robots.txt"
robots="$(fetch /robots.txt)"
if grep -qi '^Sitemap:' <<<"$robots"; then pass "robots.txt 声明了 sitemap"; else bad "robots.txt 缺少 Sitemap: 行"; fi
if grep -qi '^Disallow:' <<<"$robots"; then bad "robots.txt 出现 Disallow（会屏蔽 noindex 信号）"; else pass "robots.txt 无 Disallow"; fi

say "== 2. sitemap 可解析 + 规模"
sitemap="$(fetch /sitemap.xml)"
echo "$sitemap" | head -1 | grep -q '<urlset' && pass "sitemap 是 urlset" || bad "sitemap 格式异常"
total=$(grep -o '<loc>' <<<"$sitemap" | wc -l | tr -d ' ')
say "  条目数: $total"
[[ "$total" -gt 300 && "$total" -lt 500 ]] && pass "条目数在合理区间(300~500)" || bad "条目数异常: $total"

say "== 3. sitemap 抽样 50 条 URL 可访问"
sample=$(grep -o '<loc>[^<]*</loc>' <<<"$sitemap" | sed 's/<[^>]*>//g' | awk 'NR%8==0' | head -50)
n=0; bad_n=0
while read -r url; do
  [[ -z "$url" ]] && continue
  path="$(to_path "$url")"
  code=$(status "$path"); n=$((n+1))
  [[ "$code" == "200" ]] || { bad_n=$((bad_n+1)); say "    $code $path"; }
done <<<"$sample"
[[ "$bad_n" -eq 0 ]] && pass "抽样 $n 条全部 200" || bad "抽样 $n 条中 $bad_n 条非 200"

say "== 4. sitemap 中的 term 页必须承载 >= 3 篇文章"
thin=0; checked=0
for raw in $(grep -o '<loc>[^<]*</loc>' <<<"$sitemap" | sed 's/<[^>]*>//g' | grep -E '/(tags|categories|series)/[^/]+/$'); do
  path="$(to_path "$raw")"
  body="$(fetch "$path")"; checked=$((checked+1))
  # PaperMod 每篇文章渲染一个 article.post-entry
  cnt=$(grep -oE 'class="?post-entry"?' <<<"$body" | wc -l | tr -d ' ')
  # 分页上限 20，>=3 即可判定"不薄"
  if [[ "$cnt" -lt 3 ]]; then thin=$((thin+1)); say "    薄 term 混入 sitemap: $path ($cnt 篇)"; fi
done
[[ "$thin" -eq 0 ]] && pass "检查 $checked 个 term 页，全部 >= 3 篇" || bad "$thin 个薄 term 页混入 sitemap"

say "== 5. noindex 与 sitemap 一致性（thin term 不得同时出现）"
# sitemap 有、但页面自身 noindex → 矛盾信号
mismatch=0
for raw in $(grep -o '<loc>[^<]*</loc>' <<<"$sitemap" | sed 's/<[^>]*>//g' | awk 'NR%40==0' | head -12); do
  path="$(to_path "$raw")"
  body="$(fetch "$path")"
  if grep -qE 'name="?robots"? content="?noindex' <<<"$body"; then
    mismatch=$((mismatch+1)); say "    在 sitemap 中但页面 noindex: $path"
  fi
done
[[ "$mismatch" -eq 0 ]] && pass "抽样页面无 sitemap/noindex 冲突" || bad "$mismatch 处冲突"

echo
if [[ "$fail" -eq 0 ]]; then say "✅ 索引策略校验通过（${MODE}）"; else say "❌ 索引策略校验失败：$fail 项"; fi
exit $(( fail > 0 ))
