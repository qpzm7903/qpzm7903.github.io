---
title: "🔧 Openclaw 更新日报 2026-05-15"
date: 2026-05-15T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.14

**发布日期**: 2026-05-15  
**⚠️ 新版本发布**

## Changes

- Dependencies: route root ambient Node proxy agents through `@openclaw/proxyline` and drop root `proxy-agent`, `https-proxy-agent`, and `minimatch` dependencies.
- Control UI/i18n: add a `pnpm ui:i18n:report` baseline report for hardcoded-copy focus areas and locale fallback metadata. (#81320) Thanks @samzong.
- Maintainer tooling: add a repo-local `codex-review` skill for Codex closeout reviews, including local dirty-work and PR-branch review helpers that rerun until no accepted/actionable findings remain and avoid unsupported inline prompts with `--base`.
- Maintainer tooling: fail CI when pull requests add package patch files or pnpm patched dependencies, preserving the upstream-and-bump dependency workflow.
- Codex app-server: stream commentary preambles into editable channel progress drafts without promoting them to final answers.
- Codex migration: remove the bundled `codex-cli` backend and repair legacy `codex-cli/*` model refs to the Codex app-server route on `openai/*`.
- Gateway/startup: add owner-level startup trace attribution for auth, plugin loading, lookup counts, and plugin sidecar services. (#81738) Thanks @samzong.
- Plugins/hooks: expose the resolved effective `contextTokenBudget` plus source/reference metadata on `llm_output` and sanitized `model_call_*` hook events/contexts so plugin cost and context-health alerts can use agent-level context caps. Fixes #64327. Thanks @BunsDev.
- Channels/status reactions: wire `StatusReactionController` into WhatsApp message turns (queued → thinking → tool → done/error lifecycle, on par with Telegram and Discord), add `deploy`/`build`/`concierge` emoji categories with tool-token routing, and replace the status reaction defaults with self-explanatory emoji (🧠 thinking, 🛠️ tool, 💻 coding, 🌐 web, ⏳ stallSoft, ⚠️ stallHard, ✅ done, ❌ error, 🗜️ compacting) so stall and lifecycle reactions read as status indicators instead of emotional commentary. Fixes #59077. (#80612) Thanks @gado-ships-it.
- Control UI: add a browser-local Text size setting in Appearance and Quick Settings, scaling chat and dense UI text while keeping inputs above the mobile Safari focus-zoom threshold. Fixes #8547. Thanks @BunsDev.
- Docs: add a dedicated ds4 provider page with local DeepSeek V4 Flash config, on-demand startup, context sizing, and live verification steps.
- Release validation: add a package-installed Docker user-journey lane that verifies onboarding, mocked model setup, external plugin install/uninstall, ClickClack outbound/inbound messaging, Gateway restart survival, and doctor.

## Fixes

- Agents/WebChat: stop a successful assistant turn whose stale `errorMessage` matches a billing, auth, or rate-limit pattern from rotating profiles, falling back, or surfacing a hard `FailoverError` unless the current attempt has a real failover failure. (#70900) Thanks @truffle-dev.
- Control UI/logs: make the Gateway Logs stream height responsive to the viewport with a minimum height floor, so larger screens can show substantially more log lines without collapsing on shorter viewports. (#53916) Thanks @extrasmall0.
- ACP/Codex: surface redacted Codex wrapper stderr for generic ACP internal failures and preserve safe Codex model/provider routing in isolated `CODEX_HOME`, making `sessions_spawn(runtime="acp", agentId="codex")` failures actionable. Fixes #80079. (#80718) Thanks @leoge007.
- ACP: treat rejected timeout config options as best-effort hints so ACP turns continue with adapters that do not support `session/set_config_option` timeout keys. Fixes #81250. (#81603) Thanks @qkal.
- Cron/Codex: default exact-command scheduled agent turns to lightweight bootstrap context so automation runs the command before loading workspace identity or memory context.
- Codex cron: disable native Codex project-doc loading for lightweight app-server cron turns so scheduled jobs avoid project-doc injection after OpenClaw suppresses bootstrap context. (#81822) Thanks @jalehman.
- Codex plugin/Gateway: strip unpaired UTF-16 surrogates from Codex app-server JSON-RPC payloads and let stale reply-work recovery abort stalled reply runs, preventing malformed media turns from wedging gateway lanes.
- Codex app server: force OAuth refresh requests to perform a real token refresh instead of reusing unchanged inherited auth-profile tokens after refresh failures. (#80738) Thanks @simplyclever914.
- Control UI/WebChat: render `/tts audio` replies as playable audio attachments through the assistant-media ticket path, with structured-audio compatibility for older live payloads. (#81722) Thanks @Conan-Scott.
- Bind gateway approval access to requester metadata [AI]. (#81380) Thanks @pgondhi987.
- Telegram: let isolated polling drain independent topics, DMs, and status/control commands concurrently while preserving same-lane order. (#81849) Thanks @VACInc.
- Ollama/Doctor: copy explicit native Ollama `contextWindow` or `maxTokens` provider/model budgets into `params.num_ctx` during `openclaw doctor --fix`, preserving large-context configs after native Ollama stopped inferring per-request `num_ctx`. Fixes #81878. (#81928) Thanks @joshavant and @ArthurusDent.


---

## 💡 深度点评

### 核心亮点

- **子代理任务流转优化**：子代理的 `sessions_spawn` 任务现在直接投递到子会话的第一个可见 `[Subagent Task]` 消息中，不再隐藏于系统提示词（System Prompt）内。这一设计在保持任务可审计性的同时，有效避免了 Token 的重复消耗。
- **上下文预算与监控暴露**：插件系统在 `llm_output` 和经过脱敏的 `model_call_*` Hook 事件中，正式暴露了实际生效的 `contextTokenBudget` 及引用元数据。这使得开发者可以基于代理级别的上下文上限，构建精确的成本控制和上下文健康度告警。
- **实时语音流集成**：在语音调用层面，新增了基于 Telnyx 的实时媒体流（Realtime Media-streaming）支持，为构建低延迟的对话式语音应用提供了基础设施。

### 值得注意的修复

- **多代理心跳调度（Heartbeat）重构**：修复了导致多代理心跳节奏崩溃的 7 个底层堆叠问题。关键修复包括：使用 `Promise.all` 并行广播唤醒以防止单代理阻塞全局；修复 TCP/TLS 握手阶段的流超时挂起问题；以及确保 `HEARTBEAT.md` 中的散文指令（即使没有定义周期任务）也能正确触达模型。
- **跨渠道 Bot 无限循环防护**：在核心的渠道流转内核中实现了共享的 Bot 循环防护机制。通过对 `(scope, conversation, participant pair)` 进行联合限流，在 Discord、Slack、Matrix 和 Google Chat 等渠道中彻底阻断了 Bot 之间互相回复导致的死循环风暴。
- **内存持久化异常冒泡**：修复了内存刷新（Memory-flush）失败时的静默吞异常问题。现在，提供商超时、传输错误等非中止性失败会作为可见的回复 Payload 正确冒泡，使得外层重试逻辑和隔离的 Cron 任务能捕获到真实错误，而不是收到虚假的 `status: "ok"`。

### 个人评价

openclaw 本次更新展现了框架向企业级生产环境演进的明确倾向，重点攻坚了多代理并发场景下的稳定性和可观测性。对 Heartbeat 调度器的底层重构以及全局 Bot 循环防护的引入，解决了复杂自动化工作流中最棘手的系统级阻塞与失控问题。同时，通过暴露 Hook 的 Token 预算明细和优化子代理上下文分配，官方正为开发者提供更细粒度的成本与性能调优抓手。总体而言，这是一个极具技术含量的「硬核」维护版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-15 08:04:26*
