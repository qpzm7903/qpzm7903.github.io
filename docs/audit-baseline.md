# 站点结构基线（P0）

> 本文件是后续 P1–P6 全部改动的**唯一比较基准**。任何"优化了"的结论，必须能用同一脚本、同一口径复现出前后数字。

- 基线 commit：`ef55945`
- 对照 commit：`ecb9569`（最后一篇日报，产线断流前）
- 快照文件：`docs/audit/ef55945.json`、`docs/audit/ecb9569.json`
- 脚本：`scripts/audit.sh`（构建编排） + `scripts/audit.py`（指标计算，仅标准库）

## 1. 如何复现

```bash
# 当前工作区
bash scripts/audit.sh | jq -e '.posts == 366'

# 历史版本（git worktree + submodule，同一套度量代码）
bash scripts/audit.sh --ref ecb9569 | jq '.posts'

# 落盘快照，便于 diff
bash scripts/audit.sh > docs/audit/$(git rev-parse --short HEAD).json
```

约定：**stdout 只有 JSON**（可直接管道给 `jq`），构建日志走 stderr，产物构建到临时目录，不污染工作区。

## 2. 忠实性验证（审计口径必须等于线上口径）

体积类指标只有在"与 CI 相同的构建参数"下才可比，因此 `audit.sh` 使用与 `.github/workflows/hugo.yaml` 一致的
`hugo --minify --buildFuture --cleanDestinationDir`。抽样对照线上：

| 页面 | 线上字节 | 审计构建字节 | 一致 |
|---|---|---|---|
| `/` | 50296 | 50296 | ✅ |
| `/archives/` | 171528 | 171528 | ✅ |

这条对照是"审计能代表线上"的必要证据；如果哪天不一致，说明构建参数或 Hugo 版本漂移，必须先修口径。

## 3. 指标口径

| 指标 | 定义 | 取数来源 | 为什么这样定义 | 已知局限 |
|---|---|---|---|---|
| `posts` | `content/posts/*.md` 文件数（不含 `_index.md`） | 文件系统 | 与 `hugo list all` 的 page 数一致，是最稳的基数 | 不等于"有索引价值的页面数" |
| `thin_posts` | 正文 Markdown 字节 < 1500 的篇数 | 文件大小 | 字节是产物无关的代理指标，避免中文分词依赖 | 代码多、中文少的文章可能被误判 |
| `content.md_bytes` | 正文 Markdown 字节的中位/p90/max | 文件大小 | 观察内容分布，防止"平均值掩盖长尾" | 同上 |
| `content.date.last_two_gap_days` | 最近两篇文章日期差（天） | front matter `date` | 比"近 30 天篇数"更抗单篇噪声，直接暴露产线断流 | 依赖 `date` 可信 |
| `taxonomy.categories.terms` | 分类去重后条目数 | front matter `categories` | 分类应少而稳 | 仅统计 posts 目录 |
| `taxonomy.*.single_use` | 只被 1 篇文章使用的条目数 | 同上 | 一次性条目几乎无导航价值 | |
| `taxonomy.*.below_threshold.count` | 承载 < 3 篇文章的条目数 | 同上 | 用于判定"薄 term 页该不该进索引"（P2 依据） | 阈值 3 是经验值，需 ADR 记录 |
| `taxonomy.menu_coverage.ratio` | 菜单里分类入口覆盖的文章数 / 分类条目总数 | `hugo.yaml` menu + front matter | 量化"导航失真"：菜单点进去到底能看到多少内容 | 只算 categories 入口，不含 tags/archives |
| `links.internal_total` | 正文中指向站内的链接条数 | 正文（剔除代码块），markdown `[]()` + HTML `<a href>` | 内链是发现性的硬指标 | 不含主题自动生成的"上一篇/归档"链接（那些不是编辑行为） |
| `links.internal_per_post_median` | 每篇正文内链数的中位数 | 同上 | 中位数能立刻暴露"绝大多数文章零内链" | |
| `links.posts_without_internal_link` | 正文 0 条内链的文章数 | 同上 | 与上一条互补 | |
| `links.orphan_posts` | **没有任何其他内容页**（posts + concepts）正文链接指向它的文章数 | 入链图（链接目标按 permalink 规范化匹配） | 孤儿页 = 只能靠列表页被发现的页面 | 自动列表页（首页/归档/taxonomy）不计入，否则孤儿率永远为 0 |
| `metadata.coverage.*` | front matter 中出现的篇数（`description`/`lastmod`/`slug`/`aliases`/`series`） | front matter | 决定 SEO 摘要质量与 URL 迁移能力 | 不判断内容质量 |
| `metadata.html_lang` | 首页 `<html lang>` | 构建产物 | 语言信号错误会同时影响 SEO 与读屏 | |
| `metadata.jsonld.issues` | 抽样文章 JSON-LD 的问题（`inLanguage` 非 zh、`author.name` 嵌套、`description`/`articleBody` 塞全文） | 构建产物 | 结构化数据"有但错"是最常见的假达标 | 只抽最新 1 篇，不代表全站 |
| `output.html_bytes_posts` | 文章页 `index.html` 字节的中位/p90/max | 构建产物 | 体积是可预算、可门禁的硬指标 | 未 gzip；CI 预算应按同口径定 |
| `output.md_to_html_ratio_median` | HTML 字节 / Markdown 字节 的中位数 | 两者 | 暴露"模板注入放大正文"这类结构性浪费 | |
| `output.sitemap.*` | sitemap 中 URL 按路径分桶计数 | 构建产物 | sitemap 是给搜索引擎的"请索引我"清单 | 不判断页面质量 |
| `output.rss.*` | 首页 RSS 字节/条目数 + 单篇 RSS 文件数 | 构建产物 | 订阅成本与重复内容 | |
| `output.robots` | `robots.txt` 是否存在、是否声明 sitemap | 构建产物 | 缺失即无法指导抓取 | 线上 404 已单独核验 |
| `build.hugo_warnings` | 构建日志中 `WARN` 行数 | `hugo` 日志 | P6 要把警告收成 0 并加 `--panicOnWarning` | 数量≠严重性 |

