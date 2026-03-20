---
title: "🔧 Openclaw 更新日报 2026-03-20"
date: 2026-03-20T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-20  
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

这是一份关于 openclaw 2026.3.13 版本的技术点评。

### 核心亮点

*   **原生浏览器深度集成 (Chrome DevTools MCP)**：新版增加了官方的 Chrome DevTools MCP 挂载模式，允许直接附加到已登录的活跃 Chrome 会话（通过 `chrome://inspect`）。结合新增的 `profile="user"` 配置，Agent 现在可以直接复用宿主浏览器的登录状态和上下文，无需再繁琐地处理 `browserSession` 选择器，大幅提升了 Web Automation 的成功率。
*   **浏览器操作批处理与增强**：引入了 `batched actions` 和选择器定向功能。通过规范化的批量调度和延迟点击（delayed clicks），减少了浏览器执行请求的往返次数。这对于需要高频操作或复杂交互的自动化任务来说，不仅提高了执行效率，也增强了在模拟人类行为时的稳定性。
*   **灵活的 Cron 任务会话绑定**：Cron 任务现在支持 `sessionTarget: "current"` 或指定的 `session:<id>`。这意味着定时任务不再局限于全局或孤立运行，而是可以精确绑定到特定的持久化会话中，为构建复杂的长期运行工作流（Long-running Workflows）提供了底层支撑。

### 值得注意的修复

*   **控制台 UI 性能优化**：修复了 Dashboard v2 在工具执行过程中频繁触发全量历史记录重载的问题。这一改进彻底解决了“工具密集型”任务运行过程中出现的 UI 冻结和渲染风暴，显著提升了长会话的操作流畅度。
*   **安全与执行审批强化**：针对 `pnpm` 运行时、PowerShell 脚本以及 macOS 下的 `env` 包装器进行了深度的执行审批解包优化。同时修复了通过反斜杠换行绕过 shell 检查的安全漏洞。这一系列变更显示出项目在多平台安全沙箱边界控制上的持续投入。
*   **底层稳定性与内存修复**：通过将 `plugin-sdk` 的子路径项合并到单个共享构建阶段，解决了近期出现的内存膨胀问题。此外，Gateway 增加了对超时未响应 RPC 调用的强制回收机制，有效防止了因挂起 Promise 导致的内存泄漏。

### 个人评价

openclaw 2026.3.13 是一个侧重于“工程化落地”的版本。它没有追求激进的新功能堆砌，而是通过完善 Chrome 原生会话接入、优化 UI 渲染效率和加固执行安全边界，解决了开发者在实际生产中使用 openclaw 时的痛点。特别是对 `MEMORY.md` 优先级的规范化（Breaking Change），标志着项目在处理跨平台一致性问题上进入了更成熟的阶段。整体来看，这是一个显著提升生产力上限并加固了运行底座的稳定版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-20 08:02:18*
