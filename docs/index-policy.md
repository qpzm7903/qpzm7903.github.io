# 索引策略（P2）

> 一句话：**该被搜索到的留在索引里，不该被搜索到的用 `noindex` 明确表达，并且不放进 sitemap。**
> 本文是策略的唯一权威说明，`layouts/sitemap.xml`、`layouts/partials/extend_head.html`、`static/robots.txt` 都必须与本文一致。

## 1. 分层

| 层 | 页面 | 索引 | sitemap | 实现 |
|---|---|---|---|---|
| A 不索引 | 承载 < 3 篇文章的 term 页（标签/分类/连载） | `noindex, follow` | 排除 | `extend_head.html` 判断 `eq .Kind "term"` 且 `lt (len .Pages) 3` |
| A 不索引 | 已废弃分类的跳转页（13 个） | `noindex, follow` | 不适用（static 文件天然不进 sitemap） | `scripts/gen-taxonomy-redirects.py` |
| A 不索引 | `/search/`（纯客户端搜索，无独立内容） | `noindex, nofollow` | 排除 | `content/search.md` 的 `robotsNoIndex: true`（PaperMod 原生支持，输出单条声明） |
| B 索引 | 全部文章（含 14 篇薄文章） | `index, follow` | 收录 | 默认 |
| B 索引 | ≥ 3 篇文章的 term 页（当前 23 个标签 + 7 个分类 + 3 个连载） | `index, follow` | 收录 | 默认 |
| B 索引 | 概念卡、归档、首页、taxonomy 索引页 | `index, follow` | 收录 | 默认 |

效果（同口径实测）：sitemap `458 → 449(P1) → 412`；其中 tags `60 → 24（23 term + 索引页）`，**且全部 ≥ 3 篇**；
`noindex` 页面 50 个（36 薄 term + 13 跳转页 + 1 搜索页）。

## 2. 为什么这么定

1. **不 Disallow，只 noindex**：被 `robots.txt` 禁止抓取的 URL，爬虫读不到页面上的 `noindex`，
   等于"没有任何索引信号"，反而可能因外链被收录出低质页面。因此 `robots.txt` 只做 `Allow` + 声明 sitemap。
2. **sitemap 必须是"请索引我"的清单**：保留 noindex 页面在 sitemap 里是自相矛盾的信号，且浪费抓取预算。
3. **阈值 3 篇**：承载 1~2 篇的 term 页对用户几乎无导航价值（本站在此之前有 36 个这样的标签页、8 个单篇分类页），
   但对爬虫是 36 个独立 URL。阈值可调（见 §5），调整必须重跑基线并写进 PR。
4. **薄文章不 noindex**（与初始设想不同，见 ADR-0003）：14 篇薄文章全部属于 `Claude Code 更新`/`Codex 更新` 连载
   （`docs/thin-content.csv`），每篇对应一次具体版本发布，是唯一内容而非重复内容；noindex 会打断连载的连续性，
   收益（省 14 个 URL 的抓取）远小于风险（误伤正常内容）。处理办法改为**内容待办**：合并进月度版本汇总，属内容编辑工作，不在结构重构范围。

## 3. 已知副作用（不藏着）

1. **同页出现两条 `robots` 声明**：PaperMod 的 `head.html` 固定输出 `index, follow`，我们在 `extend_head.html` 追加 `noindex, follow`。
   Google/Bing 按"最严格者生效"取 `noindex`，行为正确；代价是标记冗余、且 `vnu` 会给出提示（P6 处理方式：要么接受并加白名单，要么 override 主题 head）。
   选择不 override 主题模板，是为了避免主题升级时产生合并冲突。
2. **跳转页不是 301**：GitHub Pages 无法下发 301，用 `meta refresh + canonical + noindex` 近似；链接权重传递弱于真 301。
3. **`noindex` 不是删除**：页面仍可访问、仍可被外链引用，只是不进搜索结果。可逆（去掉参数重跑即可）。

## 4. 验证

```bash
# 本地构建产物
bash scripts/audit.sh > /tmp/audit.json
jq '.output.index_policy' /tmp/audit.json        # sitemap_thin_tag_terms 必须为 0
jq '.output.robots'        /tmp/audit.json       # exists=true, declares_sitemap=true

# 构建产物逐项判据（robots / sitemap 抽样 50 条 / 每个 tag 页 ≥3 篇）
bash scripts/verify-index-policy.sh --dir <hugo 构建目录>

# 部署后（PR 合并、Actions 完成）
bash scripts/verify-index-policy.sh --base https://qpzm7903.github.io
```

## 5. 调整阈值

- 阈值常量在两处：`layouts/partials/extend_head.html`（`lt (len .Pages) 3`）与 `layouts/sitemap.xml`（同值）。
  **必须同时改**，否则出现"页面 noindex 但仍在 sitemap"的不一致。
- 改阈值后必须：重跑 `scripts/audit.sh` → 更新本文 §1 的数字 → PR 里贴前后对比。
- `scripts/verify-index-policy.sh` 会校验"noindex 集合 ⊇ sitemap 排除集合"这一致性，改漏了会被它抓住。

## 6. 与后续阶段的关系

- P4（内链）：thin term 页仍会被文章里的链接指向，`follow` 保证爬虫可沿链接继续发现文章。
- P6（CI 门禁）：`index_policy.sitemap_thin_tag_terms == 0`、`tags.below_threshold.count` 上限、`robots.declares_sitemap == true` 将作为断言写进 CI。
