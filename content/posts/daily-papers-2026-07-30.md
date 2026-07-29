---
title: "📄 论文日报 | 2026-07-30"
date: 2026-07-30T06:39:03+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

## ⭐ 今日必读

### HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity UMI Data Alone

**作者：** Yuteng Wei、Jinming Ma、Jiawei Wang 等
**论文链接：** [arXiv:2607.25895](https://arxiv.org/abs/2607.25895)

**人话版：** 教机器人做家务或装配，通常要让真人遥控真实机器人录示范，准确但昂贵。HiFi-UMI 想证明：如果把“人手拿便携设备做示范”的数据采得足够准，就能不做真实机器人后训练，直接把策略部署到机器上。

系统把头戴式双目惯性定位、双夹爪原生相对位姿、微秒级 GPIO 同步和每只手约 200° 视野的双广角相机组合起来，在没有外部追踪基础设施时达到 3 mm 工作区局部末端精度。只用 HiFi-UMI 演示做后训练的策略可直接部署到真实机器人；最强策略在精密插入任务上达到 85% 成功率。

团队还开放 2,000 小时的 HiFi-UMI-2K 数据集，每条示范都通过仿真回放自动重建和检查。报告称，用同一体系的 4,000 小时数据预训练后，十项未见任务的动作误差下降 41%。重要性在于它尝试把机器人数据生产从昂贵设备使用时间，转向可规模化的人类示范采集。

**原文金句：** “We demonstrate zero-robot post-training.”
**中文：** 我们展示了不使用真实机器人数据的后训练。

## 📄 也值得了解

### Self-Supervised Consistency Enhanced Disentangled Learning for Neural Decoding Generalization in Brain-Machine Interface

**作者：** Jiyu Wei、Di Hong、Zhanjie Zhang 等
**论文链接：** [arXiv:2607.24023](https://arxiv.org/abs/2607.24023)

**人话版：** 脑机接口今天能读懂的神经信号，过几天可能“口音变了”，导致控制效果变差。这篇论文希望让解码器学会忽略这种日常漂移，并分别理解速度、方向和快慢，不必天天重新校准。

SSCDL 先用教师—学生一致性约束和模拟扰动，学习对神经漂移不敏感的表示；再用三个专门解码器分别处理 velocity、direction 和 speed。作者报告其跨天解码性能与稳定性达到当前最佳水平。对长期使用的侵入式脑机接口而言，减少反复校准是从实验室走向康复与辅助设备的关键条件。

### A New Role for Relevance: Guiding Corpus Interaction in Agentic Search

**作者：** Yuqing Li、Zexue He、Julian McAuley 等
**论文链接：** [arXiv:2607.24223](https://arxiv.org/abs/2607.24223)

**人话版：** 搜索代理像人在一大堆文件里用 grep 找答案；如果完全按文件顺序扫，关键线索可能很晚才出现。RARG 先给文件和段落排优先级，让代理先看更可能有用的地方。

方法把相关性从一次性的 top-k 筛选变成执行先验：安排文档遍历顺序、用相关段落初始化入口，并重新排序 grep 命中片段。作者称它在浏览问答和推理型检索上改善了准确率—效率权衡。代码已经公开，下一步值得检查的是不同语料规模下的成本，以及重排模型本身是否会漏掉“看似不相关但决定答案”的证据。

## 📖 今日英语

1. **high-fidelity（高保真）**
   原句（HiFi-UMI）： “Learning deployable manipulation policies is bottlenecked by the scarcity of data that is both high-fidelity and scalable.”
   常用于数据、音频、仿真和传感器，强调与真实对象足够接近。
2. **neural drift（神经漂移）**
   原句（SSCDL）： “Due to neural drift, the performance of BMIs decreases over time.”
   这是脑机接口长期稳定性讨论中的核心短语。
3. **execution prior（执行先验）**
   原句（RARG）： “RARG turns relevance into an execution prior for corpus interaction.”
   适合描述一个评分不只做筛选，还直接决定工具执行顺序。

## 选稿说明

候选来自 Hugging Face Daily Papers API，并按 upvotes 排序后与最近 7 天日报的“论文链接”行逐条做 arXiv ID 去重。Kimi K3 已归入 AI 日报，因此论文日报不重复收录其技术报告；以上三篇的 URL 均未在历史日报出现。
