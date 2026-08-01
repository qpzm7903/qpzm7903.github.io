---
title: "📄 论文日报 | 2026-08-02"
date: 2026-08-02T06:37:19+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### Frontis-MA1：让 AI 不只写模型代码，还反复改进“造 AI 的流程”

**人话版：** 想象让一个程序参加机器学习比赛：它先写方案，运行后看分数，再定位错误、组合旧方案并继续改，直到时间用完。Frontis-MA1 研究的不是“一次写出最好代码”，而是怎样让 AI 把这套试验—反馈—改进循环本身做得越来越好。

作者把这类能力称为 AI4AI，并开放 OpenMLE 全栈：OpenMLE-Gym 提供能真实执行和打分的任务环境，OpenMLE-RL 用运行反馈训练四种原子操作——起草、改进、调试和交叉组合，OpenMLE-Evo 再把这些操作编成长流程搜索。35B 参数的 Frontis-MA1 在训练和推理时使用同一组操作，减少“训练学一种动作、部署却换另一套搜索流程”的断层。

在 MLE-Bench Lite 上，每项任务限制 12 小时、单张 RTX 4090 且显存封顶 12GB。基础模型的 Medal Average 为 39.39%，接入 Frontis-MA1 与 OpenMLE-Evo 后升至 60.61%；再加入与基准无关的经验先验和异步搜索后达到 71.21%。作者称它超过 GPT-5.5 + Codex，并接近 GPT-5.6 Sol 与 2.8T 参数的 Kimi K3，但这些是论文设定下的结果，不能等同于通用开发能力排名。

迁移实验把“模型”和“搜索框架”的贡献拆开：在未参与训练的 NatureBench Lite 上，固定框架只替换模型，Match-SOTA 从 50% 升到 70%；固定模型只替换搜索框架，则从 20% 升到 50%。这说明改进不只来自更会写代码的模型，也来自如何组织长时间试验。模型权重与完整 OpenMLE 栈均已开放，便于复现实验。

**原文金句：** “We release the model weights and the full OpenMLE stack to enable reproducible research on executable AI4AI toward RSI.”
**中文：** 我们开放模型权重和完整 OpenMLE 栈，以支持面向递归自我改进、可执行且可复现的 AI4AI 研究。

论文链接：[arXiv: Frontis-MA1](https://arxiv.org/abs/2607.28568) ｜ [代码](https://github.com/FrontisAI/OpenRSI)

## 📄 也值得了解

### PhiZero：先用“物理语言”推演世界，再把结果渲染成视频

**人话版：** 普通视频模型像直接猜下一帧像素，画面可能漂亮，却不一定说得清物体为什么这样运动。PhiZero 先把世界变化翻译成一串紧凑的“物理语言”，像先写动作分镜和因果步骤，再根据这份推演生成视频。

现有世界模型通常直接在高维像素空间预测未来，因此运动规律藏在庞大的视觉网络里。PhiZero 从自然视频中用自监督方法学习离散的世界状态变化表示，并采用 `reason-then-render`：先预测未来如何演化的物理语言序列，再把这些转换渲染成视频。

作者报告，它在生成与理解基准上能保持更连贯的物理演化，并展示了交互式世界建模、精细动作条件模拟和零样本运动迁移的潜力。摘要没有给出足以独立判断优势幅度的统一数字，因此更稳妥的解读是一个架构方向：把隐式像素预测拆成可推理的中间表示，而不是据此宣称已经解决通用物理模拟。

**原文金句：** “PhiZero adopts a reason-then-render paradigm: it first infers future world evolution as a physical-language sequence and then renders the inferred transitions into videos.”
**中文：** PhiZero 采用“先推理、后渲染”范式：先把未来世界演化推断成物理语言序列，再将这些变化渲染为视频。

论文链接：[arXiv: PhiZero](https://arxiv.org/abs/2607.28624) ｜ [项目页](https://phi-zero.github.io/)

### DistillAlign：视频蒸馏不能只追求“看起来好”，还要保住结果的多样性

**人话版：** 把大视频模型压缩成小模型，像让学生模仿老师画很多不同场景。如果只奖励最像老师佳作的结果，学生会反复画少数安全模板，看起来精致却越来越单一。DistillAlign 试图让学生既画得准，也别忘掉老师会画的其他可能性。

论文指出，常见的分布匹配蒸馏（DMD）多阶段流程存在目标错位：初始化阶段和后续 DMD 优化追逐不同分布，中间模型却主要按 VBench 等视觉分数判断。作者在共享潜空间中同时测量 precision 与 coverage，发现有些初始化精度高但覆盖率低，后续很难恢复被丢掉的模式。

即使初始化与教师目标已经对齐，DMD 的 reverse-KL 目标在训练后期仍会把学生推向教师分布的高概率区域，继续牺牲覆盖和多样性。论文因此加入 consistency distillation 的 mode-covering 约束，与 DMD 的 mode-seeking 目标联合训练。这里的 `mode` 可以理解成数据分布里一种稳定的生成方式或场景类型。

作者称，在 Wan-1.3B DMD 教师下，联合方案也能超过使用 Wan-14B 教师精炼的基线，说明分布目标的协调可能比单纯换更大教师更重要。不过这一结论仍依赖其评测协议与视频数据，需在更多模型家族上复现。

**原文金句：** “A good initialization should match the mode coverage of the target DMD teacher, rather than merely pursuing high quality.”
**中文：** 好的初始化应匹配目标 DMD 教师的模式覆盖，而不只是追求高视觉质量。

论文链接：[arXiv: DistillAlign](https://arxiv.org/abs/2607.26811) ｜ [项目页](https://lijiaxing0213.github.io/DistillAlign)

## 📖 今日英语

1. **recursive self-improvement（递归自我改进）**
   原句（Frontis-MA1）：“Recursive self-improvement (RSI) requires AI systems that improve the process of building AI.”
   不只是完成任务，而是改进“如何构建和改进系统”的过程；AI4AI 讨论中的核心短语。
2. **execution feedback（执行反馈）**
   原句（Frontis-MA1）：“We introduce OpenMLE, an open full-stack system for RSI research in MLE, spanning verifiable task environments with execution feedback...”
   指通过真正运行程序得到测试、分数或错误，而非只靠语言评价。
3. **reason-then-render（先推理、后渲染）**
   原句（PhiZero）：“PhiZero adopts a reason-then-render paradigm...”
   用来描述先生成结构化中间过程、再生成最终视觉结果的两阶段设计。
4. **mode coverage（模式覆盖）**
   原句（DistillAlign）：“A good initialization should match the mode coverage of the target DMD teacher, rather than merely pursuing high quality.”
   生成模型中表示能否覆盖数据分布里的多种有效形态，常与多样性和 mode collapse 一起出现。
