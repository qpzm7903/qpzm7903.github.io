---
title: "混合专家模型（Mixture-of-Experts, MoE）"
date: 2026-07-12T06:50:00+08:00
tags: ["概念"]
---

**人话版**：普通神经网络是"每一个输入都让所有参数一起算一遍"，模型越大推理越慢。混合专家模型（Mixture-of-Experts，MoE）的思路是：把模型拆成很多个"专家"子网络，遇到一个输入时只激活其中最相关的一两个专家来算，其他专家可以"摸鱼"。这样总参数量很大（知识容量大），但单次计算量很小（推理快）——把"模型大"和"算得快"这两个原本矛盾的目标解耦。

**一个例子**：一个 100B 参数的 MoE 模型可能每个 token 只激活 5B 参数的"专家"参与计算，单步计算量约等于一个 5B 的 dense 模型，但知识容量接近一个 100B 模型。这就是为什么现在很多旗舰大模型（如 GLM-5、Mixtral、Qwen3、DeepSeek 系列）都采用 MoE 架构。

**常见搭配**：top-2 routing（每次激活 2 个专家）、expert capacity（每个专家每步最多能接多少任务）、load balancing loss（防"几个专家累死、其他专家闲死"的正则项）、fine-grained MoE（把专家拆得更细、数量更多）、shared expert（所有 token 都经过的"共享专家"，保留通用知识）。

**延伸阅读**：[Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer (Shazeer et al., 2017)](https://arxiv.org/abs/1701.06538)