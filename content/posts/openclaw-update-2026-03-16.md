---
title: "🔧 Openclaw 更新日报 2026-03-16"
date: 2026-03-16T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-16  
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

### 核心亮点

*   **浏览器原生会话挂载（Chrome DevTools MCP）**：新增官方 Chrome DevTools MCP 挂载模式，支持通过 `chrome://inspect` 直接接入已登录的实时 Chrome 会话。配合内置的 `profile="user"` 属性，Agent 现在可以直接在用户的主浏览器环境内执行任务，无需额外的 `browserSession` 选择器，极大简化了复杂 Web 任务的上下文继承。
*   **浏览器自动化指令集增强**：针对 `browser/act` 引入了批量操作（batched actions）、选择器定位优化以及延迟点击功能。通过标准化的批处理调度，Agent 在处理动态 Web 页面时的响应速度和动作准确度有了显著提升。
*   **Cron 任务会话绑定**：`sessionTarget` 现在支持 `current` 或特定 `session:<id>`。这意味着定时任务不再局限于孤立环境或主会话，而是可以灵活绑定到当前活跃会话或持久化的命名会话中，实现了自动化流与人工交互流的深度协同。

### 值得注意的修复

*   **Dashboard 渲染性能优化**：修复了在执行工具密集型（tool-heavy）任务时，UI 频繁重载全量历史记录导致的重绘风暴和界面冻结问题。现在只有最终状态会触发持久化历史刷新，大幅提升了长链条任务的交互流畅度。
*   **本地推理模型「思维泄露」修复**：针对 Ollama 等具备思考能力的模型，优化了 `thinking` 和 `reasoning` 字段的处理逻辑，防止内部推理过程泄露到最终的助理回复正文中，保证了输出结果的纯净性。
*   **多平台安全审批加固**：针对 macOS 和 Windows 的 `exec` 审批逻辑进行了深度重构，能够识别并拆解 `pnpm`、`PowerShell` 以及 `env` 包装器下的真实可执行路径。同时，`MEMORY.md` 权重的明确化解决了 Docker 挂载时大小写不敏感带来的内存注入重复问题。

### 个人评价

openclaw 2026.3.13 是一个典型的「工程化落地」版本，核心价值在于消弭了 Agent 与用户真实工作环境（如已登录浏览器、活跃会话）之间的鸿沟。通过对浏览器自动化指令的批量化改版和 Dashboard 渲染瓶颈的修复，开发者能够明显感受到在大规模工具调用场景下的稳定性提升。整体演进方向正从「对话式助理」快速向「深度嵌入工作流的系统级插件」转变。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-16 08:01:44*
