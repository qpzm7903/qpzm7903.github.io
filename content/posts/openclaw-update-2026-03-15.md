---
title: "🔧 Openclaw 更新日报 2026-03-15"
date: 2026-03-15T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-15  
**⚠️ 新版本发布**

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

这份关于 openclaw 2026.3.13 的更新说明显示，该版本在浏览器深度集成、自动化任务调度以及系统安全审计方面迈出了实质性的一步。以下是本次更新的深度点评：

### 核心亮点

*   **浏览器原生会话深度集成 (Chrome DevTools MCP)**
    新版本引入了官方的 Chrome DevTools MCP 挂载模式，允许 Agent 直接接入已登录的 live Chrome 会话。配合新增的 `profile="user"` 内置配置，Agent 能够无缝调用宿主浏览器的登录状态，无需再繁琐地处理 `browserSession` 选择器。这意味着 Agent 现在可以像真人插件一样，在用户的真实工作流中进行操作。
*   **Cron 任务的会话绑定能力**
    定时任务（Cron）不再局限于 `main` 或 `isolated` 会话，新增了 `sessionTarget: "current"` 和特定 `session:<id>` 支持。这一改进使得自动化脚本可以精准地在持久化命名会话中运行，极大地增强了有状态自动化流程的灵活性。
*   **浏览器操作自动化升级**
    引入了批处理动作（Batched actions）和选择器定位优化。通过归一化的批量调度机制，Agent 在执行点击、延迟触发等一系列连续指令时，响应速度和成功率将得到显著提升，减少了因网络抖动或 DOM 异步加载导致的指令失效。

### 值得注意的修复

*   **Dashboard v2 渲染性能优化**
    修复了在执行重型工具任务时，UI 会因频繁重载完整历史记录而导致的闪屏或假死（re-render storms）问题。现在仅在最终事件触发时刷新持久化历史，大幅提升了复杂任务执行时的实时观测体验。
*   **本地模型推理泄露修复 (Ollama)**
    针对 Ollama 等本地模型，修复了 `thinking` 和 `reasoning` 字段意外混入最终回复的问题。这确保了用户在与具备思考能力的模型交互时，不会被冗长的内部推理过程干扰干扰输出。
*   **执行审批流的安全增强**
    针对 macOS 和 Windows 环境进行了深度加固，包括识别 `pnpm`、`PowerShell` 的多种包装形式，以及对 shell 转义字符注入的严格过滤。同时，设备配对码（Pairing codes）改为一次性使用，防止了潜在的权限提升风险。

### 个人评价

openclaw 2026.3.13 是一个典型的从「功能丰富」向「生产可用」过渡的版本。它通过 MCP 协议将浏览器从一个受控沙盒变成了 Agent 的原生延伸，极大降低了复杂 Web 环境下的开发门槛。同时，大量的安全补丁和对 `MEMORY.md` 加载逻辑的标准化（Breaking Change），标志着该项目正在构建更严谨的内存模型和执行策略。整体来看，这个版本在提升开发者交互效率的同时，显著加固了作为系统级工具的安全底座。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-15 10:25:07*
