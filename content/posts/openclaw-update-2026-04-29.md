---
title: "🔧 Openclaw 更新日报 2026-04-29"
date: 2026-04-29T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.27

**发布日期**: 2026-04-29  
**⚠️ 新版本发布**

## Changes

- Sandbox/Docker: add opt-in `sandbox.docker.gpus` passthrough for Docker sandbox containers so local GPU workloads can run inside sandboxed agents when the host Docker runtime supports `--gpus`. Fixes #57976; carries forward #58124. Thanks @cyan-ember.
- iOS/Gateway: add an authenticated `node.presence.alive` protocol event and `node.list` last-seen fields so background iOS wakes can mark paired nodes recently alive without treating them as connected. Carries forward #63123. Thanks @ngutman.
- Android: publish authenticated `node.presence.alive` events after node connect and background transitions so paired Android nodes retain durable last-seen metadata after disconnects. Carries forward #63123. Thanks @ngutman.
- Gateway/chat: accept non-image attachments through `chat.send` by staging them as agent-readable media paths, while keeping unsupported RPC attachment paths explicit instead of silently dropping files. Fixes #48123. (#67572) Thanks @samzong.
- Security/networking: add opt-in operator-managed outbound proxy routing (proxy.enabled + proxy.proxyUrl/OPENCLAW_PROXY_URL) with strict http:// forward-proxy validation, loopback-only Gateway bypass, and cleanup of proxy env/dispatcher state on exit. (#70044) Thanks @jesse-merhi and @joshavant.
- Dependencies: refresh provider and tooling dependencies, including AWS SDK, PI runtime packages, AJV, Feishu SDK, Anthropic SDK, tokenjuice, and native TypeScript/oxlint tooling. Thanks @dependabot.
- Matrix/QA: add live Matrix approval scenarios for exec metadata, chunked fallback, plugin approvals, deny reactions, thread targeting, and `target: "both"` delivery, with redacted artifacts preserving safe approval summaries. Thanks @gumadeiras.
- Diagnostics/Codex: add owner-only core `/diagnostics` with a sensitive-data preamble, docs link, and explicit Gateway export approval guidance; Codex harness sessions also ask before uploading Codex feedback for the attached thread and print the matching `codex resume <thread-id>` inspection command after confirmed upload. Thanks @pashpashpash.
- Trajectory export: route `/export-trajectory` through per-run exec approval, send group-chat approval prompts and export results only to the owner privately, and add `openclaw sessions export-trajectory` for the approved command path. Thanks @pashpashpash.
- Codex: add Computer Use setup for Codex-mode agents, including `/codex computer-use status/install`, marketplace discovery, optional auto-install, and fail-closed MCP server checks before Codex-mode turns start. Fixes #72094. (#71842) Thanks @pash-openai.
- Apps: consume Peekaboo 3.0.0-beta4 and ElevenLabsKit 0.1.1, align Swabble on Commander 0.2.2, and refresh macOS/iOS SwiftPM resolutions against the released dependency graph. Thanks @Blaizzy.
- Plugin SDK: expose shared channel route normalization, parser-driven target resolution, raw-target compact keys, parsed-target types, and route comparison helpers through `openclaw/plugin-sdk/channel-route`, switch native approval origin matching onto that route contract with optional delivery and match-only target normalization, and retire the internal channel-route shim behind dated compatibility aliases for legacy key/comparable-target helpers. Thanks @vincentkoc.

## Fixes

