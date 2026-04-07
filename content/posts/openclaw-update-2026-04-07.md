---
title: "🔧 Openclaw 更新日报 2026-04-07"
date: 2026-04-07T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.5

**发布日期**: 2026-04-07  
**⚠️ 新版本发布**

## Breaking

- Config: remove legacy public config aliases such as `talk.voiceId` / `talk.apiKey`, `agents.*.sandbox.perSession`, `browser.ssrfPolicy.allowPrivateNetwork`, `hooks.internal.handlers`, and channel/group/room `allow` toggles in favor of the canonical public paths and `enabled`, while keeping load-time compatibility and `openclaw doctor --fix` migration support for existing configs. (#60726) Thanks @vincentkoc.

## Changes

- Agents/video generation: add the built-in `video_generate` tool so agents can create videos through configured providers and return the generated media directly in the reply.
- Agents/music generation: ignore unsupported optional hints such as `durationSeconds` with a warning instead of hard-failing requests on providers like Google Lyria.
- Providers/Arcee AI: add a bundled Arcee AI provider plugin with `ARCEEAI_API_KEY` onboarding, Trinity model catalog (mini, large-preview, large-thinking), OpenAI-compatible API support, and OpenRouter as an alternative auth path. (#62068) Thanks @arthurbr11.
- Providers/ComfyUI: add a bundled `comfy` workflow media plugin for local ComfyUI and Comfy Cloud workflows, including shared `image_generate`, `video_generate`, and workflow-backed `music_generate` support, with prompt injection, optional reference-image upload, live tests, and output download.
- Tools/music generation: add the built-in `music_generate` tool with bundled Google (Lyria) and MiniMax providers plus workflow-backed Comfy support, including async task tracking and follow-up delivery of finished audio.
- Providers: add bundled Qwen, Fireworks AI, and StepFun providers, plus MiniMax TTS, Ollama Web Search, and MiniMax Search integrations for chat, speech, and search workflows. (#60032, #55921, #59318, #54648)
- Providers/Amazon Bedrock: add bundled Mantle support plus inference-profile discovery and automatic request-region injection so Bedrock-hosted Claude, GPT-OSS, Qwen, Kimi, GLM, and similar routes work with less manual setup. (#61296, #61299) Thanks @wirjo.
- Control UI/multilingual: add localized control UI support for Simplified Chinese, Traditional Chinese, Brazilian Portuguese, German, Spanish, Japanese, Korean, French, Turkish, Indonesian, Polish, and Ukrainian. Thanks @vincentkoc.
- Plugins: add plugin-config TUI prompts to guided onboarding/setup flows, and add `openclaw plugins install --force` so existing plugin and hook-pack targets can be replaced without using the dangerous-code override flag. (#60590, #60544)
- Control UI/skills: add ClawHub search, detail, and install flows directly in the Skills panel. (#60134) Thanks @samzong.
- iOS/exec approvals: add generic APNs approval notifications that open an in-app exec approval modal, fetch command details only after authenticated operator reconnect, and clear stale notification state when the approval resolves. (#60239) Thanks @ngutman.
- Matrix/exec approvals: add Matrix-native exec approval prompts with account-scoped approvers, channel-or-DM delivery, and room-thread aware resolution handling. (#58635) Thanks @gumadeiras.

## Fixes

- Control UI/chat: show `/tts` and other local audio-only slash replies in webchat by embedding local audio in the assistant message and rendering `<audio>` controls instead of dropping empty-text finals. Fixes #61564. (#61598) Thanks @neeravmakwana.
- Security: preserve restrictive plugin-only tool allowlists, require owner access for `/allowlist add` and `/allowlist remove`, fail closed when `before_tool_call` hooks crash, block browser SSRF redirect bypasses earlier, and keep non-interactive auth-choice inference scoped to bundled and already-trusted plugins. (#58476, #59836, #59822, #58771, #59120) Thanks @eleqtrizit and @pgondhi987.
- Providers/OpenAI: make GPT-5 and Codex runs act sooner with lower-verbosity defaults, visible progress during tool work, and a one-shot retry when a turn only narrates the plan instead of taking action.
- Providers/OpenAI and reply delivery: preserve native `reasoning.effort: "none"` and strict schemas where supported, add GPT-5.4 assistant `phase` metadata across replay and the Gateway `/v1/responses` layer, and keep commentary buffered until `final_answer` so web chat, session previews, embedded replies, and Telegram partials stop leaking planning text. Fixes #59150, #59643, #61282.
- Telegram: fix current-model checks in the model picker, HTML-format non-default `/model` confirmations, explicit topic replies, persisted reaction ownership across restarts, caption-media placeholder and `file_id` preservation on download failure, and upgraded-install inbound image reads. (#60384, #60042, #59634, #59207, #59948, #59971) Thanks @sfuminya, @GitZhangChi, @dashhuang, @samzong, @v1p0r, and @neeravmakwana.
- Telegram: restore DM voice-note preflight transcription so direct-message audio stops arriving as raw `<media:audio>` placeholders. (#61008) Thanks @manueltarouca.
- Telegram/reasoning: only create a Telegram reasoning preview lane when the session is explicitly `reasoning:stream`, so hidden `<think>` traces from streamed replies stop surfacing as chat previews on normal sessions. Thanks @vincentkoc.
- Telegram/native command menu: trim long menu descriptions before dropping commands so sub-100 command sets can still fit Telegram's payload budget and keep more `/` entries visible. (#61129) Thanks @neeravmakwana.
- Telegram/startup: bound `deleteWebhook`, `getMe`, and `setWebhook` startup requests while keeping the longer `getUpdates` poll timeout, so wedged Telegram control-plane calls stop hanging startup indefinitely. (#61601) Thanks @neeravmakwana.
- Agents/failover: classify Anthropic "extra usage" exhaustion as billing so same-turn model fallback still triggers when Claude blocks long-context requests on usage limits. (#61608) Thanks @neeravmakwana.
- Discord: keep REST, webhook, and monitor traffic on the configured proxy, preserve component-only media sends, honor `@everyone` and `@here` mention gates, keep ACK reactions on the active account, and split voice connect/playback timeouts so auto-join is more reliable. (#57465, #60361, #60345) Thanks @geekhuashan.
- Discord/reply tags: strip leaked `[[reply_to_current]]` control tags from preview text and honor explicit reply-tag threading during final delivery, so Discord replies stay attached to the triggering message instead of printing reply metadata into chat.


---

## 💡 深度点评

这是一篇关于 OpenClaw 2026.4.5 更新内容的深度点评：

### 核心亮点

*   **多模态生成能力的深度工具化**
    本版本正式引入了 `video_generate` 和 `music_generate` 内置工具，支持 Agent 直接调用。值得关注的是对 **ComfyUI 工作流插件** 的整合，它允许开发者将本地或云端的 ComfyUI 工作流（包括 prompt 注入、参考图上传）直接接入 Agent，实现从单一模型调用向复杂 AIGC 工作流的跨越。此外，集成了 Google Lyria、MiniMax、Runway 以及 Alibaba Wan 等主流多模态模型，完善了从生成到异步任务追踪的闭环。
*   **实验性“梦境”记忆系统（Memory Dreaming）**
    这是对 Agent 长期记忆架构的一次重大重塑。该功能将记忆晋升分为轻度、深度和 REM 三个协作阶段，通过异步处理将短期对话碎片提炼为 `dreams.md` 中的持久知识。这种模拟人类睡眠的记忆固化机制，配合加权短期回溯和 conceptual tagging，有效解决了长周期运行下 Agent 知识冗余与关键信息遗忘的权衡问题。
*   **提示词缓存（Prompt Caching）的极致优化**
    针对长上下文场景，OpenClaw 进行了底层的工程优化。通过标准化系统提示词指纹（处理空白符、换行符等差异）、实现 **MCP 工具排序确定性**，并从系统提示词中移除了重复的带内工具声明，强制模型依赖结构化定义。这些改动显著提升了 KV Cache 的重用率，直接降低了多轮对话的延迟与 Token 成本。

### 值得注意的修复

*   **推理链路隔离与隐私保护**：修复了在 Telegram 和飞书等频道中 `<think>` 思考标签外泄的问题，现在仅在显式开启 `reasoning:stream` 时才会显示推理过程，保证了普通对话界面的整洁。
*   **安全性加固**：修补了多个关键安全漏洞，包括插件工具白名单绕过、浏览器 SSRF 重定向规避，以及设备配对过程中的 Token 劫持风险，进一步收紧了 `exec` 执行策略。
*   **跨平台交付稳定性**：解决了 Discord 生成图片路径丢失、Telegram 语音消息预检转录失效以及 iOS/Matrix 原生审批流状态清理不及时等影响生产体验的边缘 Case。

### 个人评价

OpenClaw 2026.4.5 是一个从“交互式助手”向“生产级自主智能体”转化的关键版本。它不仅在多模态生成上提供了更灵活的插件化方案，更通过“梦境系统”和“缓存一致性优化”在架构层面尝试解决 Agent 的智力稳定性与成本问题。对于开发者而言，这不仅是功能堆砌，更是对 Agent 底层运行机制的一次深度打磨，整体价值导向非常明确：追求更高的工程可靠性与长周期任务处理能力。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-07 08:00:59*
