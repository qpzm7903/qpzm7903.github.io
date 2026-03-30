---
title: "🔧 Openclaw 更新日报 2026-03-30"
date: 2026-03-30T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.28

**发布日期**: 2026-03-30  
**⚠️ 新版本发布**

## Breaking

- Providers/Qwen: remove the deprecated `qwen-portal-auth` OAuth integration for `portal.qwen.ai`; migrate to Model Studio with `openclaw onboard --auth-choice modelstudio-api-key`. (#52709) Thanks @pomelo-nwu.
- Config/Doctor: drop automatic config migrations older than two months; very old legacy keys now fail validation instead of being rewritten on load or by `openclaw doctor`.

## Changes

- xAI/tools: move the bundled xAI provider to the Responses API, add first-class `x_search`, and auto-enable the xAI plugin from owned web-search and tool config so bundled Grok auth/configured search flows work without manual plugin toggles. (#56048) Thanks @huntharo.
- xAI/onboarding: let the bundled Grok web-search plugin offer optional `x_search` setup during `openclaw onboard` and `openclaw configure --section web`, including an x_search model picker with the shared xAI key.
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

## Fixes

- Agents/Anthropic: recover unhandled provider stop reasons (e.g. `sensitive`) as structured assistant errors instead of crashing the agent run. (#56639)
- Google/models: resolve Gemini 3.1 pro, flash, and flash-lite for all Google provider aliases by passing the actual runtime provider ID and adding a template-provider fallback; fix flash-lite prefix ordering. (#56567)
- OpenAI Codex/image tools: register Codex for media understanding and route image prompts through Codex instructions so image analysis no longer fails on missing provider registration or missing `instructions`. (#54829) Thanks @neeravmakwana.
- Agents/image tool: restore the generic image-runtime fallback when no provider-specific media-understanding provider is registered, so image analysis works again for providers like `openrouter` and `minimax-portal`. (#54858) Thanks @MonkeyLeeT.
- WhatsApp: fix infinite echo loop in self-chat DM mode where the bot's own outbound replies were re-processed as new inbound user messages. (#54570) Thanks @joelnishanth
- Telegram/splitting: replace proportional text estimate with verified HTML-length search so long messages split at word boundaries instead of mid-word; gracefully degrade when tag overhead exceeds the limit. (#56595)
- Telegram/delivery: skip whitespace-only and hook-blanked text replies in bot delivery to prevent GrammyError 400 empty-text crashes. (#56620)
- Telegram/send: validate `replyToMessageId` at all four API sinks with a shared normalizer that rejects non-numeric, NaN, and mixed-content strings. (#56587)
- Approvals/UI: keep the newest pending approval at the front of the Control UI queue so approving one request does not accidentally target an older expired id. Thanks @vincentkoc.
- Plugin approvals: accept unique short approval-id prefixes on `plugin.approval.resolve`, matching exec approvals and restoring `/approve` fallback flows on chat approval surfaces. Thanks @vincentkoc.
- Mistral: normalize OpenAI-compatible request flags so official Mistral API runs no longer fail with remaining `422 status code (no body)` chat errors.
- Control UI/config: keep sensitive raw config hidden by default, replace the blank blocked editor with an explicit reveal-to-edit state, and restore raw JSON editing without auto-exposing secrets. Fixes #55322.


---

## 💡 深度点评

这是针对 openclaw 2026.3.28 版本的深度技术点评：

### 核心亮点

*   **插件钩子与交互式审批（requireApproval）**：插件系统的 `before_tool_call` 钩子现在支持异步 `requireApproval`。这意味着插件可以在工具执行前暂停任务，并通过 Telegram 按钮、Discord 交互或 CLI 的 `/approve` 命令请求人工干预。这种「人在回路」（Human-in-the-loop）的机制显著增强了 Agent 在执行敏感操作时的安全性与可控性。
*   **ACP 频道绑定与工作区一体化**：新增对 Discord、BlueBubbles 和 iMessage 的当前会话 ACP 绑定支持。通过 `/acp spawn codex --bind here`，开发者可以将当前的 IM 聊天窗口直接转化为一个 Codex 驱动的工作区，无需创建子线程。这打破了聊天界面与运行时工作区之间的隔阂，实现了更自然的开发流转。
*   **基础设施的统一与插件化**：该版本将 Claude CLI、Codex CLI 和 Gemini CLI 的推理默认值移至插件层，并统一了 `--cli-backend-logs` 标志。同时，跨平台的垂直文件操作也被归并至 `upload-file` 动作下（覆盖 Slack、Teams 和 Google Chat）。这种底层架构的收敛，降低了维护多平台机器人时的配置复杂度。

### 值得注意的修复

*   **长消息处理与交付优化**：Telegram 弃用了基于字符比例的粗略估算，转而使用验证 HTML 长度的搜索算法，确保消息在单词边界处正确拆分；同时修复了 WhatsApp 在自聊模式下的无限回声循环 Bug。
*   **模型路由与容错增强**：修复了 Gemini 3.1 系列（Pro/Flash/Flash-lite）的运行时 ID 解析问题；针对 Anthropic 引入了 provider 停止原因（如 `sensitive`）的结构化错误恢复，避免 Agent 运行崩溃；此外，Ollama 现在支持通过 `thinkingLevel=off` 参数直接关闭具思考能力模型的推理过程。
*   **连接性与稳定性**：重构了 Discord 网关的重连逻辑，强制清理陈旧的 WebSocket 状态，解决了在某些网络环境下死循环尝试重连的毒化问题；同时优化了 macOS 下 SQLite 的瞬态错误处理，防止 LaunchAgent 进入崩溃重启循环。

### 个人评价

2026.3.28 版本标志着 openclaw 从「功能堆砌」向「架构精炼」的转型。通过将核心推理后端逻辑移至插件面，并引入跨频道的统一审批机制，项目在模块化和安全性上有了质的提升。对于深度用户而言，ACP 频道绑定和内存压缩逻辑的优化，直接解决了长会话开发场景下的痛点。整体来看，这是一个侧重于工程健壮性、旨在打通多平台协作壁垒的稳健更新。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-30 08:01:19*
