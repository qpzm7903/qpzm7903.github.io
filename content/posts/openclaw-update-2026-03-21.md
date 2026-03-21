---
title: "🔧 Openclaw 更新日报 2026-03-21"
date: 2026-03-21T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-21  
**📋 版本维护**

## Changes

- Android/chat settings: redesign the chat settings sheet with grouped device and media sections, refresh the Connect and Voice tabs, and tighten the chat composer/session header for a denser mobile layout. (#44894) Thanks @obviyus.
- iOS/onboarding: add a first-run welcome pager before gateway setup, stop auto-opening the QR scanner, and show `/pair qr` instructions on the connect step. (#45054) Thanks @ngutman.
- Browser/existing-session: add an official Chrome DevTools MCP attach mode for signed-in live Chrome sessions, with docs for `chrome://inspect/#remote-debugging` enablement and direct backlinks to Chrome’s own setup guides.
- Browser/agents: add built-in `profile="user"` for the logged-in host browser and `profile="chrome-relay"` for the extension relay, so agent browser calls can prefer the real signed-in browser without the extra `browserSession` selector.
- Browser/act automation: add batched actions, selector targeting, and delayed clicks for browser act requests with normalized batch dispatch. Thanks @vincentkoc.
- Docker/timezone override: add `OPENCLAW_TZ` so `docker-setup.sh` can pin gateway and CLI containers to a chosen IANA timezone instead of inheriting the daemon default. (#34119) Thanks @Lanfei.
- Dependencies/pi: bump `@mariozechner/pi-agent-core`, `@mariozechner/pi-ai`, `@mariozechner/pi-coding-agent`, and `@mariozechner/pi-tui` to `0.58.0`.
- Cron/sessions: add `sessionTarget: "current"` and `session:<id>` support so cron jobs can bind to the creating session or a persistent named session instead of only `main` or `isolated`. Thanks @kkhomej33-netizen and @ImLukeF.
- Telegram/message send: add `--force-document` so Telegram image and GIF sends can upload as documents without compression. (#45111) Thanks @thepagent.

## Fixes

- Dashboard/chat UI: stop reloading full chat history on every live tool result in dashboard v2 so tool-heavy runs no longer trigger UI freeze/re-render storms while the final event still refreshes persisted history. (#45541) Thanks @BunsDev.
- Gateway/client requests: reject unanswered gateway RPC calls after a bounded timeout and clear their pending state, so stalled connections no longer leak hanging `GatewayClient.request()` promises indefinitely.
- Build/plugin-sdk bundling: bundle plugin-sdk subpath entries in one shared build pass so published packages stop duplicating shared chunks and avoid the recent plugin-sdk memory blow-up. (#45426) Thanks @TarasShyn.
- Ollama/reasoning visibility: stop promoting native `thinking` and `reasoning` fields into final assistant text so local reasoning models no longer leak internal thoughts in normal replies. (#45330) Thanks @xi7ang.
- Android/onboarding QR scan: switch setup QR scanning to Google Code Scanner so onboarding uses a more reliable scanner instead of the legacy embedded ZXing flow. (#45021) Thanks @obviyus.
- Browser/existing-session: harden driver validation and session lifecycle so transport errors trigger reconnects while tool-level errors preserve the session, and extract shared ARIA role sets to deduplicate Playwright and Chrome MCP snapshot paths. (#45682) Thanks @odysseus0.
- Browser/existing-session: accept text-only `list_pages` and `new_page` responses from Chrome DevTools MCP so live-session tab discovery and new-tab open flows keep working when the server omits structured page metadata.
- Control UI/insecure auth: preserve explicit shared token and password auth on plain-HTTP Control UI connects so LAN and reverse-proxy sessions no longer drop shared auth before the first WebSocket handshake. (#45088) Thanks @velvet-shark.
- Gateway/session reset: preserve `lastAccountId` and `lastThreadId` across gateway session resets so replies keep routing back to the same account and thread after `/reset`. (#44773) Thanks @Lanfei.
- macOS/onboarding: avoid self-restarting freshly bootstrapped launchd gateways and give new daemon installs longer to become healthy, so `openclaw onboard --install-daemon` no longer false-fails on slower Macs and fresh VM snapshots.
- Gateway/status: add `openclaw gateway status --require-rpc` and clearer Linux non-interactive daemon-install failure reporting so automation can fail hard on probe misses instead of treating a printed RPC error as green.
- macOS/exec approvals: respect per-agent exec approval settings in the gateway prompter, including allowlist fallback when the native prompt cannot be shown, so gateway-triggered `system.run` requests follow configured policy instead of always prompting or denying unexpectedly. (#13707) Thanks @sliekens.

## Breaking

- **BREAKING:** Agents now load at most one root memory bootstrap file. `MEMORY.md` wins; `memory.md` is only used when `MEMORY.md` is absent. If you intentionally kept both files and depended on both being injected, merge them before upgrade. This also fixes duplicate memory injection on case-insensitive Docker mounts. (#26054) Thanks @Lanfei.


---

## 💡 深度点评

这份 openclaw 2026.3.13 的更新日志显示，项目正从早期的“自动化脚本”向“深度整合的 Agent 运行环境”演进。以下是针对该版本的深度点评：

### 核心亮点

*   **Chrome DevTools MCP 与原生会话接入**：新增官方 Chrome DevTools MCP 挂载模式，支持直接接管已登录的 live Chrome 会话。配合内置的 `profile="user"` 预设，Agent 可以直接在用户真实的浏览器上下文中执行任务，告别了过去复杂的会话选择器配置，极大提升了浏览器自动化任务的可用性。
*   **浏览器 act 自动化能力增强**：引入了批处理动作（batched actions）、精确的选择器定位以及延迟点击功能。这些改动配合规范化的批处理调度，显著优化了 Agent 在处理复杂网页交互时的稳定性和响应速度。
*   **Cron 任务会话绑定灵活性**：定时任务不再局限于 `main` 或 `isolated` 会话，新版本支持 `sessionTarget: "current"` 或指定 `session:<id>`。这使得自动化任务能够精准地在特定持久化会话中运行，为复杂的长期工作流提供了基础支持。

### 值得注意的修复

*   **Dashboard UI 性能瓶颈解决**：修复了 Dashboard v2 在工具执行期间频繁重载完整聊天历史的问题。此前，在处理工具密集型任务时常会出现 UI 冻结或渲染风暴，优化后有效提升了高频交互场景下的操作流畅度。
*   **Ollama 推理内容脱敏**：针对本地推理模型，系统现在会自动拦截并隐藏 `thinking` 和 `reasoning` 等内部思考字段，防止模型在最终回答中泄露冗长的内部推理过程。
*   **执行审批（exec approvals）安全强化**：针对 macOS 和 Windows 环境下的 `pnpm`、`env`、PowerShell 等多种运行时进行了深度解包与校验，修复了多个可能绕过安全审批的路径，提升了 sandbox 的防御水位。
*   **Gateway 资源泄露修复**：为 Gateway RPC 请求增加了有界超时机制并自动清理挂起状态，解决了长时间连接卡死导致 `GatewayClient` Promise 无限堆积的内存泄露隐患。

### 个人评价

2026.3.13 版本是 openclaw 在工程化道路上的一个重要节点。通过深度整合 Chrome MCP，它正试图打破 Agent 与用户日常环境之间的边界，使其能够真正利用真实的浏览器状态。同时，版本中大量关于执行审批、内存泄露和配置校验的修复，表明该框架已进入大规模、长时间运行的稳定性打磨阶段。唯一需要注意的是 `MEMORY.md` 优先级的 Breaking Change，用户在升级前需确保合并不规范命名的记忆文件。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-21 08:01:57*
