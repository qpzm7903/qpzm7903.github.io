---
title: "🔧 Openclaw 更新日报 2026-03-26"
date: 2026-03-26T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.24

**发布日期**: 2026-03-26  
**⚠️ 新版本发布**

## Changes

- Gateway/OpenAI compatibility: add `/v1/models` and `/v1/embeddings`, and forward explicit model overrides through `/v1/chat/completions` and `/v1/responses` for broader client and RAG compatibility. Thanks @vincentkoc.
- Agents/tools: make `/tools` show the tools the current agent can actually use right now, add a compact default view with an optional detailed mode, and add a live "Available Right Now" section in the Control UI so it is easier to see what will work before you ask.
- Microsoft Teams: migrate to the official Teams SDK and add AI-agent UX best practices including streaming 1:1 replies, welcome cards with prompt starters, feedback/reflection, informative status updates, typing indicators, and native AI labeling. (#51808)
- Microsoft Teams: add message edit and delete support for sent messages, including in-thread fallbacks when no explicit target is provided. (#49925)
- Skills/install metadata: add one-click install recipes to bundled skills (coding-agent, gh-issues, openai-whisper-api, session-logs, tmux, trello, weather) so the CLI and Control UI can offer dependency installation when requirements are missing. (#53411) Thanks @BunsDev.
- Control UI/skills: add status-filter tabs (All / Ready / Needs Setup / Disabled) with counts, replace inline skill cards with a click-to-detail dialog showing requirements, toggle switch, install action, API key entry, source metadata, and homepage link. (#53411) Thanks @BunsDev.
- Slack/interactive replies: restore rich reply parity for direct deliveries, auto-render simple trailing `Options:` lines as buttons/selects, improve Slack interactive setup defaults, and isolate reply controls from plugin interactive handlers. (#53389) Thanks @vincentkoc.
- CLI/containers: add `--container` and `OPENCLAW_CONTAINER` to run `openclaw` commands inside a running Docker or Podman OpenClaw container. (#52651) Thanks @sallyom.
- Discord/auto threads: add optional `autoThreadName: "generated"` naming so new auto-created threads can be renamed asynchronously with concise LLM-generated titles while keeping the existing message-based naming as the default. (#43366) Thanks @davidguttman.
- Plugins/hooks: add `before_dispatch` with canonical inbound metadata and route handled replies through the normal final-delivery path, preserving TTS and routed delivery semantics. (#50444) Thanks @gfzhx.
- Control UI/agents: convert agent workspace file rows to expandable `<details>` with lazy-loaded inline markdown preview, and add comprehensive `.sidebar-markdown` styles for headings, lists, code blocks, tables, blockquotes, and details/summary elements. (#53411) Thanks @BunsDev.
- Control UI/markdown preview: restyle the agent workspace file preview dialog with a frosted backdrop, sized panel, and styled header, and integrate `@create-markdown/preview` v2 system theme for rich markdown rendering (headings, tables, code blocks, callouts, blockquotes) that auto-adapts to the app's light/dark design tokens. (#53411) Thanks @BunsDev.

## Fixes

- Outbound media/local files: align outbound media access with the configured fs policy so host-local files and inbound-media paths keep sending when `workspaceOnly` is off, while strict workspace-only agents remain sandboxed.
- Security/sandbox media dispatch: close the `mediaUrl`/`fileUrl` alias bypass so outbound tool and message actions cannot escape media-root restrictions. (#54034)
- Gateway/restart sentinel: wake the interrupted agent session via heartbeat after restart instead of only sending a best-effort restart note, retry outbound delivery once on transient failure, and preserve explicit thread/topic routing through the wake path so replies land in the correct Telegram topic or Slack thread. (#53940) Thanks @VACInc.
- Docker/setup: avoid the pre-start `openclaw-cli` shared-network namespace loop by routing setup-time onboard/config writes through `openclaw-gateway`, so fresh Docker installs stop failing before the gateway comes up. (#53385) Thanks @amsminn.
- Gateway/channels: keep channel startup sequential while isolating per-channel boot failures, so one broken channel no longer blocks later channels from starting. (#54215) Thanks @JonathanJing.
- Embedded runs/secrets: stop unresolved `SecretRef` config from crashing embedded agent runs by falling back to the resolved runtime snapshot when needed. Fixes #45838.
- WhatsApp/groups: track recent gateway-sent message IDs and suppress only matching group echoes, preserving owner `/status`, `/new`, and `/activation` commands from linked-account `fromMe` traffic. (#53624) Thanks @w-sss.
- WhatsApp/reply-to-bot detection: restore implicit group reply detection by unwrapping `botInvokeMessage` payloads and reading `selfLid` from `creds.json`, so reply-based mentions reach the bot again in linked-account group chats.
- Telegram/forum topics: recover `#General` topic `1` routing when Telegram omits forum metadata, including native commands, interactive callbacks, inbound message context, and fallback error replies. (#53699) thanks @huntharo
- Discord/gateway supervision: centralize gateway error handling behind a lifetime-owned supervisor so early, active, and late-teardown Carbon gateway errors stay classified consistently and stop surfacing as process-killing teardown crashes.
- Discord/timeouts: send a visible timeout reply when the inbound Discord worker times out before a final reply starts, including created auto-thread targets and queued-run ordering. (#53823) Thanks @Kimbo7870.
- ACP/direct chats: always deliver a terminal ACP result when final TTS does not yield audio, even if block text already streamed earlier, and skip redundant empty-text final synthesis. (#53692) Thanks @w-sss.


---

## 💡 深度点评

### 核心亮点

*   **网关层 OpenAI 兼容性增强**：新增 `/v1/models` 和 `/v1/embeddings` 端点，并支持通过 `/v1/chat/completions` 透传模型覆盖参数。这一改动显著提升了 OpenClaw 与现有 RAG 框架及第三方客户端的集成能力，使其能更无缝地接入标准 AI 生态。
*   **Skill 生态安装工程化**：引入了「一键安装」配方（Recipe）及依赖预检机制。CLI 与 Control UI 现在能自动识别缺失依赖并引导安装，配合新增的「状态过滤」标签（Ready / Needs Setup 等），大幅降低了复杂 Skill（如 coding-agent, openai-whisper-api）的部署门槛。
*   **企业级通信集成深度演进**：Microsoft Teams 迁移至官方 SDK，并补齐了流式回复、原生 AI 标签、欢迎卡片及消息编辑/删除等关键交互特性；同时 Slack 恢复了富文本回复对齐，并支持自动将文本选项渲染为交互按钮，生产环境的沟通体验更趋近原生。

### 值得注意的修复

*   **安全沙箱强化**：修补了通过 `mediaUrl` / `fileUrl` 别名绕过媒体根目录限制的漏洞，确保受限 Agent 无法访问工作区外的本地文件，强化了多租户环境下的数据安全性。
*   **启动稳定性优化**：重构了 Docker 环境下的初始化逻辑，解决了 `openclaw-cli` 在网关就绪前的网络命名空间循环等待问题；同时将渠道（Channels）启动改为顺序加载且异常隔离，避免单一渠道失效导致整个系统无法启动。
*   **媒体传输鲁棒性**：针对 Telegram 增加了照片尺寸与比例的预检逻辑，当不符合 Telegram 原生规则时自动回退至文档传输模式，解决了长久以来的 `PHOTO_INVALID_DIMENSIONS` 上传失败问题。

### 个人评价

2026.3.24 版本展示了 OpenClaw 从「功能堆砌」向「操作卓越」转型的趋势。通过强化 OpenAI 标准 API 兼容性和 Skill 依赖自动化管理，开发者接入与维护的成本被进一步压缩。同时，针对 Teams、Slack、Discord 等主流平台的交互修补，表明该项目正致力于在复杂生产环境下提供更稳定、更符合人类直觉的 AI 助手体验。整体而言，这是一个侧重于稳定交付与生态对齐的权重更新。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-26 12:47:48*