## 4. 基线数据

### 4.1 当前（`ef55945`，366 篇）

| 维度 | 指标 | 值 |
|---|---|---|
| 内容 | posts / concept_pages | 366 / 7 |
| 内容 | Markdown 字节 中位 / p90 / max | 6809 / 9937 / 22337 |
| 内容 | 薄内容（< 1500B） | 14 篇 |
| 内容 | 首篇 / 末篇 / 最近两篇间隔 | 2026-03-07 / 2026-10-23 / **81 天** |
| 分类 | 分类条目 / 仅 1 篇 / < 3 篇 | **20 / 8 / 12** |
| 分类 | **菜单分类覆盖度** | **67 / 366 = 17.91%** |
| 标签 | 标签条目 / 仅 1 次 / < 3 篇 | **59 / 35 / 37** |
| 系列 | `series` 条目 | **0** |
| 链接 | 内链总数 / 外链总数 | 144 / 954 |
| 链接 | 每篇内链中位数 / 零内链篇数 | **0.0 / 343** |
| 链接 | **孤儿页** | **303 篇（82.79%）** |
| 元数据 | description / lastmod / slug / aliases / series | **9 / 0 / 0 / 0 / 0** |
| 元数据 | `<html lang>` | **en**（内容 zh-cn） |
| 元数据 | 首页 og:image | 无 |
| 元数据 | JSON-LD 类型 / 问题 | BreadcrumbList + BlogPosting / `inLanguage='en'`、`articleBody_duplicates_body` |
| 体积 | 文章页 HTML 中位 / p90 / max | **38544 / 56228 / 120733** B |
| 体积 | `HTML/Markdown` 中位倍率 | **7.23×** |
| 体积 | 首页 / 归档页 | 50296 / **171528** B |
| 索引 | sitemap 总数（posts/tags/categories/other） | **458**（367 / 60 / 21 / 10） |
| 订阅 | index.xml 字节 / 条目 / 单篇 RSS 文件 | **2.10 MB / 372 / 366** |
| 抓取 | robots.txt | **不存在**（线上 404） |
| 构建 | hugo WARN | 4（`languageCode` 弃用、`.Language.LanguageDirection` 弃用、`.Language.LanguageCode` 弃用、`Raw HTML omitted` 各 1 条） |

