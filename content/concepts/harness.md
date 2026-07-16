---
title: "Harness（Agent 框架/套件）"
date: 2026-07-17T06:31:18+08:00
tags: ["概念"]
---

## Harness 是什么

在 AI agent 语境下，**harness** 指的是包裹在大语言模型外面的那层"脚手架"代码——它负责组装 prompt、管理对话状态、调用外部工具（搜索、代码执行、文件读写等）、协调多步执行流程。模型本身只是"大脑"，harness 是"手脚和神经系统"。

一个类比：你可以把大模型想象成一个很聪明的客服坐席，但光有脑子不够——她还需要电话系统、工单系统、知识库检索接口、转接上级的权限。这些"周边设施"合在一起就是 harness。

## 为什么重要

同一个底座模型，配上不同的 harness，能力差距可以非常大。Kimi K3 技术博客专门讲了它如何用 K3 自主构建 GPU 编译器、设计芯片，这些能力不只来自模型参数大，也来自 harness 把代码执行、截图反馈、多轮迭代串起来的能力。

今天 HuggingFace 遭到的 AI 攻击，攻击者也是用了一个"agentic 安全研究框架"作为 harness——说明 harness 既能做好事也能做坏事，理解它对攻防双方都很关键。

Harness 的工程做法正在快速演进——从手写 prompt 到使用框架（Claude Code、Codex、OpenCode 等），再到论文层面的"behavior localization"自动化维护。这一层很可能成为 2026-2027 年 AI 工程的主战场之一。

## 延伸阅读

- [Harness Handbook 论文](https://arxiv.org/abs/2607.13285)——专门研究如何让 agent harness 可读、可导航、可编辑
- [Kimi K3 技术博客](https://www.kimi.com/blog/kimi-k3)——展示了用 harnessed agent 构建编译器、芯片的案例