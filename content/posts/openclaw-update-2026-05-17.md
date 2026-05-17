---
title: "🔧 Openclaw 更新日报 2026-05-17"
date: 2026-05-17T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.17

**发布日期**: 2026-05-17  
**⚠️ 新版本发布**

## Changes

- Security/audit: add `security.audit.suppressions` for intentionally accepted audit findings, keeping suppressed matches out of the active summary while preserving them in JSON output with an active suppression notice. (#76949) Thanks @100menotu001.
- Agents/subagents: label delegated task and subagent completion handoffs as ready for parent review, and tell requester agents to review/verify results before calling them done. (#78985) Thanks @100menotu001.
- Providers/media: add fal and OpenRouter music-generation providers for the shared `music_generate` tool, including fal MiniMax/ACE/Stable Audio endpoints and OpenRouter Lyria audio output.
- Maintainer tooling: warn before running JS package commands on raw Crabbox AWS boxes, pointing maintainers to Actions hydration or Blacksmith Testbox for CI-like proof.
- Control UI: show provider quota usage in the Overview card and Chat header, and recover stale Chat in-progress state after missed terminal events. (#82647)
- Mac app remote setup can now be preconfigured from `openclaw-mac configure-remote`, skips onboarding when config is already complete, supports direct LAN/Tailnet gateway URLs, allows private same-origin Control UI loads, and owns the SSH tunnel process when SSH is selected.
- Providers/xAI: add xAI Grok OAuth login for SuperGrok subscribers, letting `xai/*` models and xAI media/tool providers authenticate without `XAI_API_KEY`.
- CLI/cron: add `openclaw cron run --wait` with timeout and poll interval controls, plus exact `cron.runs --run-id` filtering so automation can block on one queued manual run. (#81929) Thanks @ificator.
- Maintainer tooling: route Crabbox skill defaults through the repo brokered AWS config, leaving Blacksmith Testbox as an explicit opt-in instead of the broad-proof default.
- CLI/onboarding: localize the setup wizard and bundled channel setup flows for English, Simplified Chinese, and Traditional Chinese. (#80645) Thanks @GaosCode.
- Agents/skills: cache hydrated `resolvedSkills` across warm gateway turns while keying reuse by the redacted effective config, reducing redundant skill snapshot rebuilds without crossing config-gated skill boundaries. (#81451) Thanks @solodmd.
- Group chat: add core inbound event classification with opt-in `messages.groupChat.unmentionedInbound: "room_event"`, so always-on unmentioned room chatter can run as quiet context and speak visibly only via the message tool. (#81317) Thanks @obviyus.

## Fixes

- Providers/GitHub Copilot: hash Responses replay item ids with sha256 instead of a weak 32-bit hash and build same-provider Copilot tool-call ids distinctly, so concurrent tool-call replays no longer collide and reject follow-up turns.
- Providers/Anthropic-messages: extract `reasoning_content` from `thinking` blocks during assistant replay so proxy providers that route through the Anthropic-messages transport preserve reasoning context across tool-call follow-up turns. Thanks @Sunnyone2three.
- Agents/GitHub Copilot: normalize replayed Responses tool-call IDs before dispatch so resumed sessions with historical overlong tool IDs continue instead of failing Copilot schema validation. (#82750) Thanks @galiniliev.
- Mac app: let menu gateway/session error text wrap across a few lines and stop rebuilding dynamic Context/Gateway menu rows while the menu is open, reducing flicker.
- Mac app: make device pairing approval sheets friendlier, with concise Mac/device copy, shortened identifiers, friendly scope labels, and Approve as the primary action.
- Providers/Qwen: honor session thinking level for `qwen-chat-template` payloads so `/think off` disables nested llama.cpp chat-template thinking controls. Fixes #82768. Thanks @bfox55.
- Feishu/wiki: reject numeric wiki space IDs before creating Lark clients and keep numeric-looking IDs documented as quoted opaque strings, preventing JavaScript precision loss in knowledge base calls. Fixes #45301. (#82769) Thanks @hyspacex.
- Control UI: simplify Talk settings to Voice, Model, and Sensitivity defaults, with provider, transport, exact VAD, and timing controls behind Advanced.
- Telegram: let catch-all mention patterns match captionless group photos, so media-only group messages reach the agent when the group is intentionally configured to respond to all messages. Fixes #44833. (#82756) Thanks @IWhatsskill.
- Gateway/pairing: reject forged loopback Control UI origins from non-local proxy paths, and keep mobile pairing setup on Tailscale bind mode pointing users to Tailscale Serve/Funnel instead of cleartext tailnet WebSockets.
- Telegram/Gateway: persist isolated polling offsets only after main-thread dispatch and preserve gateway caller scopes for Telegram message actions, fixing consumed-but-unrouted polling updates and recursive CLI send scope approvals. Fixes #82277. (#82705) Thanks @udaymanish6.
- Memory-core: abort timed-out embedding provider calls so remote embedding HTTP requests do not continue running after memory query or indexing timeouts. Fixes #82732. Thanks @adityarya24.


---

## 💡 深度点评

### 核心亮点

*   **群聊上下文管理机制优化**：引入了 `messages.groupChat.unmentionedInbound: "room_event"` 选项。该机制允许代理将未被提及的群聊消息作为“安静上下文（quiet context）”在后台运行，且仅在调用消息工具（message tool）时才产生可见回复。这大幅提升了机器人在高频群聊中维持上下文感知时的信噪比。
*   **安全审计的精确抑制**：新增 `security.audit.suppressions` 功能。运维人员现在可以有意忽略已知的审计结果，使其不在活跃的摘要报告中告警，但同时会在输出的 JSON 报告中保留带有标记的抑制记录，在保持合规性的同时减少了 CI 阶段的噪音。
*   **网关可观测性与启动性能拆分**：网关层引入了可选的追踪日志（覆盖重启信号、任务排空、下一次启动及内存跨度等阶段）。更重要的是，将启动基准测试中的 HTTP 端口绑定计时与网关完全就绪计时进行了物理拆分，为复杂生产环境提供了更准确的性能诊断指标。

### 值得注意的修复

*   **带推理过程模型的多轮工具调用断层**：修复了 Anthropic 及兼容模型（包含 Xiaomi MiMo 和 Kimi 的思考模型）在多轮工具调用时的状态毒化问题。现在会在助手重放流中精确提取并保留 `thinking` 块内的 `reasoning_content`，防止二轮请求因缺失推理签名而报错。
*   **并发工具调用的哈希碰撞阻断**：将 GitHub Copilot 响应重放 ID 的生成算法从脆弱的 32 位哈希替换为 SHA-256，从底层解决了并发工具调用重放时因 ID 冲突导致后续交互被拒绝的严重 Bug。
*   **内存搜索相关的文件句柄（FD）泄漏**：移除了 QMD 和内存监视器中基于 `chokidar` 的写入稳定性轮询机制。现在的变更文件通过已有的防抖同步队列进行处理，彻底修复了包含大量 Markdown 文件的仓库导致的文件描述符耗尽问题（Fixes #77327, #78224）。

### 个人评价

本次 2026.5.17 的版本更新是一次典型且高质量的工程稳定性迭代，核心聚焦于边缘场景的健壮性与复杂通信链路的上下文一致性。开发团队着重解决了带有独立推理阶段（Thinking Models）的新一代模型在 Agent 工具链中的生命周期断裂问题，确保了复杂任务状态机的平滑流转。整体来看，系统正朝着具备更高可观测性、更精细资源隔离以及更强原生企业级兼容性的方向稳步迈进。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-17 09:57:38*
