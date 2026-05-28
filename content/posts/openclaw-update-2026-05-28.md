---
title: "🔧 Openclaw 更新日报 2026-05-28"
date: 2026-05-28T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.27

**发布日期**: 2026-05-28  
**⚠️ 新版本发布**

## Highlights

- Safer local/runtime boundaries: OpenClaw now rejects unsafe command wrappers, malformed CLI numeric options, unsafe Node runtime env overrides, no-auth Tailscale exposure, and non-admin device-role pairing approvals before they can affect live runs. (#87308, #87305, #87292, #87146)
- Matrix and auto-reply delivery are steadier: mention previews stay inert, final mention replies deliver normally, shared-DM notices are awaited, MXID parsing ignores filenames, and reasoning-prefixed `NO_REPLY` responses stay suppressed.
- Provider and agent reliability improved across OpenAI-compatible embeddings, cached token usage, Anthropic/Codex/Claude runtime state, unsupported tool-schema quarantine, heartbeat templates, and session fallback errors. (#85269, #82062, #85416, #86855)
- Plugin and package release paths got tighter: Pixverse ships as an external video plugin with region selection, package exclusions and shrinkwrap inventory match the published npm shape, and release/package smoke commands fail bounded instead of hanging.
- Gateway hot paths do less rediscovery by reusing current plugin metadata fingerprints, stable plugin index fingerprints, read-only session metadata, active working stores, status fast paths, and auth/env snapshots. (#86439)

## Changes

- Memory: add a core OpenAI-compatible embedding provider for local and hosted OpenAI-style endpoints, with config, doctor, and docs support. (#85269) Thanks @dutifulbob.
- Plugin SDK: mark memory-specific embedding provider registration as deprecated compatibility and surface non-bundled usage in plugin compatibility diagnostics. (#85072) Thanks @mbelinky.
- Pixverse: add video generation provider support, API region selection, and external plugin publishing.
- Plugins: expose approval action metadata for plugin-driven approval surfaces.

## Fixes

- Security/CLI/runtime: harden hostname normalization for repeated trailing dots, block side-effecting command wrappers, reject unsafe Node runtime env overrides, reject loose numeric CLI and gateway options, require admin approval for node device-role pairing, and reject no-auth Tailscale exposure. (#87305, #87292, #87308, #87146) Thanks @pgondhi987.
- Doctor: validate runtime tool schemas for every configured embedded agent while skipping ACP-only profiles, so bad non-default plugin or MCP tools are reported before assistant turns.
- Telegram: route `sendMessage` action replies through durable outbound delivery so completed agent responses remain retryable when the gateway send path times out. (#87261) Thanks @mbelinky.
- Matrix/auto-reply: keep draft previews mention-inert, preserve final mention delivery, send mention finals normally, await shared DM notices, ignore filename-embedded MXIDs, and suppress reasoning-prefixed `NO_REPLY` responses.
- Agents/providers: add OpenAI-compatible cache retention, forward cached token usage in chat completions, preserve runtime context before active user turns, strip stale Anthropic thinking, load Claude CLI OAuth for Pi auth profiles, avoid false Codex runtime live switches, and quarantine unsupported tool schemas. (#82062, #87167, #86855)
- Gateway/performance: cache plugin metadata fingerprints and stable plugin index fingerprints, borrow read-only session metadata safely, keep the active session working store hot, keep status on a bounded fast path, and preserve model auth profile suffixes. (#86439)
- Package/install/release: align npm package exclusions and inventory, omit unpacked test helpers, skip Homebrew until macOS packages need it, cap tsdown heap in containers, bound install/release smoke waits, and harden post-publish verification.
- Codex: bound ChatGPT OAuth token exchange and refresh requests so stalled auth endpoints fail instead of hanging login or refresh.
- QA/E2E/CI: bound Telegram, kitchen-sink, Open WebUI, ClawHub, MCP, Discord, realtime, labeler, and GitHub API waits; fail empty explicit test, live-media, gateway CPU, plugin gauntlet, and beta-smoke runs instead of false-greening.
- Agents/Codex: keep spawned agent bootstrap files rooted in the agent workspace while running task commands, transcripts, and compaction from the requested cwd. (#87218) Thanks @mbelinky.


---

## 💡 深度点评

### 核心亮点

*   **运行时安全边界大幅强化**：此版本重点收紧了本地执行与运行时环境的安全限制。系统现在能够识别并拒绝不安全的命令包装器（Command Wrappers）、畸形的 CLI 数值选项以及非法的 Node 运行时环境变量覆盖。此外，针对 Tailscale 的无鉴权暴露和非管理员角色的设备配对申请也增加了前置拦截，显著提升了 Agent 在本地环境执行任务时的安全性。
*   **OpenAI 兼容生态与成本管理优化**：新增了核心 OpenAI 兼容 Embedding 提供商，支持本地及托管的 OpenAI 标准端点。更重要的是，系统现在能更精准地处理缓存 Token 的使用情况并在 Chat Completions 中转发相关指标，这为基于成本和性能考量的模型调用提供了更细粒度的数据支持。
*   **网关热路径性能重构**：通过复用当前插件的元数据指纹（Metadata Fingerprints）和稳定的索引指纹，网关大幅减少了重复探索（Rediscovery）的开销。配合只读会话元数据的高效借用和工作存储的常驻热化，高频调用的路径响应速度得到了显著优化。

### 值得注意的修复

*   **预检式工具架构验证**：Doctor 诊断工具现在会在 Agent 轮次开始前，强制验证所有已配置内置 Agent 的运行时工具架构（Tool Schemas）。这一改动确保了非默认插件或错误的 MCP 工具能在实际执行前被拦截，避免了运行时的意外中断。
*   **消息传递的鲁棒性提升**：Telegram 的 `sendMessage` 操作现已接入持久化出站交付链路，当网关发送路径超时时，Agent 的响应仍可重试。同时，Matrix 协议下的提及（Mention）处理逻辑也得到了修正，解决了草稿预览干扰正常回复的问题。
*   **授权与超时控制硬化**：修复了 Codex 与 Claude 在 OAuth 令牌交换时可能导致的挂起问题，通过引入严格的端点响应边界，确保授权超时时能够快速失败而非长时间阻塞登录流程。

### 个人评价

2026.5.27 版本的更新重心明显从“功能扩张”转向了“工程治理与工业级可靠性”。通过对运行时边界的深度硬化和网关性能的细致打磨，OpenClaw 正在解决 Agent 框架在大规模生产环境中的核心痛点。尤其是对工具架构的预验证和对缓存 Token 指标的支持，体现了该工具在提升开发者排障效率和成本管控能力上的成熟度。这是一个以稳定性为导向的实干版本，建议所有追求生产安全的用户跟进升级。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-28 08:25:26*
