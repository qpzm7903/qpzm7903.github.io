# 索引卫生：noindex 只用在"薄 term 页/跳转页/搜索页"，并用 sitemap 过滤让"请索引"清单自洽

## 背景

P0 基线实测：

- sitemap 458 条 URL，其中 **60 条 tag 页 + 21 条分类页**；59 个标签里 **35 个只被 1 篇文章使用**（P1 后 36 个 < 3 篇）
- 完全没有 `robots.txt`（线上 404），既无法声明 sitemap，也无法表达抓取意愿
- 13 个被废弃的分类 term 在 P1 收敛后需要"等价内容"承接（GH Pages 无 301）
- 14 篇文章正文 < 1500 字节（`docs/thin-content.csv`），且**全部属于连载**（Claude Code 更新 81 / openclaw 更新 46 / Codex 更新 36）

问题本质不是"页面太多"，而是**索引信号不自洽**：sitemap 声称"这些都值得索引"，但其中 36 个页面只有 1 篇内容。

## 决策

1. `robots.txt`：只 `Allow: /` + `Sitemap:` 声明，**不使用 `Disallow`**
2. 承载 **< 3 篇**的 term 页：`noindex, follow`（保留链接权重传递）
3. sitemap 只收录"该索引"的 URL：自定义 `layouts/sitemap.xml`，排除薄 term 页与 `noindex` 页面
4. 13 个废弃分类跳转页：`noindex, follow` + 自引用不足时用 canonical 指向新 term
5. `/search/`：`robotsNoIndex: true`（主题原生，单条 `noindex, nofollow`）
6. **14 篇薄文章不 noindex**，转为内容待办（见 Consequences）

## Considered Options

- **A. 用 `robots.txt` Disallow 掉薄 term 页**：被否。被 Disallow 的 URL 爬虫读不到页面上的 `noindex`，
  等于"没有任何信号"，仍可能凭外链被收录出低质页面；这是 Google 明确警告的反模式。
- **B. 直接不生成薄 term 页（删标签）**：被否。会产生 36 个新 404（需再补 36 个跳转页），
  且标签是内容维度，删不删属内容决策，不该由结构重构顺手决定；还会破坏文章里的既有标签语义。
- **C. 只 noindex，不改 sitemap**：被否。sitemap 的语义是"请索引我"，收录 noindex 页面是自相矛盾的信号，
  抓取预算也没省下来（爬虫仍会来）。
- **D. noindex + sitemap 过滤（采纳）**：两个信号一致，且都可逆（删配置即恢复）。
- **E. 薄文章也 noindex（原设想）**：被否。14 篇薄文章全部属于连载，每篇对应一次具体版本发布，
  是唯一内容而非重复内容；noindex 会打断连载连续性，且省下的抓取预算可忽略（14 个 URL）。
  改为内容待办（合并为月度版本汇总），属编辑工作，不在结构重构范围。
- **F. override `layouts/partials/head.html` 以消除重复的 robots 声明**：被否（本阶段）。
  代价是 fork 主题模板、升级时冲突；收益只是少一条 meta。选择在 `extend_head.html` 追加，
  依赖"多条 robots 取最严格者"的既定行为，并在 `docs/index-policy.md` 记录该副作用。

## Consequences

- **正面**：sitemap 从 458 降到 412 条，其中 tag 页 60 → 24 且**全部 ≥ 3 篇**；索引信号自洽；
  `robots.txt` 让 sitemap 可被发现；废弃 URL 仍有等价承接。
- **代价**：
  1. 同一页面可能出现两条 `robots` 声明（`index, follow` + `noindex, follow`），`vnu` 会给提示；
  2. 跳转页是 `meta refresh`，不是 301，权重传递弱；
  3. 阈值 3 是经验值，写死在模板两处（`extend_head.html`、`sitemap.xml`），**改一处忘另一处会造成不一致**，
     因此 `scripts/verify-index-policy.sh` 专门校验"noindex 与 sitemap 排除集合一致"。
- **可逆**：去掉 `extend_head.html` 的注入、恢复默认 sitemap 模板即可；无内容改动。
- **监测**：`audit.sh` 新增 `output.index_policy`（`noindex_pages`、`sitemap_thin_tag_terms` 必须为 0、
  `sitemap_tag_terms`）；P6 把这些写进 CI 断言。
- **遗留待办**：14 篇薄文章合并/扩充（`docs/thin-content.csv`）；标签大小写与空格归一化
  （本次顺手修了 `Codex`/`codex` 冲突导致的 term 页被覆盖，暴露此类问题需要 P4 的标签治理规则）。
