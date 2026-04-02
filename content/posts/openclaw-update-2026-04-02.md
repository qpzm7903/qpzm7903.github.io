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

### 📝 个人评价

2026.4.2 包含多项变更，请查看上方详细列表。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-02 08:20:26*
