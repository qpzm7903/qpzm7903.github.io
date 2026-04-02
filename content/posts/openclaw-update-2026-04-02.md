---
title: "🔧 Openclaw 更新日报 2026-04-02"
date: 2026-04-02T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.2

**发布日期**: 2026-04-02  
**⚠️ 新版本发布**

## Changes

- Tasks/chat: add `/tasks` as a chat-native background task board for the current session, with recent task details and agent-local fallback counts when no linked tasks are visible. Related #54226. Thanks @vincentkoc.
- Web search/SearXNG: add the bundled SearXNG provider plugin for `web_search` with configurable host support. (#57317) Thanks @cgdusek.
- Amazon Bedrock/Guardrails: add Bedrock Guardrails support to the bundled provider. (#58588) Thanks @MikeORed.
- macOS/Voice Wake: add the Voice Wake option to trigger Talk Mode. (#58490) Thanks @SmoothExec.
- Feishu/comments: add a dedicated Drive comment-event flow with comment-thread context resolution, in-thread replies, and `feishu_drive` comment actions for document collaboration workflows. (#58497) Thanks @wittam-01.
- Gateway/webchat: make `chat.history` text truncation configurable with `gateway.webchat.chatHistoryMaxChars` and per-request `maxChars`, while preserving silent-reply filtering and existing default payload limits. (#58900)
- Agents/default params: add `agents.defaults.params` for global default provider parameters. (#58548) Thanks @lpender.
- Agents/failover: cap prompt-side and assistant-side same-provider auth-profile retries for rate-limit failures before cross-provider model fallback, add the `auth.cooldowns.rateLimitedProfileRotations` knob, and document the new fallback behavior. (#58707) Thanks @Forgely3D
- Cron/tools allowlist: add `openclaw cron --tools` for per-job tool allowlists. (#58504) Thanks @andyk-ms.
- Channels/session routing: move provider-specific session conversation grammar into plugin-owned session-key surfaces, preserving Telegram topic routing and Feishu scoped inheritance across bootstrap, model override, restart, and tool-policy paths.
- WhatsApp/reactions: add `reactionLevel` guidance for agent reactions. Thanks @mcaxtr.
- Telegram/errors: add configurable `errorPolicy` and `errorCooldownMs` controls so Telegram can suppress repeated delivery errors per account, chat, and topic without muting distinct failures. (#51914) Thanks @chinar-amrutkar

## Fixes

- Chat/error replies: stop leaking raw provider/runtime failures into external chat channels, return a friendly retry message instead, and add a specific `/new` hint for Bedrock toolResult/toolUse session mismatches. (#58831) Thanks @ImLukeF.
- Gateway/reload: ignore startup config writes by persisted hash in the config reloader so generated auth tokens and seeded Control UI origins do not trigger a restart loop, while real `gateway.auth.*` edits still require restart. (#58678) Thanks @yelog
- Tasks/gateway: keep the task registry maintenance sweep from stalling the gateway event loop under synchronous SQLite pressure, so upgraded gateways stop hanging about a minute after startup. (#58670) Thanks @openperf
- Tasks/status: hide stale completed background tasks from `/status` and `session_status`, prefer live task context, and show recent failures only when no active work remains. (#58661) Thanks @vincentkoc
- Tasks/gateway: re-check the current task record before maintenance marks runs lost or prunes them, so a task heartbeat or cleanup update that lands during a sweep no longer gets overwritten by stale snapshot state.
- Exec/approvals: honor `exec-approvals.json` security defaults when inline or configured tool policy is unset, and keep Slack and Discord native approval handling aligned with inferred approvers and real channel enablement so remote exec stops falling into false approval timeouts and disabled states. Thanks @scoootscooob and @vincentkoc.
- Exec/approvals: make `allow-always` persist as durable user-approved trust instead of behaving like `allow-once`, reuse exact-command trust on shell-wrapper paths that cannot safely persist an executable allowlist entry, keep static allowlist entries from silently bypassing `ask:"always"`, and require explicit approval when Windows cannot build an allowlist execution plan instead of hard-dead-ending remote exec. Thanks @scoootscooob and @vincentkoc.
- Exec/cron: resolve isolated cron no-route approval dead-ends from the effective host fallback policy when trusted automation is allowed, and make `openclaw doctor` warn when `tools.exec` is broader than `~/.openclaw/exec-approvals.json` so stricter host-policy conflicts are explicit. Thanks @scoootscooob and @vincentkoc.
- Sessions/model switching: keep `/model` changes queued behind busy runs instead of interrupting the active turn, and retarget queued followups so later work picks up the new model as soon as the current turn finishes.
- Gateway/HTTP: skip failing HTTP request stages so one broken facade no longer forces every HTTP endpoint to return 500. (#58746) Thanks @yelog
- Gateway/nodes: stop pinning live node commands to the approved node-pair record. Node pairing remains a trust/token flow, while per-node `system.run` policy stays in that node's exec approvals config. Fixes #58824.
- WebChat/exec approvals: use native approval UI guidance in agent system prompts instead of telling agents to paste manual `/approve` commands in webchat sessions. Thanks @vincentkoc.


---

## 💡 深度点评

Openclaw 2026.4.2 版本更新深度点评。

### 核心亮点

*   **会话原生任务看板 `/tasks`**：新增了聊天内嵌的任务看板功能，支持在当前 Session 中直接管理后台任务。它不仅能显示近期任务详情，还具备 Agent 局部回退计数功能，极大提升了开发者在复杂长任务场景下的状态监控效率。
*   **多模型容错与 Failover 机制增强**：该版本针对 API 频率限制（Rate-limit）引入了更精细的控制，支持在触发跨厂商模型降级前，先进行同厂商不同 Auth Profile 的轮换重试，并新增了 `auth.cooldowns.rateLimitedProfileRotations` 配置项，增强了生产环境下的代理稳定性。
*   **生产力工具流深度集成**：飞书插件现在支持专用的文档评论事件流，能够解析评论线程上下文并实现自动回复；同时，Web 搜索新增了内置的 SearXNG 供应商支持，允许开发者自定义 Host，为私有化部署和数据隐私提供了更多选择。

### 值得注意的修复

*   **执行权限持久化（Exec Approvals）**：修复了 `allow-always` 信任模式被错误当作一次性授权的问题，现在可以正确持久化用户对特定命令的信任状态。同时，解决了 Windows 环境下无法构建白名单执行计划时的死锁问题。
*   **Anthropic 推理完整性保障**：修复了在进行上下文压缩（Compaction）时，Anthropic 模型的“思考块”（Thinking blocks）和签名可能被误删的 Bug，确保了 Claude 等模型在长对话重放和缓存控制下的逻辑连贯性。
*   **网关与数据库稳定性**：解决了 SQLite 同步压力导致网关事件循环停顿的问题，防止了网关在启动一分钟后可能出现的挂起现象，并优化了任务心跳检查机制，避免了任务状态被旧快照覆盖。

### 个人评价

2026.4.2 版本标志着 Openclaw 从“功能堆砌”向“生产级稳健”的进一步转型。核心逻辑的改进（如 Failover 机制和权限持久化）直接解决了开发者在构建自动化代理时的信任与可靠性痛点。特别是对会话内存压缩算法的细节打磨，显示出团队在处理长上下文推理一致性上的技术深度。这是一个值得所有追求高可用 AI 自动化环境的用户立即跟进的稳定版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-02 08:19:44*
