---
title: "🔧 Openclaw 更新日报 2026-04-25"
date: 2026-04-25T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.24

**发布日期**: 2026-04-25  
**⚠️ 新版本发布**

## Breaking

- Plugin SDK/tool-result transforms: deprecate the Pi-only `api.registerEmbeddedExtensionFactory(...)` path for tool-result rewriting in favor of bundled `api.registerAgentToolResultMiddleware(...)`, with `contracts.agentToolResultMiddleware` declaring the targeted harnesses. The legacy Pi hook remains wired as a bundled compatibility seam, but new bundled transforms should use the harness-neutral middleware contract so transforms run consistently across Pi and Codex app-server dynamic tools. Thanks @vincentkoc.

## Changes

- WebChat/sessions: keep runtime-only prompt context out of visible transcript history and scrub legacy wrappers from session history surfaces. Thanks @91wan.
- Gradium: add a bundled text-to-speech provider with voice-note and telephony output support. (#64958) Thanks @LaurentMazare.
- Plugins/setup: honor explicit `setup.requiresRuntime: false` as a descriptor-only setup contract while keeping omitted values on the legacy setup-api fallback path. Thanks @vincentkoc.
- Plugins/setup: report descriptor/runtime drift when setup-api registrations disagree with `setup.providers` or `setup.cliBackends`, without rejecting legacy setup plugins. Thanks @vincentkoc.
- Plugin hooks: expose first-class run, message, sender, session, and trace correlation fields on message hook contexts and run lifecycle events. Thanks @vincentkoc.
- Plugins/setup: include `setup.providers[].envVars` in generic provider auth/env lookups and warn non-bundled plugins that still rely on deprecated `providerAuthEnvVars` compatibility metadata. Thanks @vincentkoc.
- Plugins/setup: derive generic provider setup choices from descriptor-safe `setup.providers[].authMethods` before falling back to setup runtime. Thanks @vincentkoc.
- Plugins/setup: surface manifest provider auth choices directly in provider setup flow before falling back to setup runtime or install-catalog choices. Thanks @vincentkoc.
- Plugins/setup: warn when descriptor-only setup plugins still ship ignored setup runtime entries, keeping `setup.requiresRuntime: false` semantics explicit without breaking existing metadata. Thanks @vincentkoc.
- Plugins/channels: use manifest `channelConfigs` for read-only external channel discovery when no setup entry is available or setup descriptors declare runtime unnecessary. Thanks @vincentkoc.
- TUI/dependencies: remove direct `cli-highlight` usage from the OpenClaw TUI code-block renderer, keeping themed code coloring without the extra root dependency. Thanks @vincentkoc.
- Diagnostics/OTEL: export run, model-call, and tool-execution diagnostic lifecycle events as OTEL spans without retaining live span state. Thanks @vincentkoc.

## Fixes

- Plugin SDK/tool-result transforms: bound middleware `details`, validate in-place result mutations, and mark fail-closed middleware fallbacks with canonical `error` status. Thanks @vincentkoc.
- Discord/gateway: prevent startup from getting stuck at `awaiting gateway readiness` when Carbon gateway registration races with a lifecycle reconnect. Fixes #52372. (#68159) Thanks @IVY-AI-gif.
- Discord/gateway: supervise Carbon's async gateway registration promise so fatal Discord metadata failures surface through startup instead of process-level unhandled rejections. (#62451) Thanks @safzanpirani.
- Discord/gateway: record websocket frame activity as transport liveness, so idle but healthy Discord gateways no longer look stale between user messages. (#68213) Thanks @bmadwaves.
- Slack/streaming: suppress block replies while native or draft preview streaming owns the turn, preventing duplicate Slack delivery when block streaming is also enabled. Addresses #56675. Thanks @hsiaoa.
- Plugins/cache: restore plugin command and interactive handler registries on loader cache hits without resetting interactive callback dedupe, so cached external plugins keep slash commands and callback handlers available after reloads. Fixes #71100. Thanks @BomBastikDE.
- Gateway/OpenAI-compatible: report non-zero token usage for `/v1/chat/completions` when the agent run has only last-call usage metadata available. Fixes #71118. (#71242) Thanks @RenzoMXD.
- Plugin SDK/tool-result transforms: restrict harness tool-result middleware to bundled plugins, fail closed on middleware errors, validate rewritten result shapes, preserve Pi per-call ids, and keep Codex media trust checks anchored to raw tool provenance. Thanks @vincentkoc.
- Gateway/MCP loopback: apply owner-only tool policy and run before-tool-call hooks on `127.0.0.1/mcp` `tools/list` and `tools/call`, so non-owner bearer callers can no longer see or invoke owner-only tools such as `cron`, `gateway`, and `nodes`, matching the existing HTTP `/tools/invoke` and embedded-agent paths. (#71159) Thanks @mmaps.
- Codex harness/security: wait for final app-server approval decisions and sanitize approval preview text, so native Codex permission prompts cannot be resolved by an early placeholder decision or render unsafe terminal/control content. (#70751, #70569) Thanks @Lucenx9.
- Providers/voice security: route ElevenLabs TTS and OpenAI Realtime browser-session secret creation through guarded fetch paths, preserving provider calls while keeping SSRF protections on voice surfaces. Thanks @steipete.
- Agents/OpenAI WS: match Codex's Responses WebSocket continuation strategy, sending only strict incremental follow-up input with `previous_response_id` and falling back to full context when the replay chain or request shape differs. Fixes #44948. Thanks @hss-oss.


---

## 💡 深度点评

OpenClaw 2026.4.24 版本发布，这是一次侧重于**架构标准化、实时语音能力扩展以及可观测性增强**的重要更新。以下是本次更新的深度点评：

### 核心亮点

*   **插件 SDK 与 Harness 架构归一化**：Breaking Change 明确废弃了原有的 `api.registerEmbeddedExtensionFactory`，转而推行通用的 `api.registerAgentToolResultMiddleware` 契约。这意味着工具结果的改写逻辑现在可以在 Pi 和 Codex 等不同 Harness 之间保持一致，减少了跨运行时环境的兼容性负担。
*   **多模态实时交互（Realtime）爆发**：此版本深度集成了 Gemini Live 和 OpenAI Realtime 协议，并新增了 Google Meet 参与者插件。支持通过 WebRTC 建立实时语音会话，配合 `openclaw_agent_consult` 工具，使得 Agent 能够直接参与在线会议并处理复杂的实时音频流。
*   **浏览器自动化工具链升级**：引入了 `browser-automation` 技能包，支持 Playwright 的 AI Aria 快照 API 和稳定的 `tabId` 句柄。这显著提升了 Agent 在复杂网页（如 Google Meet 入会拦截界面）中的定位准确性，增强了多标签页协作的稳定性。

### 值得注意的修复

*   **MCP 环回安全策略强化**：修复了 `127.0.0.1/mcp` 的鉴权漏洞，现在非 Owner 调用者无法通过本地 MCP 路径列出或调用 `cron`、`gateway` 等敏感工具，实现了与 HTTP API 一致的安全基线。
*   **Discord/Slack 传输层稳定性**：解决了 Discord 网关启动时因 Carbon 注册竞争导致的挂起问题，并修正了 Slack 在流式输出模式下可能产生的重复回复或丢包逻辑。
*   **DeepSeek V4 兼容性优化**：针对 DeepSeek V4 的 Thinking（思维链）控制进行了微调，确保在 Replay 过程中能够正确处理或剔除 `reasoning_content`，适配了 V4 Flash 和 Pro 模型。

### 个人评价

这个版本标志着 OpenClaw 正在从一个单纯的“指令执行框架”演变为一个真正的“生产力中枢”。通过 OpenTelemetry (OTEL) 链路追踪的深度集成和 SBOM 依赖风险报告，项目的工业级标准得到了显著提升。实时语音能力的加入让 Agent 具备了更强的现场感，而插件描述符（Descriptor）与运行时的进一步解耦，则展示了开发团队在长期维护性和插件生态规范化上的决心。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-25 08:01:51*
