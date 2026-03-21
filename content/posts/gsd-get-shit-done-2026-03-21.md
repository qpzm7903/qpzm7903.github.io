---
title: "GSD：专门对抗 Context Rot 的 Claude Code 项目管理层"
date: 2026-03-21
tags: ["Claude Code", "GSD", "AI Coding", "开源项目", "工程实践"]
categories: ["AI 工具"]
description: "深入分析 get-shit-done (GSD) 的架构设计，探讨它如何通过状态文件、编排架构和验证层，从底层消灭 AI 编码过程中的 context rot 问题。"
draft: false
---

在使用 Claude Code 进行超过 3 天的持续开发后，你可能会发现它的表现开始下滑：原本能完美遵循的架构规范被无视，它开始频繁回复"I'll be more concise now"，甚至遗忘半小时前刚刚达成的技术决策。这不是 Claude 的逻辑能力下降了，而是 context window 中充斥了大量过往推理、错误尝试和冗长的文件读写记录，导致注意力的精确度发生了系统性偏移。

这种现象被称为 **Context Rot（上下文腐烂）**。对于任何试图用 AI 助手构建真实产品而非简单 Demo 的开发者来说，Context Rot 是限制生产力的核心瓶颈。

**get-shit-done（以下简称 GSD）** 的出现并非为了让 AI 写出更精妙的代码片段，而是为 Claude Code 引入了一个专门的项目管理层。它的核心逻辑只有一句话：**通过外部化的状态文件和受限的编排架构，从底层消灭 context 积累，从而彻底解决 Context Rot 问题。**

## Context Rot 是什么，为什么它是真正的问题

当你在一个 Session 中连续输入超过 50 轮对话，Claude 的 context usage 往往会跳升至 100k token 以上。此时最直观的证据是响应变慢，以及它开始丢失对全局约束的感知。Transformer 架构的注意力机制在处理超长序列时存在权重弥散——模型会更倾向于关注最近几轮对话的细节，忽略初始阶段定义的架构原则。

根本原因是信息密度超载。在原始的 Claude Code Session 中，搜索结果、代码修改记录、测试报错和无关闲聊被线性地堆叠在一起。这些"噪音"占据了宝贵的注意力空间。即使 Claude 有 200k 的窗口，真正有效的注意力和被噪音稀释后的执行质量之间存在着巨大的鸿沟。

GSD 的判断：**不要试图管理长 context，而要从架构上消灭它的积累。** 它强制要求通过文件来同步状态，而不是通过对话历史。

## 状态文件体系：将记忆外挂

GSD 要求项目根目录下存在一套标准的机器可读文件，包括 `PROJECT.md`、`STATE.md`、`REQUIREMENTS.md`、`ROADMAP.md` 和 `PLAN.md`。这些文件不是写给人类看的文档，而是 Claude 的"外挂硬盘"。

**`STATE.md`** 记录了项目的当前进度、已完成的任务、挂起的决策以及当前的障碍。每当 Claude 启动新的子任务或恢复 Session 时，它首先读取的是这个状态文件，而不是翻阅历史对话。这保证了即使在完全不同的 Session 之间，决策的连贯性也是物理存在的。

**`PLAN.md`** 采用 XML 结构描述每一个原子任务，精确到验证命令级别：

```xml
<task type="auto">
  <name>Create login endpoint</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>
    Use jose for JWT (not jsonwebtoken - CommonJS issues).
    Validate credentials against users table.
    Return httpOnly cookie on success.
  </action>
  <verify>curl -X POST localhost:3000/api/auth/login returns 200 + Set-Cookie</verify>
  <done>Valid credentials return cookie, invalid return 401</done>
</task>
```

不是"做个登录功能"，而是精确到用什么库、怎么验证、完成条件是什么。这种结构化的方式让 Claude 以极高的精确度解析"接下来要做什么"，避免了自然语言描述带来的模糊性。

