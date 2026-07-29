---
title: "AI 论文日报 2026-07-30"
date: 2026-07-30T06:39:03+08:00
draft: false
tags: ["AI", "论文", "机器学习", "日报"]
categories: ["日报"]
summary: "今日必读 Kimi K3 技术报告；另看仅凭高保真 UMI 数据部署机器人策略，以及用相关性先验引导语料库交互的 RARG 搜索代理。"
---

## 今日必读

### Kimi K3：开放前沿智能模型的系统报告

**作者：** Kimi Team 等 300 余位作者  
**论文链接：** [arXiv:2607.24653](https://arxiv.org/abs/2607.24653)

Kimi K3 是一个 2.8T 总参数、104B 激活参数的 MoE 模型，原生支持视觉与 100 万 token 上下文。其架构把 Kimi Delta Attention、Attention Residuals 与 Stable LatentMoE 组合起来：896 个路由专家中每个 token 激活 16 个。作者称，相比 Kimi K2，整体 scaling efficiency 提升约 2.5 倍。

这篇报告值得读的地方不只是参数规模，而是训练系统与长程智能体训练的共同设计。团队描述了平衡专家并行、内存管理、百万 token agentic RL 的持久 rollout 和 sandbox 状态，以及部署侧优化。后训练同时覆盖通用、编程、智能体与不同 reasoning effort，目标是让复杂任务组合与长程执行更稳。

论文没有回避边界：作者写明总体表现仍落后于最强闭源模型。与此同时，团队开放完整权重，为第三方复现实验、检查基准选择与测试长上下文行为提供了条件。

> “We release the full Kimi K3 model weights to facilitate future research.”

## 也值得了解

### HiFi-UMI：不用真实机器人后训练，也能部署操作策略

**作者：** Yuteng Wei、Jinming Ma、Jiawei Wang 等  
**论文链接：** [arXiv:2607.25895](https://arxiv.org/abs/2607.25895)

机器人操作数据长期在“高保真但昂贵的遥操作”和“便宜可扩展但误差较大的无机器人采集”之间取舍。HiFi-UMI 把重点放在提高后者的采集质量：头戴式离线双目惯性 SLAM、原生双夹爪相对位姿、微秒级 GPIO 同步，以及每只手约 200° 视野的双广角相机。

系统在不依赖外部追踪基础设施时达到 3 mm 工作区局部末端精度。只用 HiFi-UMI 演示做后训练的策略可直接部署到真实机器人；最强策略在精密插入任务上达到 85% 成功率。团队还开放 2,000 小时 HiFi-UMI-2K 数据集，并报告用同一体系 4,000 小时预训练后，十项未见任务的动作误差下降 41%。

### RARG：让相关性不只负责检索，还直接指导 grep 顺序

**作者：** Yuqing Li、Zexue He、Julian McAuley 等  
**论文链接：** [arXiv:2607.24223](https://arxiv.org/abs/2607.24223)

传统检索把相关性用于选 top-k 文档，但复杂问题还需要定位、组合和核验证据。直接语料交互（DCI）允许代理像使用 grep 一样探索文档，却可能很晚才遇到关键线索。RARG 把相关性变成执行先验：先决定文档遍历顺序，再用相关段落初始化入口，并重排 grep 匹配片段。

作者报告，RARG 在浏览问答和推理型检索上改善了准确率—效率前沿。核心启示是：相关性不必停留在“选哪些文档”，也可进入工具执行调度，让代理更早看到高信息量证据；代码已公开，适合进一步验证其成本与泛化能力。

## 选稿说明

今日候选来自 Hugging Face Daily Papers API，并按 upvotes 排序后与最近 7 天论文日报逐条做 arXiv ID 去重；以上三篇均未在历史日报的论文链接行出现。Kimi K3 同时出现在 AI 日报，但论文日报聚焦技术报告本身，属于不同编辑角度。
