---
title: "📄 论文日报 | 2026-07-31"
date: 2026-07-31T06:34:36+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### TurboVLA：不到 1GB 显存，让机器人模型在 RTX 4090 上跑到 32Hz

**人话版：** 传统机器人 AI 像是先把摄像头看到的画面“翻译成大模型能读的内心语言”，再决定手怎么动；每动一下都要经过大模型，既慢又吃显存。TurboVLA 尝试让视觉和文字指令直接会合，然后交给一个小型动作解码器，不再把大语言模型放在每次动作的必经之路上。

论文把常见的“视觉 → 大语言模型 → 动作”路径改成“视觉 + 语言 → 动作”。视觉观察与文字指令分别编码，再通过轻量双向交互形成与任务相关的表示，最后一次预测一小段连续动作。这样保留了语言条件，又显著削减每次控制调用的计算和内存负担。

在 LIBERO 机器人操作基准上，0.2B 参数的 TurboVLA 报告平均成功率 97.7%；在消费级 RTX 4090 上，单次推理延迟 31.2 毫秒、显存 0.9GB。32Hz 意味着系统每秒可重新决定动作约 32 次，比“想很久再动一下”更接近实时控制。

这篇论文的重要性在于挑战了“机器人动作必须经过大语言模型中央接口”的默认设计。结果仍来自标准基准而非长期真实部署，但若能在更多机器人和复杂环境复现，小模型就可能承担低延迟控制，大模型只在高层规划时介入。

**原文金句：** “On LIBERO, TurboVLA achieves 97.7% average success with only 0.2B parameters, 31.2 ms inference latency, and 0.9 GB inference VRAM on a consumer-grade RTX 4090.”
**中文：** 在 LIBERO 上，TurboVLA 仅用 2 亿参数，就在消费级 RTX 4090 上取得 97.7% 平均成功率、31.2 毫秒延迟和 0.9GB 推理显存占用。

论文链接：[arXiv: TurboVLA](https://arxiv.org/abs/2607.27205)

## 📄 也值得了解

### CodeNib：给编程 Agent 准备一套可复用的代码仓库“索引服务”

**人话版：** 编程 Agent 每次接任务都像新员工重新翻仓库：搜关键词、找定义、记住刚看过的文件。CodeNib 把这些重复劳动做成按 commit 保存的多套“地图”，仓库变化时只更新该更新的部分，再按任务给 Agent 提供有限且相关的上下文。

系统同时维护词法、向量和代码结构视图，并把结果统一映射到仓库相对路径与源码范围。它明确区分不同索引在编辑后的有效边界，而不是假设所有缓存永远正确；搜索、符号跳转和受限上下文都由同一运行时提供。

在 100 个仓库快照上，当增量结果与独立重建一致时，图与向量视图的中位更新速度分别快 8.7 倍和 25.4 倍。五个模型的实验中，选定的上下文策略在保持代码定位能力的同时，比成对的 grep/read 轨迹少用 50%—87% token。它关注的不是再造一个更聪明的模型，而是降低 Agent 反复“重新认识仓库”的成本。

**原文金句：** “CodeNib builds reusable lexical, dense, and structural views per repository commit.”
**中文：** CodeNib 为每个仓库提交构建可复用的词法、稠密向量与结构视图。

论文链接：[arXiv: CodeNib](https://arxiv.org/abs/2607.25431)

### CoRT：把整段回答的奖励，重新分到真正有功劳的 token 上

**人话版：** 老师给一篇作文总分 85，但模型训练还想知道究竟哪句话写得好。许多强化学习方法把同一个总分平均广播给回答中的每个 token，CoRT 则通过一次“拿掉评分标准再重放”的对照，估计哪些 token 真正响应了规则。

CoRT 面向带 rubric（明确评分标准）的 GRPO 训练。它用原始评分提示和去掉评分标准的匹配提示，对同一回答重新计算 token 概率；两者的差异被当成 token 对 rubric 依赖程度的代理，再用于重新分配整段回答的正负优势值。这里的“优势值”可以理解为这次回答比基线好或差多少。

方法不需要额外训练 token 打分器，也不改变最终整段奖励。作者报告，在不同指令模型和奖励粒度实验中，CoRT 在绝大多数配对比较里优于普通回答级 GRPO，平均提升 4.4 个百分点。它提供了一条较省事的细粒度“功劳分配”路线，但效果仍取决于去除 rubric 后的对照提示是否真的匹配。

**原文金句：** “Experiments across instruction-tuned models and reward granularities show that CoRT improves over matched response-level GRPO in the vast majority of comparisons, with an average gain of 4.4 percentage points.”
**中文：** 在不同指令模型与奖励粒度上，CoRT 在绝大多数比较中优于匹配的回答级 GRPO，平均提升 4.4 个百分点。

论文链接：[arXiv: CoRT](https://arxiv.org/abs/2607.25659)

## 📖 今日英语

1. **inference latency（推理延迟）**
   原句（TurboVLA）： “On LIBERO, TurboVLA achieves 97.7% average success with only 0.2B parameters, 31.2 ms inference latency, and 0.9 GB inference VRAM.”
   部署论文的核心指标，常与 throughput、memory、real-time 搭配。
2. **lifecycle costs（全生命周期成本）**
   原句（CodeNib）： “Disconnected indexes, language servers, and task-local histories force repeated discovery and obscure lifecycle costs.”
   不只看一次请求，而是计算创建、更新、查询与失效处理的总成本。
3. **bounded context（有边界的上下文）**
   原句（CodeNib）： “CodeNib ... serves ranked search, symbol navigation, and bounded context through one runtime.”
   Agent 系统里常指受 token 或范围限制、经过筛选的上下文。
4. **credit allocation（功劳分配）**
   原句（CoRT）： “These results suggest that policy-internal counterfactual likelihood contrasts provide an effective training signal for within-response credit allocation.”
   强化学习高频概念，讨论怎样把最终成败归因到中间动作或 token。