### 4.2 与历史对照（`ecb9569`）

| 指标 | `ecb9569` | `ef55945` | 说明 |
|---|---|---|---|
| posts | 365 | 366 | 只多了一篇手写文章 |
| 分类条目 | 19 | 20 | 持续发散 |
| 标签条目 | 52 | 59 | 持续发散（+7） |
| 孤儿页 | 302（82.74%） | 303（82.79%） | **结构问题不是新增的，是既有的** |
| 文章页 HTML 中位 | 38538 | 38544 | 模板未变，体积问题稳定存在 |
| RSS 条目 | 371 | 372 | 全文 RSS 从未收敛 |
| sitemap 总数 | 449 | 458 | 随 taxonomy 膨胀而膨胀 |

对照的意义：**这些不是"最近才坏"的偶发问题，而是稳定的结构性缺陷**，所以修复应当是结构性修复，而不是补丁。

## 5. 由基线直接支撑的事实（P1–P6 的输入）

- **F1** 菜单分类只覆盖 17.91% 的文章 → 导航与内容模型脱节（→ P1）
- **F2** 分类 20 个、8 个仅 1 篇；标签 59 个、35 个仅 1 次 → taxonomy 发散，无收敛机制（→ P1）
- **F3** `series` = 0，而 163 篇是同一产品线的连载 → 连载没有结构表达（→ P1）
- **F4** 孤儿页 82.79%，每篇内链中位数 0 → 发现性依赖列表页（→ P4）
- **F5** `description` 覆盖 9/366 → 摘要由模板截正文前两行（→ P3）
- **F6** `<html lang>=en`、JSON-LD `inLanguage='en'`、`articleBody` 全文注入 → 元数据错误 + 体积放大（→ P3）
- **F7** 文章页 HTML 中位 38.5KB，`HTML/MD` 中位 7.23× → 存在可量化的模板级浪费（→ P3/P5）
- **F8** sitemap 含 60 个 tags + 21 个 categories，其中 37 个标签页 < 3 篇 → 抓取预算被薄页面占用（→ P2）
- **F9** 无 `robots.txt`，线上 404 → 无法声明 sitemap、无法做抓取分层（→ P2）
- **F10** RSS 2.10MB / 372 条全文 + 366 个单篇 RSS → 订阅成本与重复 URL（→ P5）
- **F11** 归档页 171KB 单页 366 条 → 单页体积与可用性问题（→ P5）
- **F12** 最近两篇间隔 81 天 → 产线断流无监控（→ P6，需要新鲜度断言/看门狗）
- **F13** 14 篇薄内容（< 1500B）+ `CONTEXT.md` 规定"禁止暂无摘要"却线上存在 → 内容规则无自动校验（→ P2/P6）

## 6. 已知局限（不要把这些当结论）

1. **无用户侧数据**：本基线只有站点自身产物，没有 Search Console / CrUX。任何"搜索表现会变好"的说法在拿到 GSC 前后都不能成立（复核方法见交付物 5）。
2. **CJK 字数**：字节数不等于字数，`wordCount` 类指标不做。
3. **孤儿页口径偏保守**：只统计正文链接，不含主题自动生成的列表页；因此"孤儿 303 篇"是"编辑层面无入链"，不是"搜索引擎发现不了"。
4. **JSON-LD 只抽 1 篇**：用于发现模式性问题，不作为全站统计。
5. **体积未 gzip**：CI 预算应沿用本口径（minified HTML 字节），如果要报传输体积需另立口径并重跑基线。

## 7. 口径维护规则

- 修改任何指标定义 → 同 PR 内更新本文档 §3 表格 + 重跑基线 + 在 PR 描述里说明"为什么旧口径不够用"
- 修改 `audit.sh` 的构建参数 → 必须重新验证 §2 的"线上字节一致"对照
- 新增指标 → 必须写清"它能推翻什么判断"，否则不进基线
