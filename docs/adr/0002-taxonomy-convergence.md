# 分类法收敛：20 → 7，并把"连载"从分类拆到 series

## 背景

站点累计 366 篇文章后，分类法已漂移为 20 个值：`工具更新`(163)、`日报`(100)、按话题的 4 个日报分类(86)、`周报`(4)，
外加 11 个只出现 1~2 次的一次性分类（`Java 性能分析`、`Kubernetes`、`实战指南`、`架构设计`…）。
基线实测（`docs/audit-baseline.md`）：

- 菜单只暴露 5 个话题分类，**只能覆盖 17.91% 的文章**（67/366）
- 8 个分类只有 1 篇文章，12 个分类不足 3 篇
- sitemap 因此包含 21 个分类页，其中多数是薄页面
- 163 篇"Claude Code / Codex / openclaw 更新"是同一条产品线的**连载**，却和日报混在同一个维度里

同时仓库内已有明确的领域词汇与决策：
`CONTEXT.md` 定义"话题（Topic）/ 话题日报"；`automation/topics/*.yaml` 为每个话题声明 `category`；
`automation/PIPELINE.md` 规定"跨话题去重时归入 AI 优先"；`docs/adr/0001` 已决定工具版本追踪并入 AI 日报、旧的 163 篇版本帖停止增长。

## 决策

1. `categories` 收敛为 **7 个稳定值**：`AI日报`、`论文日报`、`科技日报`、`股票日报`、`周报`、`工具更新`、`技术`
2. 新增 `series` taxonomy 表达**连载**：`Claude Code 更新`(81)、`openclaw 更新`(46)、`Codex 更新`(36)
3. `日报`(100) → `AI日报`（依 `PIPELINE.md` 的"AI 优先"规则）
4. 11 个一次性技术分类 → `技术`（8 篇手写长文）
5. 13 个被废弃的 term URL 生成静态跳转页（meta refresh + canonical + noindex），保证旧链接仍到达等价内容
6. 菜单同步扩到 13 项，分类入口覆盖 **366/366 = 100%**

## Considered Options

- **A. 只保留 5 个话题分类，把 163 篇工具更新并入 AI日报**：被否。语义错误（更新日志不是"日报"），
  且会让单类占 79%（291/366），分类失去区分能力；也与 ADR-0001"工具版本追踪已独立于话题日报"的记录冲突。
- **B. 保持现状 20 个分类**：被否。菜单覆盖 17.9%、8 个单篇分类，导航与内容模型脱节。
- **C. 用"话题 × 体裁"两个 taxonomy 交叉组合（如 AI×日报、AI×更新）**：被否。组合值会随话题与体裁相乘爆炸，
  且绝大多数组合为空；Hugo 的 taxonomy 更适合"少量正交维度"而不是"笛卡尔积"。
- **D. 把标签升级成分类、取消 categories**：被否。标签 59 个（35 个仅 1 次），粒度太细且不稳定，
  会重演"分类漂移"；且 term URL 大面积变更，与"不产生新 404"冲突。
- **E. 删除旧 term（不做跳转）**：被否。硬约束要求无新 404；且 GH Pages 无 301，必须靠静态跳转页兜底。

## Consequences

- **正面**：菜单入口覆盖 100%；薄分类页从 12 个降为 1 个；连载获得独立入口（`/series/`）；
  分类词表与 `automation/topics/*.yaml` 的 `category` 字段一致，未来新增话题只需加配置 + 菜单项。
- **代价**：13 个旧 term 变成 meta-refresh 跳转页（不是 301，链接权重传递弱于真 301；已用 canonical 指向新 URL 缓解）。
- **未覆盖**：面包屑仍由 PaperMod 按 section 生成（`Posts > 标题`），改成"分类 > 标题"需要 override `single.html`，
  与 P4 的 hub 页/相关文章一起做，避免两次改同一模板。
- **约束**：`series` 必须在 `hugo.yaml` 的 `taxonomies` 显式注册，否则 front matter 里的 `series` 不产生任何页面
  （本次踩过：只加 front matter 时 `/series/` 完全不生成）。
- **监测**：`scripts/audit.sh` 的 `taxonomy.categories.terms`、`single_use`、`below_threshold`、`menu_coverage.ratio`
  四项作为回归指标；任何新增一次性分类都会让 `single_use` / `below_threshold` 上升，应在 CI 里设定上限（P6）。
