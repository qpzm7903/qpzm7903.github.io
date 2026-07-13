---
title: "📄 论文日报 | 2026-07-14"
date: 2026-07-14T06:34:09+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### 1. Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading

**arXiv:** 2607.08964 | **👍 46** | 作者：Zongxia Li, Zhongzhi Li, Yucheng Shi 等

**「人话版」：** 想象你让一个 AI 助手「在终端里从零搭一个机器学习的实验并复现论文结果」。以前的考试只看最后做没做出来（及格或不及格），而做了一半或者走了歪路完全看不到。这个工作就是给 AI 出了一套更真实的考题——46 道需要几十分钟到几小时才能做完的长任务，而且每道题被拆成很多小步骤，做对一步就给一步的分。结果发现，最强的模型在「95% 以上完成度」上也只有 15.2% 的通过率，平均更低到 4.3%。这说明我们离让 AI 真正自主干长活还很远，这套题正好可以用来量进度。

**方法与亮点：** 这篇论文的核心贡献是 benchmark 本身。它把 46 个长任务分成 9 类（实验复现、软件工程、多模态分析、交互式游戏、科学计算等），每个任务都附带「参考解法或模拟器」，再细拆成细粒度子任务，从而给出 dense reward（密集奖励，意思是不只看最后及格没及格，而是每一步都打分）。这意味着你训练 agent 时有更细的梯度信号可以优化，而不只是 0/1 的稀疏奖励。论文测了 15 个前沿模型，发现平均每个任务消耗 990 万 token、跑 231 轮、85 分钟，量级上比以往的 terminal benchmark 苛刻得多。最强模型在 0.95 阈值下也只有 15.2% 通过、完美 1.0 阈值下仅 10.9%。对做 agent 与 RL（强化学习，通过试错奖励来训练模型）的人来说，这是新的「天花板测试」。

**为什么重要：** 它同时暴露了（a）当前最强 agent 在长期规划、上下文管理、迭代调试上的不足，和（b）一个可量化进步的评测阶梯。如果你的工作涉及 agent 训练、长上下文 reasoning、或工具使用评估，这几乎是必跟的 benchmark。

> **原文金句：** "Even the strongest tested model achieves 15.2% pass@1 at a partial-reward threshold of 0.95 and 10.9% at a perfect-reward threshold of 1.0, while the mean pass rate across models is 4.3% and 1.7% under the two thresholds, respectively."
>
> 译：即使最强的被测模型在 0.95 部分奖励阈值下也只拿到 15.2% 的 pass@1（一次通过率），在 1.0 完美阈值下仅 10.9%；全部模型的平均通过率分别只有 4.3% 和 1.7%。

