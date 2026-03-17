---
title: "🔧 Openclaw 更新日报 2026-03-17"
date: 2026-03-17T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-17  
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

OpenClaw 2026.3.13 版本发布，这一版在浏览器集成深度、任务自动化灵活性以及系统安全性上进行了多项关键迭代。以下是该版本的深度点评：

### 核心亮点

*   **原生 Chrome DevTools MCP 模式**：新增官方 Chrome DevTools MCP 挂载模式，支持直接连接已登录的活跃 Chrome 会话。配合内置的 `profile="user"` 标识，Agent 现在可以更无缝地调用宿主浏览器的真实状态，无需复杂的 `browserSession` 选择器，大幅提升了浏览器内 Agent 的执行效率和成功率。
*   **Cron 任务 Session 绑定增强**：Cron 作业新增 `sessionTarget: "current"` 和 `session:<id>` 支持。这意味着定时任务不再局限于 `main` 或隔离环境，可以直接绑定到创建它的会话或特定的持久化命名会话中，为复杂的工作流自动化提供了更精细的上下文控制。
*   **浏览器自动化指令优化**：引入了批量操作（batched actions）、选择器定位（selector targeting）和延迟点击功能。通过标准化的批量调度（normalized batch dispatch），Agent 在处理复杂的 Web 交互时，指令执行的连贯性和响应速度得到了显著提升。

### 值得注意的修复

*   **Dashboard UI 性能优化**：修复了在 Dashboard v2 中，每当工具产生实时结果时都会重新加载完整聊天历史的问题。这一改动彻底解决了在进行高强度工具调用（tool-heavy runs）时 UI 频繁冻结或渲染风暴的性能瓶颈。
*   **Ollama 思考过程隔离**：停止将本地模型的 `thinking` 和 `reasoning` 原生字段提取到最终回复文本中。这一修复确保了本地推理模型在正常回复时不会“泄露”内部思考过程，保持了输出内容的整洁性。
*   **执行审批（Exec Approvals）安全加固**：针对 macOS 和 Windows 环境下的执行审批逻辑进行了深度重构。现在能更准确地解析 `pnpm`、`env` 包装器以及 PowerShell 的多种调用形式，并修复了利用 shell 换行符绕过命令检查的潜在风险，进一步收紧了 Agent 的系统权限边界。
*   **Gateway RPC 状态泄露修复**：引入了超时的绑定机制，会自动拒绝未响应的网关 RPC 调用。这解决了长期困扰开发者的 `GatewayClient.request()` Promise 挂起导致的内存与连接泄漏问题。

### 个人评价

OpenClaw 2026.3.13 是一个典型的“工程化成熟度”版本。它并没有堆砌华丽的新功能，而是将重心放在了**生产环境的稳定性**（如 RPC 超时控制和 UI 渲染优化）以及**Agent 的原生感知力**（如 Chrome 深度集成）上。特别是对 `MEMORY.md` 加载逻辑的规范化（Breaking Change）以及对执行审批边界的打磨，显示出该工具正在从“好玩的黑客工具”向“严谨的开发者基础设施”转型。对于重度依赖浏览器自动化和定时任务的用户，这是一个必须升级的稳定版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-17 08:01:52*