- BlueBubbles: tighten DM-vs-group routing across the outbound session route (`chat_guid:iMessage;-;...` DMs no longer classified as groups), reaction handling (drop group reactions that arrive without any chat identifier instead of synthesizing a `"group"` literal peerId), inbound `chatGuid` fallback (no longer fall back to the sender's DM chatGuid when resolving a group whose webhook omits chatGuid+chatId+chatIdentifier), and short message id resolution (carry caller chat context so a numeric short id reused after a long group conversation cannot silently resolve to a message in a different chat, with the same cross-chat guard applied to full GUIDs so retries cannot bypass it). Thanks @zqchris.
- Agents/approvals: fail restart-interrupted sessions whose transcript tail is still `approval-pending` instead of replaying stale exec approval IDs into the new Gateway process after restart. Fixes #65486. Thanks @mjmai20682068-create.
- CLI/Gateway: use method-specific least-privilege scopes for classified CLI Gateway calls while preserving legacy broad scopes for unclassified plugin methods, so read-only commands no longer create admin/write/pairing scope-upgrade prompts. Fixes #68634. Thanks @nightmusher.
- Gateway/sessions: align `chat.history` and `sessions.list` thinking defaults with owning-agent and catalog-aware resolution so Control UI session defaults match backend runtime state. (#63418) Thanks @jpreagan.
- Devices/pairing: recover array-shaped device and node pairing state files before persisting approvals, so UUID-keyed pending and paired entries no longer disappear after a malformed JSON store write. Fixes #63035. Thanks @sar618.
- Gateway/auth: clear reused stale device tokens and stop reconnecting on device-token mismatch in the Control UI and Node gateway clients, avoiding rate-limit loops after scope-upgrade or token-rotation handoffs. Fixes #71609. Thanks @ricksayhi.
- Gateway/approvals: treat duplicate same-decision approval resolves as idempotent during the resolved-entry grace window, including consumed `allow-once` approvals, while returning an explicit already-resolved error for conflicting repeats. Fixes #59162; refs #58479 and #65486. Thanks @wikithoughts, @sajazuniga7-coder, and @mjmai20682068-create.
- Channels/Telegram: honor `approvals.exec/plugin.targets[].accountId` when routing native approvals across multi-bot Telegram accounts while preserving unscoped Telegram targets for any account. Fixes #69916. Thanks @joerod26.
- Agents/exec: omit the internal session-resume fallback preface from successful async exec completion messages sent directly back to chat. Fixes #67181. Thanks @raistlin88.
- Agents/media: register detached `video_generate` and `music_generate` tool run contexts until terminal status, so Discord-backed provider jobs stay live in `/tasks` instead of becoming `lost` when the parent chat run context disappears. Thanks @vincentkoc.
- Agents/media: prefer OpenAI image and video providers when the default model uses the OpenAI Codex auth alias, so auto media generation no longer falls through to Fal before GPT Image or Sora. Thanks @vincentkoc.
- Tasks/media: infer agent ownership for session-scoped task records so `/tasks` agent-local fallback includes session-backed `video_generate` and other async media jobs even when the current chat session has no linked rows. Thanks @vincentkoc.


---

## 💡 深度点评

作为 AI 开发工具博主，针对 openclaw 2026.4.27 版本的更新内容，以下是技术维度的深度点评：

### 核心亮点

*   **Codex Computer Use 的深度集成**：此版本完善了 Codex 模式下的计算机控制（Computer Use）设置，新增了状态查询、自动安装及 marketplace 发现功能。配合 `cua-driver` 与 PeekabooBridge 的文档更新，标志着 openclaw 从纯文本交互向系统级自动化控制迈出了关键一步。
*   **Sandbox GPU 透传能力**：新增了 `sandbox.docker.gpus` 选项，允许本地 GPU 工作负载在 Docker 沙箱环境中运行。对于需要在受限容器内测试显存密集型任务或运行本地模型推理的开发者来说，这是提升隔离环境性能的核心更新。
*   **模型目录（Model Catalog）架构重构**：大量的 Provider（如 DeepSeek、Fireworks、Together AI、Mistral 等）从硬编码逻辑迁移到了基于 Manifest 的静态目录管理。这种模块化设计不仅提升了 Gateway 的启动速度，也为开发者自定义模型和第三方插件接入提供了更标准、更清晰的路径。

### 值得注意的修复

*   **DeepSeek 推理逻辑补全**：修复了 DeepSeek V4 在常规 Assistant 消息重放中缺失 `reasoning_content` 的问题，确保了多轮对话中“思考链”逻辑的连续性，避免了因工具调用后状态丢失导致的异常。
*   **通信渠道（Channel）路由精准化**：针对 BlueBubbles 进行了严格的 DM 与群组路由校准，解决了 iMessage 消息在复杂会话中可能出现的标识符混淆问题，提升了在多模态、多群组场景下的通信鲁棒性。
*   **任务生命周期管理优化**：修复了 Discord 背景下视频、音乐生成任务因父上下文消失而标记为 `lost` 的 bug，通过持久化任务记录和所有权推断，确保了长耗时异步任务的最终交付。

### 个人评价

这个版本展现了 openclaw 从“快速迭代”向“架构标准化”转型的趋势，尤其是对插件 SDK 单元测试路径的拆分和 Manifest 驱动的配置设计，大幅降低了系统的耦合度。GPU 透传与 Computer Use 功能的强化，意味着其定位已不再仅仅是 API 网关，而是一个具备强本地能力的 Agent 运行环境。整体来看，2026.4.27 是一个在提升开发者生产力的同时，极力追求系统稳定与资源隔离的高质量版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-29 08:01:39*
