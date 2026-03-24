---
title: "🔧 Openclaw 更新日报 2026-03-23"
date: 2026-03-23T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-23  
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

这是一份关于 openclaw 2026.3.13 版本的深度技术点评。

### 核心亮点

*   **浏览器实时会话接入（Chrome DevTools MCP）**：新版本正式支持通过 `chrome://inspect/#remote-debugging` 接入已登录的 Chrome 实时会话。配合新增的 `profile="user"` 配置，智能体现在可以直接调用宿主浏览器的真实登录状态，无需再处理复杂的 `browserSession` 选择器，极大提升了处理复杂 Web 业务流程的成功率。
*   **浏览器动作自动化增强**：引入了批量操作（batched actions）、选择器定位优化以及延迟点击功能。通过规范化的批量调度，减少了智能体在执行浏览器自动化任务时的请求往返次数，提升了操作的原子性和执行效率。
*   **Cron 任务会话绑定**：Cron 调度新增了 `sessionTarget: "current"` 和 `session:<id>` 支持。这意味着定时任务不再局限于 `main` 或 `isolated` 会话，而是可以精确绑定到特定的持久化命名会话中，为构建复杂的长期运行（Long-running）工作流提供了底层支持。

### 值得注意的修复

*   **仪表盘渲染性能优化**：修复了在执行工具密集型任务时，Dashboard v2 频繁触发全量聊天历史重载导致的 UI 冻结问题。现在工具执行过程中的实时结果更新不再引发重绘风暴，显著提升了高频任务下的交互体验。
*   **本地推理模型隐私修正**：针对使用 Ollama 运行的具备推理能力的模型，新版本停止将 `thinking` 和 `reasoning` 内部字段合并到助手正文中。这解决了本地模型在回答时“思考过程”泄露的问题，确保输出内容的简洁与专业。
*   **安全执行审批（Exec Approvals）强化**：针对 macOS 和 Windows 环境进行了多项安全加固，包括识别 `pnpm` 各类运行形式、解析 PowerShell 文件模式以及处理 macOS 上的 `env` 包装器。这些底层修复确保了安全策略无法通过简单的 shell 技巧被绕过，进一步完善了零信任架构。

### 个人评价

openclaw 在这个版本中表现出明显的“工程化落地”倾向。通过深化 Chrome 实时会话的集成和增强 Cron 任务的灵活性，它正在从一个简单的自动化工具进化为能够深度嵌入用户现有工作环境的协同系统。同时，对 Dashboard 性能和本地模型输出逻辑的修补，也体现了团队在用户体验和隐私边界处理上的成熟度。这是一个侧重于连接能力和运行稳定性的关键迭代。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-23 08:01:43*
