---
title: "🔧 Openclaw 更新日报 2026-04-21"
date: 2026-04-21T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.20

**发布日期**: 2026-04-21  
**⚠️ 新版本发布**

## Changes

- Plugins/tasks: add a detached runtime registration contract so plugin executors can own detached task lifecycle and cancellation without reaching into core task internals. (#68915) Thanks @mbelinky.
- Terminal/logging: optimize `sanitizeForLog()` by replacing the iterative control-character stripping loop with a single regex pass while preserving the existing ANSI-first sanitization behavior. (#67205) Thanks @bulutmuf.
- QA/CI: make `openclaw qa suite` and `openclaw qa telegram` fail by default when scenarios fail, add `--allow-failures` for artifact-only runs, and tighten live-lane defaults for CI automation. (#69122) Thanks @joshavant.
- Mattermost: stream thinking, tool activity, and partial reply text into a single draft preview post that finalizes in place when safe. (#47838) thanks @ninjaa.

## Fixes

- Cron/Telegram: key isolated direct-delivery dedupe to each cron execution instead of the reused session id, so recurring Telegram announce runs no longer report delivered while silently skipping later sends. (#69000) Thanks @obviyus.
- Models/Kimi: default bundled Kimi thinking to off and normalize Anthropic-compatible `thinking` payloads so stale session `/think` state no longer silently re-enables reasoning on Kimi runs. (#68907) Thanks @frankekn.
- Control UI/cron: keep the runtime-only `last` delivery sentinel from being materialized into persisted cron delivery and failure-alert channel configs when jobs are created or edited. (#68829) Thanks @tianhaocui.
- OpenAI/Responses: strip orphaned reasoning blocks before outbound Responses API calls so compacted or restored histories no longer fail on standalone reasoning items. (#55787) Thanks @suboss87.
- Cron/CLI: parse PowerShell-style `--tools` allow-lists the same way as comma-separated input, so `cron add` and `cron edit` no longer persist `exec read write` as one combined tool entry on Windows. (#68858) Thanks @chen-zhang-cs-code.
- Browser/user-profile: let existing-session `profile="user"` tool calls auto-route to a connected browser node or use explicit `target="node"`, while still honoring explicit `target="host"` pinning. (#48677)
- Discord/slash commands: tolerate partial Discord channel metadata in slash-command and model-picker flows so partial channel objects no longer crash when channel names, topics, or thread parent metadata are unavailable. (#68953) Thanks @dutifulbob.
- BlueBubbles: consolidate outbound HTTP through a typed `BlueBubblesClient` that resolves the SSRF policy once at construction so image attachments stop getting blocked on localhost and reactions stop getting blocked on private-IP BB deployments. Fixes #34749 and #59722. (#68234) Thanks @omarshahine.
- Cron/gateway: reject ambiguous announce delivery config at add/update time so invalid multi-channel or target-id provider settings fail early instead of persisting broken cron jobs. (#69015) Thanks @obviyus.
- Cron/main-session delivery: preserve `heartbeat.target="last"` through deferred wake queuing, gateway wake forwarding, and same-target wake coalescing so queued cron replies still return to the last active chat. (#69021) Thanks @obviyus.
- Cron/gateway: ignore disabled channels when announce delivery ambiguity is checked, and validate main-session delivery patches against the live cron service default agent so hot-reloaded agent config does not falsely reject valid updates. (#69040) Thanks @obviyus.
- Matrix/allowlists: hot-reload `dm.allowFrom` and `groupAllowFrom` entries on inbound messages while keeping config removals authoritative, so Matrix allowlist changes no longer require a channel restart to add or revoke a sender. (#68546) Thanks @johnlanni.


---

## 💡 深度点评

### 核心亮点

*   **插件任务运行时注册协议解耦 (#68915)**：引入了分离的运行时注册机制，使插件执行器能够独立管理任务的生命周期与取消逻辑，无需侵入核心任务（Core Task）内部实现。这一架构优化显著增强了插件系统的隔离性与稳定性。
*   **Mattermost 流式交互优化 (#47838)**：支持将思考过程、工具活动及部分回复内容实时推送到单一草稿预览帖中，并在安全时原位转正。这种流式反馈极大提升了用户在复杂任务协作中的感知度。
*   **QA/CI 自动化质量闸门强化 (#69122)**：调整了 `openclaw qa` 相关命令的默认行为，使其在场景失败时直接返回失败状态。通过收紧 CI 自动化默认设置，确保了生产环境交付的严谨性，同时提供 `--allow-failures` 参数用于特定场景。

### 值得注意的修复

*   **推理状态一致性管理 (#68907, #55787)**：针对 Kimi 模型，修复了 `/think` 状态在 Session 结束后静默残留的问题，实现了推理载荷的标准化；同时在调用 OpenAI API 前自动剥离孤立的推理块，避免因历史记录压缩导致的请求失败。
*   **自动化任务递送逻辑 (#69000, #69021)**：修复了 Cron 任务在 Telegram 场景下的递送去重 Bug，确保重复执行时不再因 Session ID 复用而静默跳过消息；同时优化了延迟唤醒队列，确保 Cron 响应能准确返回至最后活跃的聊天目标。
*   **BlueBubbles 连接性与兼容性 (#68234, #69070)**：通过建立类型化的客户端解决了 SSRF 策略导致的本地 IP 拦截问题，并针对 macOS 26 环境下的 AppleScript 发送错误进行了适配，确保在无 Private API 权限时也能可靠递送。

### 个人评价

OpenClaw 2026.4.20 版本是一个侧重于“生产环境可靠性”的迭代。它不仅在插件架构上完成了关键的解耦，还针对模型推理状态（Thinking State）在长对话场景下的边界问题进行了深度修补。特别是在 Cron 自动化与跨平台 IM（如 Matrix、BlueBubbles、Mattermost）的集成上，该版本解决了一系列隐蔽的递送失败与状态漂移 Bug。整体而言，这一版本标志着系统正从功能堆叠向精细化状态控制与高可用自动化转型。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-21 08:01:23*
