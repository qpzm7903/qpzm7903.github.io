---
title: "🔧 Openclaw 更新日报 2026-03-18"
date: 2026-03-18T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-18  
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

## Breaking

- **BREAKING:** Agents now load at most one root memory bootstrap file. `MEMORY.md` wins; `memory.md` is only used when `MEMORY.md` is absent. If you intentionally kept both files and depended on both being injected, merge them before upgrade. This also fixes duplicate memory injection on case-insensitive Docker mounts. (#26054) Thanks @Lanfei.

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


---

## 💡 深度点评

这份关于 openclaw 2026.3.13 更新内容的深度点评，重点解析了该版本在自动化连接、会话控制及系统稳定性方面的核心变化。

### 核心亮点

*   **Chrome DevTools MCP 模式支持**：新增官方 Chrome 开发者工具 MCP 挂载模式，支持通过 `chrome://inspect/#remote-debugging` 直接连接已登录的实时 Chrome 会话。这使得 Agent 能够直接利用宿主浏览器的登录状态和上下文，而无需繁琐的 `browserSession` 选择器，极大提升了 Web 自动化脚本的开发效率。
*   **Cron 任务会话绑定增强**：定时任务（Cron）现在支持 `sessionTarget: "current"` 和指定 `session:<id>`。这意味着自动化任务不再局限于 `main` 或 `isolated` 环境，而是可以精确绑定到创建它的会话或特定的持久会话中，为复杂的工作流编排提供了更高的灵活性。
*   **内存引导机制规范化（破坏性变更）**：版本统一了 root memory 引导文件的加载逻辑，规定 `MEMORY.md` 优先级高于 `memory.md` 且仅加载其一。此举不仅解决了 Docker 在大小写不敏感挂载下的内存重复注入问题，也强制规范了 Agent 的长期记忆结构。

### 值得注意的修复

*   **Dashboard UI 渲染性能大幅优化**：修复了在执行重度工具调用（tool-heavy runs）时，Dashboard v2 频繁重载完整聊天历史导致的 UI 冻结和渲染风暴，显著提升了长时间会话的操作流畅度。
*   **Ollama 推理思维链隐藏**：修正了本地推理模型（如 DeepSeek-R1 等）会将内心的 `thinking` 和 `reasoning` 字段泄露到最终回复文本中的问题，确保了 assistant 输出的纯净度。
*   **网关与跨平台稳定性加固**：针对 Windows 的 `schtasks` 挂起、macOS 的网关自重启以及 Linux 非交互式安装下的 RPC 报错进行了专项修复。同时，增强了设备配对（单次有效码）和外部内容边界过滤的安全性。

### 个人评价

openclaw 2026.3.13 是一个典型的“工程化打磨”版本。它并没有堆砌浮夸的新功能，而是将重心放在了提升 Agent 对真实环境（如已登录浏览器、特定会话上下文）的接管能力上。特别是对网关（Gateway）和执行审批（Exec Approvals）逻辑的深度重构，表明该项目正从开发者玩具向生产力工具演进。对于重度依赖 Web 自动化和长周期 Cron 任务的用户来说，这是一个必须跟进的稳定版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-18 08:02:25*
