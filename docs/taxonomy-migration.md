# 分类法迁移（P1）

> 目标：把 20 个漂移的分类收敛为**可解释的少量稳定值**，并把"连载"这一维度从分类里拆出来。
> 迁移规则全部来自仓库内既有的领域文档，不是外部最佳实践的生搬硬套。

- 规则来源：`automation/topics/*.yaml`（各话题的 `category` 字段）、`automation/PIPELINE.md`（跨话题去重规则）、`CONTEXT.md`（话题/话题日报/概念卡词汇）
- 迁移脚本：`scripts/migrate-taxonomy.py`（dry-run 默认，`--apply` 才写文件，自带幂等性检查）
- 跳转页生成：`scripts/gen-taxonomy-redirects.py`（`--check` 供 CI 用）
- 逐篇映射清单：`docs/taxonomy-migration.csv`（366 行，含"为什么归到这里"）

## 1. 收敛结果

| 目标分类 | 篇数 | 含义 |
|---|---:|---|
| 工具更新 | 163 | 产品线更新日志（连载），用 `series` 区分具体产品 |
| AI日报 | 126 | 话题日报（AI 优先归口） |
| 论文日报 | 23 | 话题日报 |
| 科技日报 | 23 | 话题日报 |
| 股票日报 | 17 | 话题日报 |
| 技术 | 10 | 手写技术长文 |
| 周报 | 4 | 周期性综述 |
| **合计** | **366** | 与 `posts` 一致，无遗漏 |

分类条目：**20 → 7**（其中仅 1 篇的条目 8 → 0；< 3 篇的条目 12 → 1）

连载（`series`，新增 Hugo taxonomy，URL 为 `/series/`）：

| series | 篇数 |
|---|---:|
| Claude Code 更新 | 81 |
| openclaw 更新 | 46 |
| Codex 更新 | 36 |
| **合计** | **163**（= 工具更新全部） |

## 2. 迁移规则与依据

| 旧分类（篇数） | 新分类 | 依据 |
|---|---|---|
| `工具更新`（163） | `工具更新` + `series` | 内容性质是产品线更新日志，不是话题日报；产品线是第二维度，用 `series` 表达（81/46/36） |
| `日报`（100） | `AI日报` | `PIPELINE.md`「跨话题去重：同一条目命中多个话题时归入 AI 优先」；这批 `daily-news-*` 的内容正是 AI 官方动态 + HN + GitHub Trending 的混合 |
| `AI日报`（24） | `AI日报` | 已是目标值 |
| `论文日报`（23）/ `科技日报`（23）/ `股票日报`（17）/ `周报`（4） | 同名 | 已是 `automation/topics/*.yaml` 里定义的话题分类 |
| `AI 工具`（2） | `AI日报` | AI 工具类日报，非产品线连载 |
| `AI 工具`+`架构分析`（1）、`AI 工具`+`开源项目`+`架构分析`（1） | `技术` | 含架构/开源分析类旧分类的手写长文，按"内容性质优先于来源标签"归入技术长文 |
| `Java 性能分析`/`Kubernetes`/`实战指南`/`架构分析`/`技术教程`/`工程实践`/`技术分析`/`工具推荐`/`架构设计`/`技术管理`/`开源项目`（共 8 篇，11 个一次性分类） | `技术` | 一次性分类无导航价值；这些都属"手写技术长文"，合并为一个稳定值 |

**未改动**：`tags`（59 个，35 个仅 1 次）。原因：标签是"实体维度"（Claude Code / Codex / HN / 论文 / 财经…），
删标签会造成 term URL 404，与硬约束冲突；其索引分层在 P2 用 `noindex` + sitemap 过滤解决，见 ADR-0003。

## 3. URL 兼容方案（不能产生新 404）

GitHub Pages 无法下发 301，因此对 **13 个被废弃的分类 term** 生成静态跳转页：

```
static/categories/<旧 term>/index.html
  ├─ <meta http-equiv="refresh" content="0; url=/categories/<新 term>/">
  ├─ <link rel="canonical" href="https://qpzm7903.github.io/categories/<新 term>/">
  ├─ <meta name="robots" content="noindex, follow">
  └─ <a> 兜底链接
```

| 旧 term | 去向 |
|---|---|
| `日报`、`AI 工具` | `/categories/ai日报/` |
| `Java 性能分析`、`Kubernetes`、`实战指南`、`架构分析`、`技术教程`、`工程实践`、`技术分析`、`工具推荐`、`架构设计`、`技术管理`、`开源项目` | `/categories/技术/` |

保留不动的 URL（无迁移成本）：`AI日报`、`论文日报`、`科技日报`、`股票日报`、`周报`、`工具更新`、`技术` 的 term 页；
所有**文章 URL 均未变化**（没有改文件名、没有加 `slug`）。

## 4. 菜单与 taxonomy 注册

- `hugo.yaml` 菜单从 10 项扩到 13 项，新增 `工具更新`、`技术`、`连载`（`/series/`），使**每个分类入口都能到达一类内容**
- `hugo.yaml` 新增 `taxonomies` 段，显式注册 `series`（Hugo 默认只有 `tags`/`categories`，不注册则 front matter 里的 `series` 不生成任何页面——这是本次改动里唯一的"坑"）

## 5. 验收证据（脚本输出，非主观判断）

```bash
# 分类计数之和 == 篇数
$ bash scripts/audit.sh | jq -e '[.taxonomy.categories.all[]] | add == 366'
true

# 分类收敛到 7 个、series 3 个
$ bash scripts/audit.sh | jq '{cats: .taxonomy.categories.terms, series: .taxonomy.series.all}'
{"cats": 7, "series": {"Claude Code 更新": 81, "openclaw 更新": 46, "Codex 更新": 36}}

# 菜单覆盖度（要求 ≥ 95%）
$ bash scripts/audit.sh | jq '.taxonomy.menu_coverage.ratio'
1.0

# series 落地篇数
$ grep -l '^series:' content/posts/*.md | wc -l
163

# 旧分类 URL 兼容
$ python3 scripts/gen-taxonomy-redirects.py --check
✅ 13 个废弃分类重定向页齐全且内容正确

# 正文零改动（迁移只碰 front matter）
正文哈希 前: a161033b5aef83b9  后: a161033b5aef83b9  一致: True
$ git diff --shortstat
274 files changed, 274 insertions(+), 111 deletions(-)
```

构建产物核对：`/categories/` 下剩 7 个真实 term 页 + 13 个跳转页；`/series/` 下 3 个 term 页；
sitemap 从 458 条降为 449 条（-13 旧分类页 +4 连载页）。

## 6. 明确不在本阶段做的

1. **面包屑**：PaperMod 的 breadcrumb 由 section 层级生成（`Posts > 标题`），要改成"分类 > 标题"需要 override `layouts/_default/single.html`，
   与 P4 的 hub 页/相关文章同属"模板层改动"，放同一 PR 才自洽（已记入 ADR-0002 后果项）。
2. **series 的 URL 美化**：当前 term URL 是 `/series/claude-code-更新/`（Hugo 对混合中英 term 的默认 slug 化结果）。
   若要 `/series/claude-code/`，需为每个 term 建 `content/series/<term>/_index.md` 并设 `slug`——属 P4 的 hub 页工作。
3. **标签治理**：见 ADR-0003（P2 阶段产出）。

## 7. 回滚

```bash
git revert <P1 commit>          # front matter + hugo.yaml + static 跳转页一起回退
# 或者只回退 front matter：
git checkout <P1 commit>^ -- content/posts
```
迁移脚本幂等（二次运行 0 变更），可安全重跑。
