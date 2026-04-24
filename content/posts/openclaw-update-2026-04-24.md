---
title: "🔧 Openclaw 更新日报 2026-04-24"
date: 2026-04-24T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.22

**发布日期**: 2026-04-24  
**⚠️ 新版本发布**

## Changes

- Providers/xAI: add image generation, text-to-speech, and speech-to-text support, including `grok-imagine-image` / `grok-imagine-image-pro`, reference-image edits, six live xAI voices, MP3/WAV/PCM/G.711 TTS formats, `grok-stt` audio transcription, and xAI realtime transcription for Voice Call streaming. (#68694) Thanks @KateWilkins.
- Providers/STT: add Voice Call streaming transcription for Deepgram, ElevenLabs, and Mistral, alongside the existing OpenAI and xAI realtime STT paths; ElevenLabs also gains Scribe v2 batch audio transcription for inbound media.
- TUI: add local embedded mode for running terminal chats without a Gateway while keeping plugin approval gates enforced. (#66767) Thanks @fuller-stack-dev.
- Onboarding: auto-install missing provider and channel plugins during setup so first-run configuration can complete without manual plugin recovery.
- OpenAI/Responses: use OpenAI's native `web_search` tool automatically for direct OpenAI Responses models when web search is enabled and no managed search provider is pinned; explicit providers such as Brave keep the managed `web_search` tool.
- Models/commands: add `/models add <provider> <modelId>` so you can register a model from chat and use it without restarting the gateway; keep `/models` as a simple provider browser while adding clearer add guidance and copy-friendly command examples. (#70211) Thanks @Takhoffman.
- WhatsApp: add configurable native reply quoting with replyToMode for WhatsApp conversations. Thanks @mcaxtr.
- WhatsApp/groups+direct: forward per-group and per-direct `systemPrompt` config into inbound context `GroupSystemPrompt` so configured per-chat behavioral instructions are injected on every turn. Supports `"*"` wildcard fallback and account-scoped overrides under `channels.whatsapp.accounts.<id>.{groups,direct}`; account maps fully replace root maps (no deep merge), matching the existing `requireMention` pattern. Closes #7011. (#59553) Thanks @Bluetegu.
- Agents/sessions: add mailbox-style `sessions_list` filters for label, agent, and search plus visibility-scoped derived title and last-message previews. (#69839) Thanks @dangoZhang.
- Control UI/settings+chat: add a browser-local personal identity for the operator (name plus local-safe avatar), route user identity rendering through the shared chat/avatar path used by assistant and agent surfaces, and tighten Quick Settings, agent fallback chips, and narrow-screen chat layouts so personalization no longer wastes space or clips controls. (#70362) Thanks @BunsDev.
- Gateway/diagnostics: enable payload-free stability recording by default and add a support-ready diagnostics export with sanitized logs, status, health, config, and stability snapshots for bug reports. (#70324) Thanks @gumadeiras.
- Agents/trajectory export: add default-on local trajectory capture plus `/export-trajectory` bundles with redacted transcripts, runtime events, prompts, metadata, and artifacts for reproducible debugging and dataset export. (#70291) Thanks @scoootscooob.

## Fixes

- CLI/Gateway: wait for one-shot gateway RPC clients to finish WebSocket teardown before the CLI process exits, reducing hangs where commands like `openclaw status` or `openclaw version` could finish their work but stay alive until an external timeout killed them.
- Thinking defaults/status: raise the implicit default thinking level for reasoning-capable models from legacy `off`/`low` fallback behavior to a safe provider-supported `medium` equivalent when no explicit config default is set, preserve configured-model reasoning metadata when runtime catalog loading is empty, and make `/status` report the same resolved default as runtime.
- Gateway/model pricing: fetch OpenRouter and LiteLLM pricing asynchronously at startup and extend catalog fetch timeouts to 30 seconds, reducing noisy timeout warnings during slow upstream responses.
- Agents/failover: classify bare undici transport failures (`terminated`, `UND_ERR_SOCKET`, `UND_ERR_CONNECT_TIMEOUT`, body/header timeouts, aborted streams) and pi-ai's openai-codex `Request failed` sentinel as `timeout`, so Cloudflare 502s with empty bodies and mid-response socket resets actually enter the configured fallback chain instead of surfacing as unclassified errors. Fixes #69368. (#69677) Thanks @sk7n4k3d.
- Providers/Anthropic Vertex: restore ADC-backed model discovery after the lightweight provider-discovery path by resolving emitted discovery entries, exposing synthetic auth on bootstrap discovery, and honoring copied env snapshots when probing the default GCP ADC path. Fixes #65715. (#65716) Thanks @feiskyer.
- Plugins/install: add newly installed plugin ids to an existing `plugins.allow` list before enabling them, so allowlisted configs load installed plugins after restart.
- Status: show `Fast` in `/status` when fast mode is enabled, including config/default-derived fast mode, and omit it when disabled.
- OpenAI/image generation: detect Azure OpenAI-style image endpoints, use Azure `api-key` auth plus deployment-scoped image URLs, and honor `AZURE_OPENAI_API_VERSION` so image generation and edits work against Azure-hosted OpenAI resources. (#70570) Thanks @zhanggpcsu.
- Control UI/chat: include cache-read and cache-write tokens when computing the message footer context percentage, so cached Claude/OpenAI sessions no longer show `0% ctx` while `/status` reports substantial context use. Fixes #70491. (#70532) Thanks @chen-zhang-cs-code.
- Models/auth: merge provider-owned default-model additions from `openclaw models auth login` instead of replacing `agents.defaults.models`, so re-authenticating an OAuth provider such as OpenAI Codex no longer wipes other providers' aliases and per-model params. Migrations that must rename keys (Anthropic -> Claude CLI) opt in with `replaceDefaultModels`. Fixes #69414. (#70435) Thanks @neeravmakwana.
- Media understanding/audio: prefer configured or key-backed STT providers before auto-detected local Whisper CLIs, so installed local transcription tools no longer shadow API providers such as Groq/OpenAI in `tools.media.audio` auto mode. Fixes #68727.
- Providers/OpenAI: lock the auth picker wording for OpenAI API key, Codex browser login, and Codex device pairing so the setup choices no longer imply a mixed Codex/API-key auth path. (#67848) Thanks @tmlxrd.


---

## 💡 深度点评

这份 openclaw 2026.4.22 的更新日志显示，该版本在多模态扩展、插件加载效率以及长连接稳定性方面进行了针对性的增强。以下是本次更新的深度点评：

### 核心亮点

*   **多模态与实时交互能力全面升级**：新增了对 xAI 全栈能力的支持，包括图像生成（Grok-imagine）、语音合成（TTS）及实时转录（STT）。同时，Voice Call 实时转录扩展至 Deepgram、ElevenLabs 和 Mistral，标志着 openclaw 在处理实时语音流交互方面已具备更强的供应商适配性。
*   **架构性能与本地化增强**：TUI 新增了本地嵌入模式（local embedded mode），允许在无需启动 Gateway 的情况下运行终端对话，并保留插件审批门禁。此外，引入 Jiti 加载机制后，内置插件的加载速度显著提升了 82-90%，极大地优化了 CLI 的启动响应。
*   **动态模型管理与工具集成**：新增 `/models add` 命令，支持在不重启 Gateway 的情况下动态注册模型。在工具链方面，原生集成了 tokenjuice 插件以压缩冗余的工具执行结果，并针对 OpenAI 模型启用了原生 `web_search` 支持，提升了检索任务的效率。

### 值得注意的修复

*   **长连接与进程退出稳定性**：修复了 CLI/Gateway 在退出时因 WebSocket 关闭等待导致的挂起问题，确保了 `status` 或 `version` 命令在完成后能立即释放进程。
*   **Agent 复杂对话逻辑修正**：解决了 Moonshot (Kimi) 在工具调用时 ID 被过度净化导致的对话中断问题（Fix #62319），并优化了推理模型（Reasoning models）的默认思考等级（Thinking level）至中等，确保了复杂逻辑任务的输出质量。
*   **消息传递可靠性**：针对 WhatsApp 修复了在并发连接重连时可能导致的重复发送问题（多达 7-12 次），通过内存锁机制保证了高并发下的消息幂等性。

### 个人评价

2026.4.22 版本是一个从「功能堆砌」转向「工程精细化」的里程碑。通过 Jiti 优化和本地嵌入模式，openclaw 显著降低了开发者在本地调试时的性能损耗；而对 xAI 及多种 STT 供应商的深度整合，进一步拓宽了其在实时交互领域的应用边界。整体来看，该版本在保持多模型兼容性的同时，将重心放在了提升 Agent 运行的稳健性与响应速度上，是近期技术价值最高的小版本更新之一。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-24 08:02:40*
