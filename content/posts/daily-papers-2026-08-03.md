---
title: "📄 论文日报 | 2026-08-03"
date: 2026-08-03T06:38:52+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### VideoCoCo：先写一段能运行的 Blender 程序，再把物理草图变成视频

**人话版：** 普通文生视频像让画师只看一句话就直接画完整动画，物体容易忽快忽慢、穿模或违背重力。VideoCoCo 先让“工程师”写出一段能运行的 Blender 程序，把场景和每一步运动明确演出来，再让“画师”把这份粗糙但物理过程清楚的草图润色成真实视频。

作者把可执行 Blender 代码当作过程级思维链：编码 Agent 根据文本生成程序，模拟引擎执行程序得到确定性的时空草稿，生成式视频引擎再以草稿为条件做高保真编辑。和只写不可执行计划、或只给少数中间帧的方法相比，代码能覆盖完整时间过程，也更容易检查和控制。

为让视频编辑器适应模拟草稿，团队构建了 3,000 组“草稿—指令—目标视频”数据。论文报告，VideoCoCo 把 OmniWeaving 基线在 PhyGenBench 上从 0.475 提升到 0.558，在 VBench-2.0 上从 52.18 提升到 77.88，并在两项基准的平均分上取得最佳结果。这些数字说明中间的可执行物理表示有效，但不等于 Blender 能覆盖所有真实世界动力学；复杂流体、材料和人与物交互仍取决于程序生成与模拟器能力。

**原文金句：** “These results demonstrate that executable code provides an effective, controllable, and inspectable intermediate representation for physically consistent video generation.”
**中文：** 这些结果表明，可执行代码为物理一致的视频生成提供了有效、可控且可检查的中间表示。

论文链接：[arXiv: VideoCoCo](https://arxiv.org/abs/2607.27380)

## 📄 也值得了解

### Memory Decoder at Scale：把“记忆容量”从基础模型参数里拆出来单独扩容

**人话版：** 现在的大模型像把知识和解题能力都塞在同一个脑袋里；想记得更多，往往只能把整个脑袋做大。Memory Decoder at Scale 尝试外挂一个专门负责长期记忆的参数模块，让基础模型不必同步膨胀，也能调用更多预训练知识。

作者把记忆模块扩到 69 亿参数，并在 3,000 亿 token 上预训练。因为标准 Faiss 的索引和检索成本在这个规模上不可承受，系统改用分布式索引/检索，以及按批次稀疏加载近邻概率分布。实验中，Pythia-410M 配 6.9B 通用记忆后，17 项基准平均分从 29.86 升到 37.34，略高于 Pythia-12B 的 37.24，同时总参数少 39%；Qwen3 Base 的多个规模配 1.7B 领域记忆后，三个领域平均均提升 9 分以上。这里的“参数记忆”仍会把知识编码进权重，不是可逐条编辑的数据库，因此更新成本、可解释性和事实过期仍是部署问题。

**原文金句：** “Across model scales, we find that allocating more parameters to memory yields a better parameter-performance tradeoff than scaling the base model alone.”
**中文：** 跨越不同模型规模，作者发现把更多参数分配给记忆，比只扩展基础模型能得到更好的参数—性能权衡。

论文链接：[arXiv: Memory Decoder at Scale](https://arxiv.org/abs/2607.27919)

### Beacon：视觉 Agent 不只要会用工具，还要知道何时不该用

**人话版：** 给视觉模型放大镜、裁图和搜索工具，不代表每道题都该拿工具出来；简单题乱用工具反而可能引入新错误。Beacon 的目标是让模型先判断“这题是否真的需要工具”，再在难题上选择合适动作。

论文把工具能力拆成两个维度：Mode Adaptiveness 衡量模型能否按任务需要调用工具，Tool Effect 衡量工具是否真的让原本解不了的问题变得可解，同时不伤害本来就会做的简单题。作者发现，现有视觉 Agent 在难题上获得的收益，经常被简单题上的工具误用抵消。Beacon 在强化学习阶段加入“必要性感知自适应奖励”和“提示引导能力扩展”，分别训练调用时机与困难样本上的工具能力。摘要没有给出统一的具体提升数字，因此更稳妥的结论是它提供了一套评估和训练框架，而不是宣称工具误用问题已经解决。

**原文金句：** “Tool Effect characterizes the actual impact of tool use: tools should extend the model's capabilities on problems unsolvable through text-only reasoning, while avoiding additional errors on problems that the model can already solve without tools.”
**中文：** 工具效果刻画工具使用的实际影响：工具应扩展模型解决纯文本推理无法解决问题的能力，同时避免在模型本已能解决的问题上引入额外错误。

论文链接：[arXiv: Beacon](https://arxiv.org/abs/2607.28595)

## 📖 今日英语

1. **executable code（可执行代码）**
   原句（VideoCoCo）：“These results demonstrate that executable code provides an effective, controllable, and inspectable intermediate representation for physically consistent video generation.”
   与只描述步骤的计划不同，它能被运行、测试并产生具体中间结果。
2. **parameter-performance tradeoff（参数—性能权衡）**
   原句（Memory Decoder at Scale）：“Across model scales, we find that allocating more parameters to memory yields a better parameter-performance tradeoff than scaling the base model alone.”
   比较增加多少参数能换来多少效果时的常见研究表达。
3. **Mode Adaptiveness（模式适应性）**
   原句（Beacon）：“Mode Adaptiveness characterizes whether an MLLM can recognize when tools are truly necessary and invoke them accordingly, thereby avoiding unnecessary computational overhead while improving performance on challenging problems that require tool assistance.”
   指系统能否按任务难度改变推理模式，而不是机械地每次都调用工具。
4. **additional errors（额外错误）**
   原句（Beacon）：“Tool Effect characterizes the actual impact of tool use: tools should extend the model's capabilities on problems unsolvable through text-only reasoning, while avoiding additional errors on problems that the model can already solve without tools.”
   评估工具或自动化流程时，不能只看新增收益，也要计算它引入的新失败。