论文链接：[arXiv: 2607.08964](https://arxiv.org/abs/2607.08964)

---

## 📄 也值得了解

### 2. Scalable Visual Pretraining for Language Intelligence

**arXiv:** 2607.09657 | **👍 41** | 作者：Yiming Zhang, Zhonghan Zhao, Wenwei Zhang 等

**「人话版」：** 现在的语言模型几乎都是用纯文本训练的——遇到带公式、图表、排版信息的 PDF 或网页时，习惯的处理是「先用 OCR 把它们抠成纯文本再喂模型」，丢掉了大量视觉线索。这篇工作说：别再抠成文本了，直接带着视觉信息训练效果更好，而且这个优势在多个骨架和 benchmark 上一致出现。

**方法与亮点：** 作者系统研究了几种 unsupervised visual pretraining（无监督视觉预训练，意思是不需要人工标注、直接从原始数据自己学）范式，直接吃视觉文档，不做文字提取。多个 baseline（基础模型架构）和 benchmark 上的结果一致：同等语料下视觉预训练 ≥ 纯文本预训练，在语言智能上也是如此。这直接挑战了「语言模型必须只看文本」的默认假设。对于做 foundation model 预训练、数据 pipeline 或 multimodal（多模态，同时处理文本与图像等）研究的人，这是一个值得重视的方向。

> **原文金句：** "Across multiple backbones and benchmarks, visual pretraining on the same underlying corpora consistently outperforms text-only pretraining, offering an efficient pathway to scalable language intelligence."
>
> 译：在多个骨架模型和基准上，基于同一语料的视觉预训练稳定优于纯文本预训练，为可扩展的语言智能提供了一条高效路径。

论文链接：[arXiv: 2607.09657](https://arxiv.org/abs/2607.09657)

### 3. Video Generation Models are General-Purpose Vision Learners

**arXiv:** 2607.09024 | **👍 40** | 作者：Letian Wang, Chuhan Zhang, Rishabh Kabra, Jasper Uijtings, Steven Waslander, Andrew Zisserman, Joao Carreira, Kaiming He, Misha Andriluka 等

**「人话版」：** NLP（自然语言处理）的「大力奇迹」来自下一个 token 预测——一个模型被喂海量文本、学着自己接话，于是就变成了能做各种任务的通用底座。视觉这边一直没找到对等的「大力奇迹」，这篇论文说：大规模「文本→视频生成」可能就是那个对等物。他们用预训练好的视频生成 diffusion（扩散模型，一类通过逐步去噪生成图像/视频的模型）骨架，改造出一个前向推理的感知模型 GenCeption，居然在深度估计、法向估计、相机位姿、表情指代分割、3D 关键点预测等多个视觉任务上都达到或超过专门的模型，而且数据效率极高——同水平性能需要的训练数据比竞争方案少 7 到 500 倍。

**方法与亮点：** GenCeption 接受文本指令来 steer（引导）输出，一个模型做多件视觉事，比 V-JEPA、Video MAE 等替代预训练范式都强。更妙的是：只在合成人像视频上训练的模型，居然 zero-shot 泛化到了真实世界的动物和机器人镜头——也就是说视频生成并不仅仅是「合成工具」，它学到的时空先验可以迁移到真实世界的感知任务。Kaiming He 等人的名字也说明这个方向值得关注。

> **原文金句：** "GenCeption exhibits preliminary data and model scaling properties along with exceptional data efficiency, where it achieves comparable performance with leading models like D4RT and VGGT-Omega with 7 to 500 less training data."
>
> 译：GenCeption 展现出初步的数据与模型 scaling 特性以及极高的数据效率——与 D4RT、VGGT-Omega 等领先模型达到相当性能时，所需的训练数据少 7 到 500 倍。

论文链接：[arXiv: 2607.09024](https://arxiv.org/abs/2607.09024)

---

## 📖 今日英语

从今日所引三篇论文的英文摘要中，挑出 5 个高频学术/技术词，供精读时对照原意理解。

### 1. Long-Horizon（长跨度 / 长时限）

> 来源：Long-Horizon-Terminal-Bench 原文——"a terminal benchmark of 46 **long-horizon** tasks spanning nine categories"

**含义：** 形容任务时间跨度很长、需要多步骤持续推进才能完成，与 one-shot / short-horizon 相对。在 AI agent 语境下特指需要数小时乃至更长、要长期规划与迭代调试的任务。

**为什么值得记：** 这几年「长跨度 agent」几乎成了行业顶层叙事之一，理解这个词就能直接读懂 API 到 paper 的标题层级。

### 2. Dense Reward（密集奖励）

> 来源：同上原文——"Each task follows a Terminal-Bench-style setup with a reference solution or simulation engine, but is further decomposed into fine-grained graded subtasks. This design enables **dense intermediate rewards** and partial credit"

**含义：** 与 sparse reward（稀疏奖励，只有最后成败才给一个奖励）相反，每走一步都给一个分数或信号，便于模型/agent 知道自己处于哪里、进度如何。

**为什么值得记：** 这是 RL 训练里反复出现的对立概念，dense vs sparse 在算法选型（如 reward shaping）中非常高频。

### 3. Unsupervised Pretraining（无监督预训练）

> 来源：Scalable Visual Pretraining 原文——"we conduct a systematic study of **unsupervised visual pretraining** paradigms that directly leverage visual documents without text extraction"

**含义：** 不依赖人工标注、让模型从原始数据中自己学到有用表示的预训练方式。典型例子包括 BERT 的 masked language model、对比学习等。

**为什么值得记：** 这是 foundation model（基础模型）时代的核心范式，几乎所有大模型的「大力奇迹」都建立在能从海量无标注数据上自监督预训练这个前提上。

### 4. Diffusion（扩散模型）

> 来源：Video Generation Models 原文——"leverages a pre-trained video generative **diffusion** backbone to define a feed-forward perception model"

**含义：** 一类生成式模型，通过「从噪声逐步去噪」的方式生成图像或视频，是目前主流的视频/图像生成技术路线之一。

**为什么值得记：** 扩散模型不是「会画图」那么简单——这篇论文展示了它的预训练骨架可以被复用做感知任务（深度、分割等），意义远超合成媒体。

### 5. Spatiotemporal Priors（时空先验）

> 来源：同上原文——"large-scale text-to-video generation serves as a strong pre-training paradigm for computer vision, providing the necessary **spatiotemporal priors**, vision-language alignment, and scalability required for general visual intelligence"

**含义：** 模型在预训练时就获得的、关于「物体在时间与空间中如何运动与变化」的内在常识，例如物体有连续轨迹、表面会随光照变化、相机运动与场景几何有规律等。

**为什么值得记：** 这是「视频生成可以当通用视觉底座」这一主张的关键论据——因为视频自带的时空一致性正好是许多视觉感知任务需要的先验知识。