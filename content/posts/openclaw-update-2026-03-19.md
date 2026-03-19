---
title: "🔧 Openclaw 更新日报 2026-03-19"
date: 2026-03-19T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.13

**发布日期**: 2026-03-19  
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

这是一份关于 openclaw 2026.3.13 更新版本的深度技术点评。

### 核心亮点

*   **浏览器原生会话集成 (Chrome DevTools MCP)**：
    新版本引入了官方的 Chrome DevTools MCP 附加模式，允许 Agent 直接挂载到已登录的实时 Chrome 会话中。配合新增的 `profile="user"` 内置配置，Agent 可以直接调用用户当前的浏览器环境，无需繁琐的会话选择器。这大幅降低了 Agent 执行网页自动化任务时的身份校验门槛。
*   **浏览器自动化动作批处理**：
    新增了批量操作 (Batched actions)、选择器定位及延迟点击功能。通过标准化的批次调度，减少了浏览器请求的往返次数，提升了 Agent 在复杂网页交互中的执行效率和稳定性。
*   **Cron 任务的会话绑定增强**：
    Cron 任务现在支持 `sessionTarget: "current"` 或指定的 `session:<id>`。这意味着定时任务不再局限于全局或孤立环境，而是可以绑定到特定的持续性会话中，为构建具有上下文感知能力的自动化流提供了可能。

### 值得注意的修复

*   **Dashboard UI 渲染性能优化**：
    修复了 v2 版控制台在处理大量工具调用结果时，因频繁重载完整聊天历史而导致的 UI 冻结问题。现在只有最终事件会触发历史持久化刷新，显著提升了高频工具调用场景下的交互流畅度。
*   **本地模型推理路径泄露修复**：
    针对使用 Ollama 等本地模型时，底层 `thinking` 和 `reasoning` 字段内容会混入最终输出的问题进行了修正。这确保了推理过程的内部思考不会干扰正常的业务回复，提升了输出内容的纯净度。
*   **安全与执行审批加固**：
    版本对 `system.run` 的审批逻辑进行了多项改进，包括单次使用的引导代码防止重放攻击，以及对 `pnpm`、PowerShell 和 macOS `env` 包装器的深度解析。现在审批系统能更准确地识别有效执行路径，避免恶意脚本通过 Shell 特性绕过限制。

### 个人评价

openclaw 2026.3.13 是一个典型的“工程化落地”版本。它没有堆砌虚华的概念，而是将重心放在了提升浏览器 Agent 的实操能力（通过 MCP 直连和动作批处理）以及解决生产环境下的稳定性痛点（如 Dashboard 性能和 RPC 泄漏）。特别是对执行审批逻辑的细粒度打磨，体现了开发团队对安全合规的重视。

**注意：** 此版本包含一项破坏性变更，Agent 现在仅加载一个根内存引导文件（`MEMORY.md` 优先级高于 `memory.md`），升级前需检查并合并相关上下文文件。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-03-19 08:01:56*
