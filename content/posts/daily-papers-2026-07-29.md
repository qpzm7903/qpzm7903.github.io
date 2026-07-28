---
title: "📄 论文日报 | 2026-07-29"
date: 2026-07-29T06:36:58+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### JarvisHub: An Open Harness for Canvas-Native Multimodal Creative Agents

**人话版**：现在的创作 Agent 很像只记得当前聊天窗口的助手——它能生成一张图或一段视频，却容易忘记前面的草稿、失败版本和“这个素材从哪里来”。JarvisHub 把可编辑画布同时当成用户工作区、Agent 的外部记忆和共享项目状态，让图片、视频、音频、UI、版本、依赖和反馈都变成带类型的节点与连线。系统由画布状态、协议桥接和 Agent 运行时三层组成，Agent 的计划、工具动作与修改结果因而可以被人检查和干预。这样，创作不必被压成一条线性对话，用户也不必事先手工画出完整节点工作流。论文的贡献主要是开放[执行支架（harness）](/concepts/harness/)与状态表达，而不是宣称某个生成模型画得更好。它要回答的是长期多模态项目如何持续积累上下文、恢复失败并保持版本关系。论文给出 15 页与 9 幅图，并开放项目页和代码；Hugging Face Daily Papers 本次抓取获得 102 票。

- 作者：Yunlong Lin、Zixu Lin、Zhaohu Xing、Biqiang Li、Chenxin Li 等
- 论文链接：[arXiv:2607.23588](https://arxiv.org/abs/2607.23588)

> **原文金句**：“JarvisHub treats an editable canvas as the user workspace, the agent's external memory, action space, and shared project state.”
>
> 中文：JarvisHub 把可编辑画布同时视为用户工作区、Agent 的外部记忆、行动空间与共享项目状态。

## 📄 也值得了解

### From Proprietary to Open-Source: Bridging the Distribution Gap via Multi-Agent Protocol Distillation in Agentic Search

**人话版**：想让小型开源模型学习闭源强模型的搜索思路，就像请名厨教徒弟：看不到秘方中的内部概率，只照抄成品文字又容易学到口头禅而非做菜方法。MAPD 先让离线多 Agent 系统拆题、检索证据和修复失败，再把过程压成风格统一的 JSON 协议，记录任务类型、推理计划和可摘录证据。训练时，只有学生模型的“特权分支”看到该协议，它产生的 token 分布提供密集的[知识蒸馏](/concepts/distillation/)信号，同时普通分支继续接受只看最终答对与否的强化学习信号。这样既绕开闭源模型 logits 不可见和 tokenizer 不一致，也减少直接模仿自然语言轨迹造成的文风漂移。七个问答基准上，论文报告 Qwen3-1.7B 平均成功率 39.4%，Qwen3-4B 为 44.4%，并称对不同闭源教师都能泛化。关键意义是把“老师怎么搜”转成结构化中间协议，而非逼学生复刻老师的措辞。Daily Papers 本次抓取获得 64 票。

- 作者：Junlin Liu、Jiangwang Chen、Zixin Song、Shuaiyu Zhou、Chunji Lv 等
- 论文链接：[arXiv:2607.24280](https://arxiv.org/abs/2607.24280)

> **原文金句**：“Raw natural language trajectory imitation transfers superficial stylistic artifacts rather than core reasoning competence.”
>
> 中文：直接模仿自然语言轨迹，传递的是表面文风痕迹，而不是核心推理能力。

### Rethinking Classifier-Free Guidance in On-Policy Diffusion Distillation

**人话版**：扩散模型常把“我要的方向”和“不要的方向”组合后再生成，就像把油门与刹车的最终合力当成唯一成绩。若训练只要求合力一致，学生可能用更大的油门错误抵消更大的刹车错误，看起来总结果正确，两个分支却各自走偏。论文指出，在线策略扩散蒸馏直接匹配组合后的 classifier-free guidance（CFG）速度时，正负分支误差可能互相补偿；当教师负分支掌握学生看不到的信息时，这种问题尤其明显。作者把它称为 Negative Branch Asymmetry，并提出 Positive–Direction Matching：分别约束正向预测和 CFG 条件方向，不让两个错误彼此遮掩。在稠密控制信号蒸馏成稀疏视频控制的实验中，普通目标对推理时 guidance scale 很敏感，而分支感知监督更稳定。它提醒工程师，最终输出对齐不等于内部组成正确，蒸馏目标必须与推理结构一致。Daily Papers 本次抓取获得 61 票。

- 作者：Bingnan Li、Haozhe Wang、Haozhong Xiong、Fangtai Wu、Jinpeng Yu 等
- 论文链接：[arXiv:2607.24731](https://arxiv.org/abs/2607.24731)

> **原文金句**：“Positive- and negative-branch errors can compensate in the guided prediction.”
>
> 中文：正分支与负分支的误差可以在引导后的预测中相互抵消。

## 📖 今日英语

- **evolving project state** — JarvisHub 原句：“References, drafts, alternatives, edits, failed attempts, version relations, tool actions, evaluation signals, and human feedback ... form an evolving project state.” 释义：持续演化的项目状态。为什么值得记：适合描述设计稿、代码库和 Agent 长任务中不断积累的上下文。
- **style-normalized protocol** — MAPD 原句：“We propose Multi-Agent Protocol Distillation (MAPD), a joint distillation and RL framework uses a structured, style-normalized protocol as an intermediate representation.” 释义：风格归一化协议。为什么值得记：`normalized` 常表示把不同来源转成统一可比较格式。
- **sparse supervision** — MAPD 原句：“Outcome-based reinforcement learning (RL) provides only sparse supervision.” 释义：稀疏监督，即反馈少且通常只在任务末尾出现。为什么值得记：Agent 训练、奖励设计和长流程评测里都很常见。
- **under-identified** — PDM 原句：“We show that this objective is under-identified at the branch level.” 释义：约束不足以唯一确定内部解。为什么值得记：统计建模和优化论文用它说明“结果对，但内部变量仍有多种解释”。
