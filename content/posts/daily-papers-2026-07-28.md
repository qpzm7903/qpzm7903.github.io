---
title: "📄 论文日报 | 2026-07-28"
date: 2026-07-28T06:36:10+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### DataPrep-Bench: Benchmarking LLMs as Training Data Preparators

**人话版**：做 AI 训练数据很像备菜——不只要把原料洗净切好，还要在真正下锅前判断哪批食材值得用。过去大家分别评“会不会生成数据”或“会不会给数据打分”，很少用同一把尺子验证这些数据最后能否真正把模型训好。DataPrep-Bench 把任务拆成数据构造与质量评估两条赛道，并在六个领域、多个基础模型上统一以训练后的下游表现为依据。作者还发布 Data-Construction-Skill，让 Agent 按技能流程把原始材料变成监督数据；在 Llama-3.1-8B 的金融任务上，它相对只用 Dolly-15k 的基线提高近 20 个绝对分。另一项 Distributional Alignment Score 用候选数据与领域代理数据的分布差异判断价值，在六个领域中的四个取得最强跨模型相关性，并在数学、科学和医学同时超过 0.70。它的重要性在于阻止评测停留在“文字看起来干净”：真正的质量定义被拉回“拿它训练后，模型是否更有用”。Hugging Face Daily Papers 本次抓取获得 38 票。

- 作者：Hao Liang、Qifeng Cai、Yibo Lin、Jianzhuo Du 等
- 论文链接：[arXiv:2607.20465](https://arxiv.org/abs/2607.20465)

> **原文金句**：“Quality refers to downstream training utility rather than surface-level textual properties.”
>
> 中文：质量指下游训练效用，而不是表层文本属性。

## 📄 也值得了解

### Show, Don't Tell: Evaluating Spatial Cognition in Generative Pixels Rather Than LLM Text

**人话版**：问模型“目标在哪里”时，逼它报坐标就像让人不用手指、只用数字描述地图位置；能直接在图上圈出来的图像模型因此吃了表达方式的亏。ProVisE 让图像生成模型按约定直接画点、区域或路径，再把这些像素答案解析成原基准可评分的结构化结果。作者同时构建 SpatialGen-Bench，包含 470 个样本、14 类空间子任务和四个能力层级，并用 Agent 自动构建和校验新任务协议。结果显示，图像生成模型在可直接用像素表达的空间任务上具有竞争力，而文本输出的视觉语言模型在组合式空间推理上仍明显领先。价值不在于宣称谁全面胜出，而是揭示评测接口本身会偏向某类模型。Hugging Face Daily Papers 本次抓取获得 35 票。

- 作者：Xu Wang、Kaixiang Yao、Miao Pan、Xiaohe Zhou 等
- 论文链接：[arXiv:2607.21072](https://arxiv.org/abs/2607.21072)

> **原文金句**：“Results show that image-generation models are competitive when spatial answers can be externalized directly in pixel space.”
>
> 中文：当空间答案能直接在像素空间中表达时，图像生成模型具有竞争力。

### SANA-Video 2.0: Hybrid Linear Attention with Attention Residuals for Efficient Video Generation

**人话版**：生成长视频时，普通注意力像让每一帧都和所有其他帧两两开会，视频越长，会议成本增长得越快。SANA-Video 2.0 用线性注意力承担大部分信息混合，每隔一段插入一次完整 softmax 注意力作为“校准会”，比例为 3:1；Attention Residuals 再把校准后的信息送到更深层。模型有 5B 与 14B 两档，目标是在单卡上生成最高 720p 视频。论文报告 5B 模型在单张 H100 上以 40 步采样生成 480p 的 VBench 得分为 84.30、耗时 13.2 秒；编译后的 720p/60 秒 DiT 前向比匹配的全 softmax 基线快 3.2 倍。叠加内核融合、缓存和稀疏注意力后，官方还报告 720p/5 秒管线用时 13.06 秒。数字来自论文设定，但它清楚展示了“偶尔做昂贵全局校准”如何换取视频长序列效率。Hugging Face Daily Papers 本次抓取获得 34 票。

- 作者：Junsong Chen、Jincheng Yu、Yitong Li、Shuchen Xue、Haozhe Liu 等
- 论文链接：[arXiv:2607.21553](https://arxiv.org/abs/2607.21553)

> **原文金句**：“Our hybrid design recovers softmax-level expressiveness at substantially reduced cost.”
>
> 中文：我们的混合设计以显著更低的成本恢复了 softmax 级别的表达能力。

## 📖 今日英语

- **downstream training utility** — DataPrep-Bench 原句：“quality refers to downstream training utility rather than surface-level textual properties.” 释义：下游训练效用。为什么值得记：数据论文里 `downstream` 指最终要服务的后续任务。
- **shared candidate pool** — DataPrep-Bench 原句：“scoring functions are scored by Pearson correlation with downstream performance on a shared candidate pool.” 释义：共享候选池。为什么值得记：强调不同方法在同一批样本上公平比较。
- **answer-interface mismatch** — ProVisE 原句：“existing spatial reasoning benchmarks usually require coordinates, options, or text, creating an answer-interface mismatch.” 释义：答案与接口不匹配。为什么值得记：不仅适用于 AI 评测，也适用于 API 和交互设计。
- **quality-efficiency trade-off** — SANA-Video 2.0 原句：“25% softmax as the optimal quality-efficiency trade-off.” 释义：质量与效率之间的权衡。为什么值得记：`trade-off` 是工程论文解释折中方案的高频词。
