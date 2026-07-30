---
title: "🌐 科技日报 | 2026-07-31"
date: 2026-07-31T06:34:36+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. GitHub 原生支持 stacked pull requests：大改动可拆层审、一次合并

GitHub 宣布 stacked pull requests 进入公开预览。所谓 stack，是一组有顺序依赖的 pull request：每一层只承载一个小而聚焦的改动，并把下一层建立在上一层之上。审核者可以只查看当前层的 diff，也能从 stack map 看到它在整个改动中的位置。

过去团队要么提交一个难审的大 PR，要么维护多条需要反复 rebase 的分支。新功能允许多名审核者并行审不同层，并继续沿用已有的 branch protection、检查和合并要求；团队可选择合并一层、若干层，或一次落地主栈。

创建 stack 可通过官方 `gh-stack` CLI 扩展，也可以在 GitHub 网页、移动端或支持该 skill 的编程 Agent 中操作。功能将逐步开放给所有仓库，merge queue 支持则在未来数周渐进推出。

它对 AI 编程时代尤其重要：代码生成速度提高后，人工评审往往成为新瓶颈。把大改动拆成依赖有序的小块，既保留端到端目标，也能让每次审查更短、更准确。

**原文金句：** “Stacked pull requests break large changes into small, reviewable pull requests.”
**中文：** 堆叠式拉取请求把大型改动拆成小而可审查的拉取请求。

[GitHub Changelog：Stacked pull requests are now in public preview](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/)

### 2. IBM 公布三项可验证“量子优势”实验：不只算得快，还要证明结果可信

量子计算声称超越经典计算时有一个悖论：如果经典计算机已经算不动，又该怎样确认量子答案正确？IBM 与多所机构公布三篇工作，把验证机制嵌进计算过程，而不是只依赖更小问题上的外推。

IBM 与芝加哥大学使用掺杂 Clifford 采样和时空码：在本来容易模拟的 Clifford 电路中加入让经典模拟变难的 T 门，同时用辅助量子位跨空间和时间检查错误。官方称，70 个逻辑量子位的计算把有效门错误降低约 10 倍，并能为难以经典模拟的逻辑计算给出保真度下界。

Qedma、RIKEN 与 BlueQubit 的实验在最多 74 个量子位上观察到经典模拟未捕捉的持续振荡，再用独立误差缓解方法和另一套 Quantinuum 硬件复核。Algorithmiq 则在五种不同噪声配置上寻找一致结果，并用带误差条的无偏估计验证过程。

这些结果仍会进入 Quantum Advantage Tracker，接受更好的经典算法持续挑战。价值不在于宣布经典计算“结束”，而在于把量子优势的门槛从“经典机暂时跟不上”提高到“计算过程提供可审查的可靠性证据”。

**原文金句：** “Announcing quantum advantage does not close the case—it opens the results to a new level of scrutiny.”
**中文：** 宣布量子优势并不会结案，而是把结果交给更高层级的审视。

[IBM 原文：Quantum advantage through trusted quantum computation](https://www.ibm.com/quantum/blog/quantum-advantage)

## 📰 快讯

### Apple 创下最强六月季度，营收同比增长 16%

Apple 公布 2026 财年第三季度营收 1,094 亿美元，同比增长 16%；毛利率 50.1%，稀释后每股收益 2.02 美元，同比增长 29%。公司称 iPhone、Mac 与服务业务均创六月季度收入纪录，但毛利率包含关税退款带来的约 2 个百分点正面影响，比较经营趋势时不能忽略这一一次性因素。

[Apple Newsroom：Apple reports third quarter results](https://www.apple.com/newsroom/2026/07/apple-reports-third-quarter-results/)

## 📖 今日英语

1. **reviewable（可审查的）**
   原句（GitHub）： “Stacked pull requests break large changes into small, reviewable pull requests.”
   常见于代码、设计稿和文档流程，强调规模已经小到可以认真检查。
2. **rigorously validated（经过严格验证）**
   原句（IBM）： “A quantum advantage occurs when a quantum computer performs a computation beyond what classical computing can achieve alone—and when the result can be rigorously validated.”
   科研报道中比 simply tested 更强，强调方法和证据经得起审查。
3. **pressure test（压力检验）**
   原句（IBM）： “These three experiments live alongside other advantage candidates on the Quantum Advantage Tracker for the broader community to further pressure test.”
   可用于技术方案、商业假设或政策，指主动寻找薄弱点。
4. **year over year（同比）**
   原句（Apple）： “The Company posted quarterly revenue of $109.4 billion, up 16 percent year over year.”
   财报最常见的时间比较方式之一，缩写为 YoY。
