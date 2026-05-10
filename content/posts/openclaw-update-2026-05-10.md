---
title: "🔧 Openclaw 更新日报 2026-05-10"
date: 2026-05-10T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.9

**发布日期**: 2026-05-10  
**⚠️ 新版本发布**

## Changes

- Skills: add `skills.load.allowSymlinkTargets` so intentional symlinked skill folders can resolve into trusted sibling repos without disabling root containment.
- Chat commands: add `/think default` and `/fast default` to clear session overrides and inherit configured/provider defaults. (#79385) Thanks @VACInc.
- Dependencies: refresh workspace dependency pins and lockfile, including `@openai/codex` `0.130.0`, `acpx` `0.7.0`, AWS SDK `3.1044.0`, OpenTelemetry `0.217.0`, `typebox` `1.1.38`, `vite` `8.0.11`, `oxfmt` `0.48.0`, and `oxlint` `1.63.0`, and update the Codex harness model snapshot for the new bundled app-server catalog.
- Plugins/install: add guarded plugin install overrides so onboarding and repair tests can route specific plugins to registry specs or local `npm pack` artifacts via environment variables.
- Tests/Docker: add Codex on-demand install and live plugin-tool dependency E2E lanes for packaged onboarding and npm-pack plugin proof.
- Plugins/ACPX: accept an optional `args` array in `agents.<name>` config so paths and flag values containing spaces stay intact when spawning ACP agent processes. Thanks @TheArchitectit and @BunsDev.
- Agents: inject the current provider/model identity into system prompts, including configured prompt overrides and CLI hook prompt replacements, so agents can answer model-identity questions from the actual runtime selection.
- Agents/subagents: add prompt-only `agents.defaults.subagents.delegationMode` and per-agent overrides with `suggest`/`prefer` modes, and centralize config-backed system prompt resolution across embedded, CLI, compaction, and command-export prompt surfaces.
- Plugins/CLI: add the optional bundled `oc-path` plugin, providing `openclaw path` for surgical `oc://` access to markdown, JSONC, and JSONL workspace files.
- Plugins/SDK: add unified model catalog registration for text, image, video, and music providers, including `providerCatalogEntry` manifests, shared media list help, live catalog caching, and per-model video capability overlays.
- Plugin SDK: add presentation helpers for controls-only interactive rendering and opt-in empty fallback text so rich channel renderers can share `MessagePresentation` semantics without duplicating native cards or components.
- CLI: make parser, startup, config, guardrail, channel, agent, task, session, and MCP failures explain what happened and point to the next recovery command.

## Breaking

- Channels/iMessage: remove the bundled BlueBubbles channel surface and deprecate BlueBubbles-backed iMessage setup in OpenClaw. Existing `channels.bluebubbles` configs must migrate to `channels.imessage` using `imsg` on a signed-in Mac or an SSH wrapper, and non-macOS default `imsg` configs now report remote-Mac wrapper guidance.

## Fixes

- Google/Gemini: default new API-key onboarding to stable `google/gemini-2.5-flash` instead of the preview Pro route, reducing surprise daily quota exhaustion. Fixes #79670. Thanks @HugeBunny.
- Amazon Bedrock: expose Claude thinking profiles through the lightweight provider policy surface so `/think:adaptive` validates before the Bedrock runtime plugin is loaded. Fixes #79754. Thanks @phoenixyy and @hclsys.
- Codex/transcripts: mirror dynamic tool calls and outputs into Codex app-server transcripts so tool activity is visible alongside assistant text instead of being elided, with per-item output capped at 12,000 characters. (#79952) Thanks @scoootscooob.
- Memory: close temp SQLite handles before failed atomic reindex cleanup and retry Windows EBUSY/EPERM/EACCES temp file removals, so `memory index --force` does not abort or leave temp sidecars on locked filesystems. Fixes #79708. Thanks @LobsterFarmerAmp and @hclsys.
- Agents/CLI: add an explicit `reseedFromRawTranscriptWhenUncompacted` backend opt-in so safe invalidated CLI sessions can reseed from a bounded raw OpenClaw transcript tail before compaction while auth-boundary resets remain no-raw. Fixes #79713. (#79764) Thanks @hclsys.
- Agents/CLI: handle resumed CLI JSONL output and bound supervisor output buffering so resumed runs stay readable without letting noisy child output grow unbounded.
- Codex app-server: honor per-call `timeoutMs`, configured `image_generate` timeouts, and media image-understanding timeouts for dynamic tool calls, capped at 600000 ms, so slow image generation and image analysis no longer fail at the 30s bridge default. Fixes #79810. Thanks @omarshahine.
- Agents/sandbox: include the container workspace path hint in sandbox-root escape errors while preserving shortened host workspace roots. Fixes #79712. Thanks @haumanto and @hclsys.
- Image generation: honor configured web-fetch SSRF policy across OpenAI, Google, MiniMax, OpenRouter, and Vydra provider requests so RFC2544 fake-IP proxy opt-ins reach generation calls. Fixes #79716. (#79765) Thanks @hclsys.
- Telegram: persist reply-chain message cache records as a compact append log instead of rewriting the full cache on every inbound message, reducing large-group turn latency.
- Telegram/CLI-backend: mirror outbound replies to the session transcript so CLI-backend agent responses create `.jsonl` session files, preventing `sessionId=unknown` on subsequent runs. Fixes #75991.
- QQBot: route gateway WebSocket connections through the ambient proxy agent so deployments with `https_proxy`, `HTTPS_PROXY`, or `HTTP_PROXY` can reach the QQ gateway. (#72961) Thanks @xialonglee.


---

## 💡 深度点评

### 核心亮点

* **Discord 语音与实时交互重构**：引入 `agent-proxy` 作为默认语音模式，使实时语音频道直接成为 Agent 会话的扩展，而非简单的 STT/TTS 转换。配合 ElevenLabs 的低延迟流式输出优化和更完善的“插嘴”（Barge-in）控制，语音交互的响应速度和自然度有了质的提升。
* **iMessage 原生能力与消息回追**：新增了对离线消息的自动回追（Catchup）功能，确保网关重启或休眠期间的消息不遗漏。同时，通过原生 API 暴露了反应（Reactions）、编辑、撤回及群组管理等高级动作，标志着对苹果生态支持的进一步深化。
* **ACP 桥接层与任务账本稳定化**：ACP（Agent Control Protocol）实现了基于账本的完整会话重放，支持会话的持久化绑定与恢复。结合稳定的任务中心 RPC 接口（list/get/cancel），OpenClaw 作为中心调度器的状态管理能力得到了显著增强。

### 值得注意的修复

* **Windows 兼容性深度打磨**：解决了 Windows 环境下因 Developer Mode 限制导致的符号链接创建失败（改为使用 Junctions），并修复了 WebView2 桥接与终端窗口频繁闪烁的问题，极大提升了 Windows 用户的宿主体验。
* **模型配额与认证防护**：Google Gemini 默认接入改为更稳定的 Flash 模型以避免频繁触发配额限制；同时，系统增强了对敏感字段（如 Auth/Cookie 标头）的脱敏力度，并修复了多处因文件锁竞争（EBUSY/EPERM）导致的 SQLite 索引中断。
* **Telegram 大群组性能治理**：将回复链缓存从“全量重写”优化为“追加日志”模式，显著降低了在活跃大群组中的消息处理延迟和 CPU 占用。

### 个人评价

2026.5.9 版本显示出 OpenClaw 正在从功能扩张期进入“架构精细化”阶段。通过对底层网络请求、数组排序逻辑以及存储层原子性的深度优化，系统在高负载环境下的表现更加从容。特别是针对 Discord 和 iMessage 等主流渠道的协议级增强，证明了其在多模态 Agent 调度领域的领先地位。整体而言，这是一个侧重于鲁棒性、性能与开发者 SDK 标准化的成熟版本，为复杂生产环境下的 Agent 部署夯实了基础。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-10 08:29:42*