通过这种方式，GSD 将项目演进从"流式历史"转变为"状态快照"。当 context 积累到影响效率时，随时重启 Session，Claude 可以在几秒内从文件恢复到工作位置，不需要任何背景补课。

## 编排架构：Thin Orchestrator + Subagents

GSD 的执行模型中，主 Session 的角色是一个"极简协调者"——它几乎从不亲自执行具体的写代码或跑测试任务。

GSD 引入了 **Wave（波次）执行模型**。协调者根据任务依赖关系将 `PLAN.md` 分解成多个 Wave：

```
WAVE 1 (并行)          WAVE 2 (并行)         WAVE 3
┌─────────┐            ┌─────────┐           ┌─────────┐
│ Plan 01 │            │ Plan 03 │           │ Plan 05 │
│User Model│           │Orders API│          │Checkout │
└─────────┘            └─────────┘           └─────────┘
┌─────────┐            ┌─────────┐
│ Plan 02 │            │ Plan 04 │
│Product  │            │Cart API │
└─────────┘            └─────────┘
```

同一 Wave 内的任务并行执行，每个 Subagent 拥有自己独立的 200k context 空间，只接收该任务相关的背景信息，完成后销毁。跨 Wave 按顺序执行，等待依赖完成。

这种设计确保主 Session 的 context 占用率始终保持在 30-40%。同时，GSD 强制执行"一个原子任务一个 commit"的原则：

```
abc123f feat: add email confirmation flow
def456g feat: implement password hashing
hij789k feat: create registration endpoint
```

每个 commit 精确对应一个 AI 执行的任务。一旦引入逻辑错误，`git bisect` 可以精确定位到是哪一个子任务出的问题。

## Nyquist 验证层：测试先于代码

GSD 内置了一个名为 Nyquist 的验证机制，它把测试提升到了比代码实现更高的优先级。

在 `plan-phase` 的研究阶段，GSD 就要求为每个需求映射自动化测试命令。Plan Checker 有一条硬性规则：**没有 `<verify>` 命令的任务，计划不通过。** 执行阶段，只有当验证命令返回成功时，任务才被标记为完成。

这意味着测试覆盖是写代码之前规划好的，不是事后补。它强迫 AI 在动手之前先思考"成功的标准是什么"。在长期的 AI 开发流程中，这是防止"看起来写完了，但实际跑不通"最有效的手段。

## 核心工作流与轻量路径

GSD 的标准工作流包含五个阶段：

```
discuss-phase  →  plan-phase  →  execute-phase  →  verify-work  →  ship
（锁定偏好）      （研究+规划）    （Wave 并行执行）   （人工 UAT）    （创建 PR）
```

**`/gsd:next`** 是核心指令：读取 `STATE.md` 自动判断当前处于哪个阶段并推进。设计目标是"走完离开，回来继续"——不需要记住上次做到哪里。

对于不需要复杂规划的 ad-hoc 任务，**`/gsd:quick`** 提供轻量路径：跳过研究和 plan-checker，但依然保留"任务-验证-commit"的原子化流程。`--discuss`、`--research`、`--full` 三个 flag 可以按需组合。

## 适合谁，不适合谁

**适合用 GSD 的场景：**
- Solo dev 或小团队，用 Claude Code 从零构建真实产品
- 已经感受到 Context Rot 痛苦，厌倦了反复纠正 AI 错误决策
- 需要跨多个 session、多天完成的复杂项目

**不适合的场景：**
- 一次性脚本或简单任务：GSD 的各种文件和验证流程反而是额外负担
- 需要精细控制每一步的场景：GSD 的"规划后全自动执行"模式是黑盒
- 已有成熟工程团队和流程的大型组织：没必要在 AI 层再套一层 PM 框架

如果你把 Claude Code 当作聊天框，GSD 没有意义。如果你准备把 Claude Code 当作执行团队，GSD 是那个负责"保持项目清醒"的项目管理层。
