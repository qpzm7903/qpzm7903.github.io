---
title: "📄 论文日报 | 2026-07-10"
date: 2026-07-10T09:00:00+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### Single-Rollout Asynchronous Optimization for Agentic Reinforcement Learning

**论文链接：** [arXiv:2607.07508](https://arxiv.org/abs/2607.07508) ｜ [HF Daily Papers](https://huggingface.co/papers/2607.07508)

这篇论文解决了大模型 Agent RL 训练中的两个工程痛点：同步 RL 对长时程 agentic 任务效率极低、异步 RL 又面临训练不稳定和 off-policy 偏差。作者提出 SAO（Single-rollout Asynchronous Optimization），将 GRPO 的 group-wise 采样替换为每个 prompt 仅一次 rollout，配合 value model 训练和双边界 token 级 clipping 策略来抑制 off-policy 偏差并稳定优化。SAO 能稳定训练上千步，在 SWE-Bench Verified、BeyondAIME、IMOAnswerBench 等 agentic 编码和推理基准上持续超越 GRPO 及其变体。

对工程师最值得关注的是：SAO 已实际部署在开源 GLM-5.2 模型（750B MoE-A40B）的 agentic RL 训练管线中——这意味着它不是实验室方法，而是经过了大规模训练验证的生产级方案。如果你正在做 LLM 后训练、尤其需要异步 RL 来提高长时程 agent 任务的吞吐，SAO 直接给你提供了可复用的优化框架。

## 📄 精选论文

### Sparse Delta Memory: Scaling the State of Linear RNNs through Sparsity
[arXiv:2607.07386](https://arxiv.org/abs/2607.07386) ｜ [HF](https://huggingface.co/papers/2607.07386)

面向线性 RNN 架构的显式记忆扩展。作者提出 Sparse Delta Memory（SDM），将 Gated DeltaNet 中的稠密 key-value 外积替换为对大容量显式记忆的稀疏读写，在不增加参数、等 FLOP 约束下将隐藏状态容量放大数个数量级。对需要极长上下文 recall 的工程场景（如长文档检索、长对话记忆）有直接参考价值。

### AgentLens: Production-Assessed Trajectory Reviews for Coding Agent Evaluation
[arXiv:2607.06624](https://arxiv.org/abs/2607.06624) ｜ [HF](https://huggingface.co/papers/2607.06624)

针对代码 Agent 评估的 benchmark。不同于传统只看 pass/fail 单比特结果，AgentLens 评估 agent 的完整轨迹质量——指令遵循、工具使用、自我验证、错误恢复、和用户沟通。将形式化验证与 LLM 轨迹评论结合，每个 run 产出可读的解释。不仅用于模型排名，还能诊断行为、比较 agent 版本迭代、捕捉产品回归。

### SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review
[arXiv:2607.06065](https://arxiv.org/abs/2607.06065) ｜ [HF](https://huggingface.co/papers/2607.06065)

为 AI 生成 PR 补上 code review 环路。给定一个 issue 和 AI 生成的 PR，reviewer agent 探索仓库、判断 PR 是否应该接受、并产出结构化修订反馈。配套 SWE-Review-Bench 评估审查正确性和下游修订效果，同时开源 SWE-Review-Traj 轨迹数据集填补 reviewer 训练数据缺口。对正在搭建"Agent 自动提交 + 自动审查"闭环的团队有直接参考价值。

### TurnOPD: Making On-Policy Distillation Turn-Aware for Efficient Long-Horizon Agent Training
[arXiv:2607.05804](https://arxiv.org/abs/2607.05804) ｜ [HF](https://huggingface.co/papers/2607.05804)

针对长时程 agentic 任务中 on-policy distillation（OPD）效率低的问题。作者发现全时程 rollout 在尾部 turn 上浪费大量 wall-clock 资源且 KL 监督信号弱噪声大，trajectory 级 KL 目标又让 loss 集中在浅层 token。TurnOPD 提出两个 turn 级预算控制器，按 turn 分配蒸馏预算，让深层决策 turn 得到充分训练。对需要蒸馏 agent 模型又不想被长时程拖垮算力的场景有工程参考价值。

### HunyuanOCR-1.5: Making Lightweight OCR VLMs Faster and Better
[arXiv:2607.04884](https://arxiv.org/abs/2607.04884) ｜ [HF](https://huggingface.co/papers/2607.04884)

腾讯混元团队的轻量端到端 OCR VLM。在 1.0 架构上不做 backbone 重设计，而是通过将 DFlash 适配到 OCR 解码来优化长结构化输出（密集文档、表格、公式）的推理延迟——Transformer 推理加速 6.37 倍，vLLM 下加速 2.14 倍，成为轻量级 OCR VLM 中推理最快的方案。统一了文档解析、文字 spotting、信息抽取、文图翻译和多图文档理解。