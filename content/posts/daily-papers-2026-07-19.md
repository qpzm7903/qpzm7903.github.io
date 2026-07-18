---
title: "📄 论文日报 | 2026-07-19"
date: 2026-07-19T06:35:00+08:00
draft: false
tags: ["AI", "论文", "日报"]
categories: ["论文日报"]
---

今天三篇论文都围绕"让 RL 在更真实的尺度上工作"：一篇解决"百万 token 上下文怎么上 RL"的工程瓶颈，一篇研究"多 agent 搜索任务怎么不卡死循环"，一篇锁向"世界-动作模型想象与现实能否对齐"——三篇都在反思"合成数据 + benchmark 刷分"之外的真实痛点。

## ⭐ 今日必读

### LongStraw：在固定 GPU 预算下把"长上下文 RL 后训练"从 25 万 token 推到 200 万+

**论文链接**：[arXiv:2607.14952](https://arxiv.org/abs/2607.14952) ｜ [代码](https://github.com/MindLab-Research/longstraw)

**人话版**：你训一个 agent 模型，让它连续调 100 次浏览器、改 50 次代码——它需要一路记得前面发生了什么。模型推理时可以读百万 token 的上下文（[Qwen3.6](https://qwenlm.github.io/)、[GLM-5.2](https://github.com/zai-org/GLM-5) 这边都已经能推到百万级），但**训练**这一侧通常还卡在 256K 以下——因为 RL 训练要把整个上下文塞进 autograd（[反向自动微分](https://en.wikipedia.org/wiki/Automatic_differentiation)）的"计算图"里，每多一段历史就多几 GB 活内存。训练时上下文比推理短一大截，就靠"长度外推"赌部署时模型能撑住——但 agent 累积观测、工具输出、历史决策的场景下这种外推常常翻车。

LongStraw 想做的不是新算法，而是一套**架构感知的执行栈**把百万 token 的 RL 推到固定 8 卡 H20 GPU 预算可跑。它干三件事：

1. **shared prompt 不跑 autograd**：agent 任务里 prompt 通常包含工具说明、指令这些"每条样本都一样"的部分，没必要回传梯度——这部分单独前向、不能反向。
2. **只保留后续 token 真正需要的模型状态**：把无关的中间激活 detach（断开梯度链），不一直挂在线上。
3. **重放短回复分支一次一跑**：多个候选回复（GRPO 里的 group）一个一个走完反向，而不是同时挂住。

实测：8 张 H20 上对 Qwen3.6-27B 跑两组 group × 8 回复的 GRPO 打分 + 反向，**峰值位置到 210 万**；group 从 2 加到 8 只多占 **0.21 GB** 峰值内存；压力测试冲到 **446 万位置**；32 卡上对 GLM-5.2 全 78 层跑通 210 万 token 的端到端路径。

**为什么重要**：这是过去半年 RL 后训练里最关键的一块工程短板。所有把 agent 训练做严肃化的人都知道——推理能上百万 token 没用，训不动就等于没有。LongStraw 没声称完整训练正确性（作者明确说 captured prompt state 是 detach 的、部分分布式 forward/gradient 路径还没完成），但它把"百万 token RL 训练"从概念推到了"在 8 卡 H20 上真能跑通前向 + 反向"这条工程线。开源代码、可复现，给还在 256K 上下文外推赌部署的团队一份直接对照的基线。

**术语速解**：
- **GRPO（Group Relative Policy Optimization）**：DeepSeek 在 R1 里走红的 RL 算法——同一个 prompt 采一组候选回复，组内相对打分算奖励，省掉单独的 value 模型。LongStraw 默认在 GRPO 上验证。
- **autograd（自动微分）**：训练时深度学习框架自动构建的"梯度计算图"。挂在上面的激活越多、显存占用越大——这是 RL 训练上下文长不起来的根本原因。
- **detach（断梯度）**：在某个张量上切断反向传播链——它之后的部分不再产生梯度，等于把它"冻结"出计算图，省显存但代价是那段不再被训练。

**方法干讲一句**：文章核心贡献不是新算法，而是把"哪些状态必须留在 autograd 图里、哪些可以 detach + 重放"这件事分清楚——shared prompt 不反传、模型特有状态留下、group 内回复串行回放——这种工程分割让百万 token RL 在固定 GPU 下可行。

> 原文金句：
> A growing gap separates inference context lengths and RL post-training: inference systems are approaching million-token contexts, while post-training workloads often remain at 256K tokens or below and rely on length generalization at deployment. The gap is especially important for AI agents, whose observations, tool outputs, documents, and prior decisions accumulate over long trajectories.
> （推理上下文长度与 RL 后训练之间存在一个不断扩大的鸿沟：推理系统正在逼近百万 token 上下文，而后训练工作负载通常仍停留在 256K 或更短、靠部署时的长度外推补差。这个鸿沟对 AI agent 尤为关键——它们的观测、工具输出、文档和历史决策会在长 trajectory 中累积。）

## 📄 也值得了解

### SearchOS-V1：把搜索 agent 的隐式进展变成显式持久状态，让多 agent 协作不卡死循环

**论文链接**：[arXiv:2607.15257](https://arxiv.org/abs/2607.15257) ｜ [代码](https://github.com/antins-labs/SearchOS)

**人话版**：让多个 agent 一起去网上搜资料、回答一个复杂问题（比如"2026 年所有支持 GPT-5.6 Sol API 的厂商对照表"）。每个 agent 各搜各的、互相不共享记录。问题来了：一个 agent 搜过一遍没用，另一个 agent 不知道、尝试同样的搜索——三五个回合后所有人都栽进**重复搜索循环**，浪费 search budget、最后还凑不齐答案。当前多数单 agent 和 multi-agent 系统都会犯这个病。

SearchOS 把"任务进展"从 agent 脑子里的隐式状态抠出来，做成显式、持久、共享的状态。它干三件事：

1. **关系 schema 完整化**：把开放域信息检索统一建模成"补全一张关系 schema"——agent 发现 entity、往 attribute 里填值、每个值都挂一条 source evidence（出处），像填 Excel 一样把答案凑齐。
2. **SOCM（Search-Oriented Context Management）**：把不断演化的状态外化成四个对象——**Frontier Task**（还没填的格子）、**Evidence Graph**（已找到的证据）、**Coverage Map**（哪些格子已覆盖）、**Failure Memory**（搜过但失败的模式）。这四个东西跨 agent 共享、跨回合持久。
3. **Pipeline-Parallel 调度 + Search Tool Middleware Harness**：子 agent 跑完一批就立刻被新任务顶上，工具调用被中间层拦截记日志、发现 stall（卡住）或预算耗尽立刻重路由；附一个可复用的分级 skill 系统（strategy skills / access skills），避免重复踩坑。

在 WideSearch 和 GISA 两个基准上所有指标都压过现有的单 agent 和 multi-agent baseline。

**为什么重要**：这是把"长程 agentic 任务里 memory + state 这一层做成真正可工程化"的一次具体尝试——和 Mozilla 报告（7/18 AI 日报）里说的"harness 层是真正瓶颈"完全在同一根线上。给所有正在搭搜索 agent / 编排框架的团队一份具体参考：不要让记忆只活在某个 agent 的 hidden state 里。

**术语速解**：
- **pipeline-parallel 调度**：把多个子任务在不同阶段交错塞进流水线——一个 agent 跑完出结果时另一个 agent 已经在新槽位起飞，"空槽及时补"——和软件流水线一个道理。
- **search budget（搜索预算）**：agent 任务里允许的最大搜索调用数——超了就停。在 web agent 评测里限制滥用和无限循环的最常用手段。

> 原文金句：
> As interaction histories grow, agents increasingly struggle to track task progress. When search attempts fail to yield useful evidence, current single- and multi-agent systems can become trapped in repetitive loops, wasting search budgets and ultimately compromising the quality and completeness of the final output.
> （随着交互历史增长，agent 越来越难以跟踪任务进展。当搜索尝试得不到有用证据时，当前的单 agent 和多 agent 系统会困在重复循环里，浪费搜索预算、最终损害输出的质量与完整性。）

### BadWAM：让你的世界-动作模型"想象得对、动作做错"——一种新型对抗攻击

**论文链接**：[arXiv:2607.15207](https://arxiv.org/abs/2607.15207)

**人话版**：现在流行一类模型叫 **[World-Action Model（WAM，世界-动作模型）](https://arxiv.org/abs/2607.14076)**——不只会输出"下一步该做什么动作"，还会预测"做完之后世界会变成什么样"。大家本来觉得这种"动作 + 想象"的耦合是个安全保障——你能让机器人的动作**对它的想象做检查**，对不上就停。BadWAM 干的事就是：**用一点小到看不太出来的视觉扰动，让 WAM 的想象看着正常、但动作跑偏**。

它分两种攻击形态，对应"要不要顾隐蔽性"：

1. **action-only attack**：只顾破坏，把模型直接往"任务失败的错误动作"上推。
2. **imagination-preserving attack**：还要隐蔽——动作被偏移，但模型**想象的未来**和"干净输入下应该想象的未来"几乎一致，所以模型自己用"想象 vs 动作对账"也查不出来。

实测：action-only 把任务成功率从 96.5% 打到 43.1%；imagination-preserving 在保持强攻击力的同时把"未来想象漂移"压到很低，靠一点 future-preserving 正则化就能做到。

**为什么重要**：过去一年 WAM 被看成 [embodied AI / 机器人](https://huggingface.co/blog/videochat3)的最新安全护城河——很多论文在写"WAM 让安全审查可解释"。BadWAM 说明这条护城河本身有缝："看动作和想象对不上"的检查思路成立的前提是想象和动作真地同源对齐——只要攻击能同时让动作偏一点、想象跟着偏一点但偏得很微妙，对账就失效。这是给所有"用生成模型做安全护栏"思路的一记提醒。

**术语速解**：
- **WAM（World-Action Model）**：把动作生成和未来世界预测一起学的模型；常被看作 [World Model](https://arxiv.org/abs/2607.14076) 的子类，强调 / 接动作输出端。
- **adversarial perturbation（对抗扰动）**：对输入做极小、人眼不可见的修改，让模型给出完全错误的输出。最早在图像分类上被发现，BadWAM 把它落到 WAM 上。
- **closed-loop execution（闭环执行）**：模型预测动作 → 机器人在真实 / 仿真世界执行 → 把新观测回传给模型 → 再预测——一个完整闭环，BadWAM 在这种设定上测的。

> 原文金句：
> BadWAM characterizes this attack surface along two natural criteria: attack strength and stealthiness. ... imagination-preserving adversarial attack, which seeks to induce harmful action shifts while keeping the model's predicted future close to its clean imagination.
> （BadWAM 沿两个天然维度刻画这种攻击面：攻击强度与隐蔽性——其中"想象保留型对抗攻击"在诱发有害动作偏移的同时，让模型预测的未来保持在接近无扰动输入时的"干净想象"。）

## 📖 今日英语

- **post-training**（后训练 / 训练后阶段）
  原句：出 ⭐ LongStraw 摘要 "A growing gap separates inference context lengths and RL post-training"——指基础预训练之后的所有训练阶段（指令微调、RLHF、GRPO 等）。LLM 圈里"pre-training / post-training"这对词是基础二分，看模型文档时几乎所有 R 系列、o 系列的"reasoning"能力都来自这一步。

- **length generalization**（长度泛化）
  原句：出 ⭐ LongStraw 摘要 "rely on length generalization at deployment"——指模型在训练时只见过较短序列、部署时被指望能处理更长序列。这是个"赌"的成分很高的假设，agent 场景下最常翻车。

- **repetitive loop**（重复循环 / 循环卡死）
  原句：出处 📄 SearchOS-V1 "current single- and multi-agent systems can become trapped in repetitive loops"——AI agent 报告里高频出现的失败模式描述。和 stuck / loop / runaway 等词常配套使用。

- **frontier task**（未开拓任务 / 前沿格子）
  原句：出处 📄 SearchOS-V1 "Frontier Task, an Evidence Graph, a Coverage Map, and Failure Memory"——这里 frontier **不是**"前沿 AI"那种语义，而是"还没被填写的格子"的工程化表达，借自图论 / 数学圈 frontier set 概念。

- **attack surface**（攻击面）
  原句：出处 📄 BadWAM "BadWAM characterizes this attack surface along two natural criteria"——安全研究里的固定搭配，指一个系统**被攻击者可能触及的总和**。常和 expand / reduce / characterize 搭配。