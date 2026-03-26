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

*   **OpenAI 兼容性深度扩展**：网关层新增了 `/v1/models` 和 `/v1/embeddings` 接口，并支持在 `/v1/chat/completions` 中转发显式模型覆盖。这一改进显著提升了 OpenClaw 与现有 RAG 框架及第三方 AI 客户端的生态兼容性，使其能更无缝地作为 OpenAI API 的替代或增强网关使用。
*   **Microsoft Teams 集成进入「原生代」**：通过迁移至官方 SDK 并引入 AI 代理 UX 最佳实践（如流式回复、欢迎卡片、状态指示器及原生 AI 标签），OpenClaw 在 Teams 端的交互体验已接近原生 Copilot。同时，新增的消息编辑/删除支持及线索内回退逻辑，补齐了企业级通讯场景下的功能短板。
*   **技能（Skills）分发与安装流程重构**：引入了一键安装配方（recipes）和更直观的元数据管理。Control UI 现在的技能卡片支持按状态过滤，并提供了包含依赖检查、API Key 引导及源码链接的详情对话框。这种「从 missing 到 needs setup」的话术转变及安装自动化，大幅降低了开发者配置 coding-agent 或 trello 等技能的门槛。

### 值得注意的修复

*   **安全沙箱漏洞封堵**：修复了 `mediaUrl` 与 `fileUrl` 的别名绕过漏洞，防止外部工具或消息动作逃逸出预设的媒体根目录限制，强化了 `workspaceOnly` 策略的执行力度。
*   **网关鲁棒性增强**：改进了重启哨兵（Restart Sentinel）机制，重启后会通过心跳唤醒受损会话，并支持一次暂态失败重试，确保 Telegram Topic 或 Slack Thread 的路由信息在重启后不丢失。
*   **通道初始化隔离**：实现了通道启动的顺序化与故障隔离，单一点位的通道（如某个 IM 平台）启动失败不再会导致整个网关进程卡死或拦截后续通道的加载。

### 个人评价

2026.3.24 版本标志着 OpenClaw 正在从「功能堆砌」向「工程标准化」转型。通过兼容 OpenAI Embedding 规范和重构技能安装工作流，它进一步弱化了底层设施的复杂感，强化了作为 Agent 中间件的属性。同时，针对 Teams、Slack、Telegram 等主流通道的细碎修复，反映出该项目在处理跨平台长连接会话稳定性方面已进入深度打磨期。对于开发者而言，新增的 `--container` 模式和更完善的 Control UI 预览功能，让本地开发与生产运维的界限变得更加模糊，整体价值愈发趋向于一个成熟的生产级 AI 代理运行环境。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-26 12:48:13*
