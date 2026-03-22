---
title: "🔧 Openclaw 更新日报 2026-03-22"
date: 2026-03-22T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-22  
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

### 核心亮点

### 浏览器会话深度集成 (Chrome DevTools MCP)
此版本引入了官方 Chrome DevTools MCP 附加模式，支持直接接入已登录的实时 Chrome 浏览器会话。配合新增的 `profile="user"` 内置配置，Agent 可以直接复用宿主浏览器的登录状态和环境，无需额外的 `browserSession` 选择器。此外，浏览器自动化（Act Automation）新增了批量操作与延迟点击支持，显著提升了复杂网页任务的执行效率。

### 灵活的 Cron 任务调度
Cron 系统现支持 `sessionTarget: "current"` 及特定 `session:<id>`。这意味着定时任务不再局限于 `main` 或隔离环境，而是可以绑定到创建该任务的具体会话或指定的持久化命名会话中，极大地增强了 Agent 在多会话并行场景下的上下文维持能力。

### 移动端 UI 体验重构
Android 端对聊天设置页进行了重新设计，通过分组管理设备与媒体选项，并收紧了对话输入框布局，实现了更紧凑的移动端视图。同时，iOS 端优化了首次运行的引导流程，将 QR 扫码改为手动触发并增加了明确的 `/pair qr` 指令引导。

### 值得注意的修复

- **Dashboard 性能优化**：修复了 Dashboard v2 在工具执行过程中频繁重载完整历史记录导致的 UI 冻结现象，现在仅在最终事件触发时刷新持久化历史。
- **本地模型隐私保护**：针对 Ollama 等本地推理模型，修复了 `thinking` 和 `reasoning` 内部思维字段泄露至最终回复的问题。
- **执行安全增强**：强化了 macOS/Windows 平台下的 `system.run` 执行审批逻辑，支持识别 `pnpm`、PowerShell 等多种封装形式，确保安全策略不被绕过。
- **资源泄漏修复**：网关层现已支持对未响应的 RPC 调用进行超时拒绝，解决了由于连接卡死导致的 `GatewayClient.request()` Promise 无限挂起问题。

### 个人评价

openclaw 2026.3.13 是一个典型的从“功能扩张”转向“工程稳固”的版本。通过 Chrome DevTools MCP 的深度集成，它进一步模糊了 AI 助手与真实工作环境的边界。针对 UI 渲染风暴、内存占用以及执行安全边界的一系列底层修复，证明了该工具正在向高可用生产力工具演进。特别是对内存引导文件（MEMORY.md）权重的明确规范，虽然是破坏性变更，但对于多平台部署的一致性至关重要。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-22 08:01:48*
