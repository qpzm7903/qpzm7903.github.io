---
title: "🔧 Openclaw 更新日报 2026-03-29"
date: 2026-03-29T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.28-beta.1

**发布日期**: 2026-03-29  
**⚠️ 新版本发布**

## Breaking

- Providers/Qwen: remove the deprecated `qwen-portal-auth` OAuth integration for `portal.qwen.ai`; migrate to Model Studio with `openclaw onboard --auth-choice modelstudio-api-key`. (#52709) Thanks @pomelo-nwu.
- Config/Doctor: drop automatic config migrations older than two months; very old legacy keys now fail validation instead of being rewritten on load or by `openclaw doctor`.

## Changes

- xAI/tools: move the bundled xAI provider to the Responses API, add first-class `x_search`, and auto-enable the xAI plugin from owned web-search and tool config so bundled Grok auth/configured search flows work without manual plugin toggles. (#56048) Thanks @huntharo.
- MiniMax: add image generation provider for `image-01` model, supporting generate and image-to-image editing with aspect ratio control. (#54487) Thanks @liyuan97.
- Plugins/hooks: add async `requireApproval` to `before_tool_call` hooks, letting plugins pause tool execution and prompt the user for approval via the exec approval overlay, Telegram buttons, Discord interactions, or the `/approve` command on any channel. The `/approve` command now handles both exec and plugin approvals with automatic fallback. (#55339) Thanks @vaclavbelak and @joshavant.
- ACP/channels: add current-conversation ACP binds for Discord, BlueBubbles, and iMessage so `/acp spawn codex --bind here` can turn the current chat into a Codex-backed workspace without creating a child thread, and document the distinction between chat surface, ACP session, and runtime workspace.
- OpenAI/apply_patch: enable `apply_patch` by default for OpenAI and OpenAI Codex models, and align its sandbox policy access with `write` permissions.
- Plugins/CLI backends: move bundled Claude CLI, Codex CLI, and Gemini CLI inference defaults onto the plugin surface, add bundled Gemini CLI backend support, and replace `gateway run --claude-cli-logs` with generic `--cli-backend-logs` while keeping the old flag as a compatibility alias.
- Plugins/startup: auto-load bundled provider and CLI-backend plugins from explicit config refs, so bundled Claude CLI, Codex CLI, and Gemini CLI message-provider setups no longer need manual `plugins.allow` entries.
- Podman: simplify the container setup around the current rootless user, install the launch helper under `~/.local/bin`, and document the host-CLI `openclaw --container <name> ...` workflow instead of a dedicated `openclaw` service user.
- Slack/tool actions: add an explicit `upload-file` Slack action that routes file uploads through the existing Slack upload transport, with optional filename/title/comment overrides for channels and DMs.
- Message actions/files: start unifying file-first sends on the canonical `upload-file` action by adding explicit support for Microsoft Teams and Google Chat, and by exposing BlueBubbles file sends through `upload-file` while keeping the legacy `sendAttachment` alias.
- Plugins/Matrix TTS: send auto-TTS replies as native Matrix voice bubbles instead of generic audio attachments. (#37080) thanks @Matthew19990919.
- CLI: add `openclaw config schema` to print the generated JSON schema for `openclaw.json`. (#54523) Thanks @kvokka.

## Fixes

- Agents/Anthropic: recover unhandled provider stop reasons (e.g. `sensitive`) as structured assistant errors instead of crashing the agent run. (#56639)
- Google/models: resolve Gemini 3.1 pro, flash, and flash-lite for all Google provider aliases by passing the actual runtime provider ID and adding a template-provider fallback; fix flash-lite prefix ordering. (#56567)
- OpenAI Codex/image tools: register Codex for media understanding and route image prompts through Codex instructions so image analysis no longer fails on missing provider registration or missing `instructions`. (#54829) Thanks @neeravmakwana.
- Agents/image tool: restore the generic image-runtime fallback when no provider-specific media-understanding provider is registered, so image analysis works again for providers like `openrouter` and `minimax-portal`. (#54858) Thanks @MonkeyLeeT.
- WhatsApp: fix infinite echo loop in self-chat DM mode where the bot's own outbound replies were re-processed as new inbound user messages. (#54570) Thanks @joelnishanth
- Telegram/splitting: replace proportional text estimate with verified HTML-length search so long messages split at word boundaries instead of mid-word; gracefully degrade when tag overhead exceeds the limit. (#56595)
- Telegram/delivery: skip whitespace-only and hook-blanked text replies in bot delivery to prevent GrammyError 400 empty-text crashes. (#56620)
- Telegram/send: validate `replyToMessageId` at all four API sinks with a shared normalizer that rejects non-numeric, NaN, and mixed-content strings. (#56587)
- Mistral: normalize OpenAI-compatible request flags so official Mistral API runs no longer fail with remaining `422 status code (no body)` chat errors.
- Control UI/config: keep sensitive raw config hidden by default, replace the blank blocked editor with an explicit reveal-to-edit state, and restore raw JSON editing without auto-exposing secrets. Fixes #55322.
- CLI/zsh: defer `compdef` registration until `compinit` is available so zsh completion loads cleanly with plugin managers and manual setups. (#56555)
- BlueBubbles/debounce: guard debounce flush against null message text by sanitizing at the enqueue boundary and adding an independent combiner guard. (#56573)


---

## 💡 深度点评

OpenClaw 2026.3.28-beta.1 版本发布，这次更新在架构一致性和交互安全性上迈出了重要一步。以下是针对该版本的深度点评：

### 核心亮点

*   **插件 Hook 引入异步审批流 (`requireApproval`)**：这是本版本最具生产价值的改进。通过在 `before_tool_call` 钩子中支持 `requireApproval`，插件现在可以中断工具执行并跨平台（Telegram、Discord、/approve 命令等）请求用户授权。这一机制为 Agent 的“人在回路”（Human-in-the-Loop）操作提供了标准化的底层支持，大幅提升了自动化工具的可控性。
*   **ACP 通道绑定深度集成**：新增了对 Discord、BlueBubbles 和 iMessage 的当前对话绑定（Current-conversation binds）。用户可以通过 `/acp spawn --bind here` 直接将当前聊天窗口转化为 Codex 工作空间，而无需创建子线程。这种对聊天表面（Chat Surface）与运行时工作空间（Runtime Workspace）权重的重新定义，进一步模糊了即时通讯与开发环境的边界。
*   **跨平台文件发送操作标准化**：版本开始通过 `upload-file` 动作统一各通道的文件发送逻辑，新增了对 Microsoft Teams 和 Google Chat 的支持，并为 Slack 提供了显式的传输路由。这种接口层面的收敛降低了开发者在多端部署 Agent 时处理媒体附件的复杂度。

### 值得注意的修复

*   **模型思维链控制优化**：针对 Ollama 模型，通过 `thinkingLevel=off` 显式路由 `think: false` 到底层扩展，解决了以往模型可能在后台静默生成隐藏推理 Token 的问题。
*   **Agent 稳定性与容错**：修复了 Anthropic 供应方因敏感内容停止（stop reason: `sensitive`）导致 Agent 崩溃的问题，将其改为结构化助手错误；同时解决了 WhatsApp 在自聊模式下可能产生的无限循环回复 Bug。
*   **安全性增强**：扩展了 Web Search 密钥审计范围，现在能够识别并保护 Gemini、xAI (Grok)、Kimi 等多个主流供应方的凭据，有效防止敏感 Key 泄露到日志或交互界面。

### 个人评价

2026.3.28-beta.1 是一个侧重于“精细化控制”与“架构收敛”的里程碑。通过引入异步审批钩子和统一文件传输接口，OpenClaw 正在从单纯的自动化工具向更安全的协作智能体框架演进。特别是对多通道 ACP 绑定的优化，反映了其在保持跨平台灵活性的同时，致力于提供更原生、更低摩擦的用户体验。整体而言，该版本显著增强了 Agent 在复杂生产环境中的作业可靠性。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-29 08:00:50*
