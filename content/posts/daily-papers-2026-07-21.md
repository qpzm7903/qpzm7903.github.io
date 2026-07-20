---
title: "📄 论文日报 | 2026-07-21"
date: 2026-07-21T06:32:00+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### RESOURCE2SKILL：从人类多模态教程资源中蒸馏出可执行的 Agent 技能

**arXiv:** 2606.29538 | 👍 112 | 作者：Yijia Fan, Zonglin Di, Zimo Wen, Yifan Yang, Mingxi Cheng 等

论文链接：[arXiv:2606.29538](https://arxiv.org/abs/2606.29538)

**人话版**：你刚招了一个新员工（AI agent），什么都不会。你手上有一堆人类做的工作教程视频、GitHub 仓库代码、操作文章。你能不能把这些资源"喂"给这个 agent，让它自己学会这些技能？RESOURCE2SKILL 做的就是这件事——它不是让人类一条条手写技能说明，而是从教程视频、代码仓库、文章等多模态资源里自动"蒸馏"出可执行的技能，组织成一个层级化的"技能 Wiki"。每条技能条目包含结构化文本、代码、视觉示例、元数据和来源信息。

**核心方法**：框架把不同类型的资源互补起来——视频捕捉时序操作和视觉效果，代码捕捉可执行的工具调用模式，文章提供概念和风格基础。推理时，agent 按需从这个技能 Wiki 检索和组合相关技能；覆盖不足时，同一套构建操作还能在线学习新技能。在七个实际创作领域上评估，比无技能的 agent 平均提升 +11.9 个百分点，在 28 个主聚合模型-领域格子中 26 个超过强基线。

**为什么重要**：现在 AI agent 最头疼的不只是"能不能推理"，而是"没有经验可复用"。手写技能库太慢且纯文字不够用（很多操作光看文字学不会，得看视频）。这篇论文提供了一条自动化的路径：利用互联网上已有的海量人类教程资源，让 agent 自己学会做事。思路与 OpenAI 那篇安全文章（同日发布）形成互补——一边在解决"agent 怎么学会更多技能"，一边在解决"agent 学会了技能后怎么保证不用歪"。

> 原文金句：
> "Skills are a useful abstraction for software agents, turning human and agent experience into reusable procedural knowledge."
> 译：技能是软件 agent 的一种实用抽象，把人类和 agent 的经验转化为可复用的程序性知识。

## 📄 也值得了解

### RAGU：带紧凑领域适配 LLM 的多步 GraphRAG 引擎

**arXiv:** 2607.11683 | 👍 110 | 作者：Mikhail Komarov, Ivan Bondarenko, Stanislav Shtuka, Oleg Sedukhin, Roman Shuvalov 等

论文链接：[arXiv:2607.11683](https://arxiv.org/abs/2607.11683) ｜ [GitHub](https://github.com/RaguTeam/RAGU)

**人话版**：GraphRAG（图增强检索生成）是让大模型"查资料"时不只查文本，而是把文档建成知识图谱（节点是实体、边是关系），查得更准。但现有系统一次性从文档里抽取实体和关系，噪声大、容易漏。RAGU 的改进是分两步走——先抽取、再合并整合（用 DBSCAN 聚类去重、LLM 摘要、Leiden 社区检测）。

这篇论文还有一个关键发现：在 RAG 流水线内部，LLM 需要的是"理解和抽取能力"，这跟"世界知识"不完全是一回事——后者跟模型大小强相关，前者不是。所以他们训练了一个 7B 参数的 Meno-Lite-0.1 专门做抽取，在知识图谱构建上比 Qwen2.5-32B 还好（+12.5% 相对调和均值），在英文 GraphRAG 任务上打平。在医学 GraphRAG-Bench 上，RAGU 在每个事实层面检索到最完整的上下文（evidence recall 达 0.84，其他系统 ≤0.76），还为多跳问答揭示了一个现象：此前 HippoRAG2 的看似优势主要是答案格式差异导致的假象。RAGU 通过 `pip install graph_ragu` 安装，MIT 许可，单 GPU 即可运行。

> 原文金句：
> "The skills an in-pipeline LLM needs — comprehension, extraction, reasoning over context — are language skills that grow only weakly with model size, unlike factual world knowledge."
> 译：流水线内 LLM 所需的能力——理解、抽取、上下文推理——是语言技能，随模型规模增长很弱，不像事实性世界知识。

### Xiaomi-Robotics-1：用超 10 万小时真实世界轨迹训练视觉-语言-动作模型

**arXiv:** 2607.15330 | 👍 53 | 作者：Xiaomi Robotics Team（小米机器人团队）等

论文链接：[arXiv:2607.15330](https://arxiv.org/abs/2607.15330) ｜ [项目页](https://robotics.xiaomi.com/xiaomi-robotics-1.html)

**人话版**：小米出了个机器人基础模型 Xiaomi-Robotics-1，核心卖点是用 UMI 设备采集了超过 10 万小时的真实世界操作视频做训练。这比之前大多数 VLA 模型用合成数据或小规模真实数据的做法激进得多。

他们设计了一个可扩展的自动标注管线：自动给每段操作视频打上自然语言描述（场景状态如何变化），为动作学习提供丰富和精确的条件信号。训练分两阶段：预训练赋予广泛的动作生成能力，后训练对齐到机器人具体形态和人类自然语言指令。实验展示出强的 scaling（scaling 往好处走的趋势）：数据和模型变大，预训练效果持续提升，且这个趋势直接迁移到后训练——预训练越好的模型，真机泛化越好。

在 RoboCasa365 上创下新纪录 57.6%（此前最佳 46.6%），在 RoboDojo 上平均 20.07（此前 SOTA 13.07）。代码和模型检查点将开源。

> 原文金句：
> "A stronger pre-training model yields better out-of-the-box real-robot performance in unseen environments."
> 译：更强的预训练模型在未见环境中的零样本真机表现更好。

## 📖 今日英语

1. **distill**（蒸馏）— 出自 RESOURCE2SKILL 标题："**Distilling** Executable Agent Skills from Human-Created Multimodal Resources." 在 AI 里不是造酒，而是"把大模型/复杂资源的知识压缩提炼到小模型/紧凑技能里"。常见搭配：knowledge distillation（知识蒸馏）、distill into skills（蒸馏成技能）。

2. **provenance**（来源 / 出处）— 出自 RESOURCE2SKILL 摘要："metadata, and **provenance**." 指一条信息或数据的来源追溯链。在构建可信知识库时很重要——每条技能都能追溯到它来自哪个视频、哪段代码。

3. **harmonic mean**（调和平均值）— 出自 RAGU 论文："+12.5% relative **harmonic mean**." 一种平均方式，对不平衡的指标（精确率和召回率差距大时）比算术平均更严格。F1 分数就是精确率和召回率的调和平均。

4. **out-of-the-box**（开箱即用 / 零样本）— 出自 Xiaomi-Robotics-1 摘要："capable of...following diverse language instructions...in unseen environments **out-of-the-box**." 意为无需额外微调就能直接使用。在模型评估里和 zero-shot、zero-extra-training 近义。

5. **embodiment**（身体形态 / 具身体）— 出自 Xiaomi-Robotics-1 摘要："align these capabilities with robot **embodiments**." 指机器人的物理形态——是机械臂、人形机器人还是移动平台。同一套智能"大脑"装在不同 embodiment 上行为方式不同。在具身智能（embodied AI）领域是核心概念。