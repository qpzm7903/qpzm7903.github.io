---
title: "📄 论文日报 | 2026-07-25"
date: 2026-07-25T06:57:27+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### AREX：研究型 agent 不再“搜得更久”，而是反复检查并定向补洞

作者：Shuqi Lu、Chaofan Li、Kun Luo、Zhang Zhang 等 | 论文链接：[arXiv:2607.21461](https://arxiv.org/abs/2607.21461) | 115 票

**人话版**：让 AI 做复杂调研时，最浪费钱的方式是不断扩大搜索范围。更像人类研究员的做法是：先写一个暂定答案，把要求逐条核对，找出证据不足的句子，再只针对这些缺口继续查。AREX 把这套“写一版—审一遍—补缺口”的循环做成了研究 agent。

**方法思路**：AREX 有内外两层循环。内层负责搜索证据并形成暂定答案；外层按约束逐项审计，标出未解决主张，再启动针对性检索。为了避免长任务的上下文越积越大，模型还学会调用一个自主 context-update 工具，把历史压缩成“已核验事实 + 未解决约束”的改进状态。训练分为 agentic mid-training 和长程强化学习，并对“获得决定性证据”或“纠正错误研究方向”的关键步骤加大权重，缓解只在最终答案给奖励导致的稀疏信号问题。

团队训练了一个 4B dense 模型和一个 122B 总参数、每次激活 10B 的 [MoE](/concepts/moe/) 模型。在 BrowseComp、WideSearch、DeepSearchQA、Humanity's Last Exam 等搜索、推理与工具使用基准上，AREX 超过相近规模基线，并能与激活参数更多的模型竞争。对开发者最直接的启发是：深度研究 agent 的核心状态不应只是聊天记录，而应是持续更新的证据账本；“自我改进”也不是让模型空想，而是把检查结果变成下一轮检索目标。

> 原文金句：“AREX alternates between an inner research loop that gathers evidence and constructs a provisional answer, and an outer self-improvement loop that audits the answer constraint-wise.”
> 中文对照：“AREX 在收集证据、构造暂定答案的内层研究循环，与按约束审计答案的外层自我改进循环之间交替运行。”

## 📄 也值得了解

### SLAI T-Rex：在昇腾 SuperPOD 上做 DeepSeek-V4 全参数后训练

作者：Dongfang Li、Xiaodong Luo、Ruoyu Sun、Xuhui Chen 等 | 论文链接：[arXiv:2607.20145](https://arxiv.org/abs/2607.20145) | 56 票

**人话版**：万亿参数 MoE 模型像一座超大型工厂，真正困难的不只是“有多少芯片”，而是内存装不下、机器间传输等着算、底层算子又跑不满。SLAI T-Rex 展示了一条不依赖 GPU 集群、在昇腾 NPU SuperPOD 上把 DeepSeek-V4 系列完整后训练跑通的工程路线。

团队从模型并行、计算与通信编排、底层 kernel 三层联合优化，达到 34.22% 的模型 FLOPs 利用率（MFU），比开源基线方案提升 2.93 倍，并维持训练稳定。随后他们用 DeepSeek-V4-Flash 建立运筹优化领域的持续预训练（CPT）和监督微调（SFT）流水线，构造 1 万条经求解器核验的数据。专用模型的零样本 Pass@1 平均分达到 71.81%，比 GPT-5.4-Mini 高 3.98 个百分点，比基础 DeepSeek-V4-Flash 高 11.27 个百分点。

这篇论文的价值在于把“国产算力能不能训前沿 MoE”从单点 kernel 测试推进到完整后训练和领域模型结果：硬件利用率、训练稳定性、数据构造和最终任务指标被放在同一条链上验证。

> 原文金句：“The resulting system achieves 34.22% Model FLOPs Utilization (MFU) with a 2.93x improvement over the open-source baseline recipe while maintaining training stability.”
> 中文对照：“该系统在保持训练稳定的同时达到 34.22% 的模型 FLOPs 利用率，相比开源基线方案提升 2.93 倍。”

### ActiveVision：最强多模态模型也不太会“多看几眼”

作者：Jiarui Zhang、Muzi Tao、Shangshang Wang、Ollie Liu、Xuezhe Ma、Willie Neiswanger | 论文链接：[arXiv:2607.16165](https://arxiv.org/abs/2607.16165) | 24 票

**人话版**：人找钥匙时会先扫一眼房间，再根据“可能在桌边”的判断移动视线、放大局部、换角度确认；现在的多模态模型常常只像看了一张静态照片就开始答题。ActiveVision 专门考试模型能否根据中间判断主动决定“下一眼看哪里”。

基准包含 3 类共 17 个任务，强制模型反复感知，而不是一次描述整张图。结果差距极大：GPT-5.5 在最高公开推理档位只做对 10.6%，17 项里有 11 项得零分；Claude Fable 5 只做对 3.5%；三名人类参与者平均为 96.1%。即使允许模型自己写并运行视觉代码，大部分差距仍然存在，因为真实图像上的视觉程序并不可靠，而发现程序看错了，本身又需要模型缺少的主动观察能力。

这说明“能识图”和“会观察”不是同一件事。要让电脑使用 agent 或机器人可靠工作，训练目标需要闭合“感知—推理—再次感知”的循环，而不能只增加静态图问答数据。

> 原文金句：“Frontier MLLMs collapse on ActiveVision.”
> 中文对照：“前沿多模态大语言模型在 ActiveVision 上全面失灵。”

## 📖 今日英语

- **provisional answer** — “constructs a provisional answer”（AREX）。释义：暂定答案，允许后续核验和修改的中间版本。为什么值得记：研究和 agent 工作流里，它比直接称为 final answer 更准确。
- **constraint-wise** — “audits the answer constraint-wise”（AREX）。释义：按约束逐项检查。为什么值得记：多条件任务常用这种审计方式，避免只评估整体观感。
- **computation-communication orchestration** — “computation-communication orchestration”（SLAI T-Rex）。释义：计算—通信编排，让计算与跨设备数据传输尽量重叠。为什么值得记：分布式训练性能瓶颈常常不是算力，而是等待通信。
- **active observation** — “this active observation is essential for a wide range of tasks”（ActiveVision）。释义：主动观察，根据中间判断决定下一步看哪里。为什么值得记：它是视觉 agent 区别于静态图像问答的核心能力。
