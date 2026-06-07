---
title: "🔧 Openclaw 更新日报 2026-06-07"
date: 2026-06-07T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.6.5

**发布日期**: 2026-06-07  
**⚠️ 新版本发布**

## Highlights

- QQBot now strips model reasoning/thinking scaffolding before native delivery, preventing raw `<thinking>` content from leaking into channel replies. (#89913, #90132) Thanks @openperf.
- MCP tool results now coerce `resource_link`, `resource`, `audio`, malformed image, and future non-text/image blocks at the materialize boundary, preventing Anthropic 400s and poisoned session history after a tool returns richer MCP content. (#90710, #90728) Thanks @RanSHammer and @849261680.
- Anthropic extended-thinking sessions recover after prompt-cache expiry or Gateway restart because stream start events wait for `message_start`, letting pre-generation signature errors trigger the existing recovery retry. (#90667, #90697) Thanks @openperf.
- Parallel is now a bundled `web_search` provider with `PARALLEL_API_KEY` discovery, guarded endpoint handling, cache-safe session ids, onboarding picker support, and docs. (#85158) Thanks @NormallyGaussian.
- Google Vertex ADC users get static catalog rows and runtime model resolution again, while single-provider cooldown recovery and memory adapter status checks are more reliable. (#90506, #90609, #90717, #90816) Thanks @849261680.
- Matrix can preflight voice notes before mention gating, preserve thread reads/replies through Matrix relations pagination, and carry QA coverage for voice and thread flows. (#78016, #90415)
- Auth and plugin install state is more durable: auth profiles now live in SQLite, official npm plugin install records keep their trusted pins, and prerelease fallback integrity checks avoid carrying stale integrity forward. (#89102, #88585)
- macOS node mode no longer silently self-reconnects away from a healthy direct Gateway session, reducing unexpected companion app session churn. (#90668, #90815) Thanks @vrurg.
- Upgrade and service paths are safer: cron legacy JSON stores migrate during doctor preflight, service env placeholders no longer mask state-dir secrets, WhatsApp startup waits are bounded, and disabled WhatsApp accounts tear down on config reload. (#90072, #90208, #90277, #90488, #90486, #87951, #87965) Thanks @MonkeyLeeT, @sallyom, @mcaxtr, and @MukundaKatta.

## Changes

- Search/providers: add the Parallel bundled web-search plugin, live provider tests, registration contracts, onboarding/docs wiring, and guarded `api.parallel.ai/v1/search` support. (#85158) Thanks @NormallyGaussian.
- Matrix/channels: add voice-message preflight and thread-aware read/reply behavior, including Matrix QA scenario wiring and docs for voice-message behavior. (#78016, #90415)
- Skills/ClawHub: install ClawHub skills backed by GitHub repositories through the resolved install API, download the pinned GitHub commit, keep install-policy checks, and report install telemetry after success. (#90478) Thanks @Patrick-Erichsen.
- Google Chat/channels: add native approval card actions and click handling so Google Chat approvals use platform-native cards instead of generic message flow.
- Mobile: Android provider/model screens now surface expiring, unavailable, unresolved, and attention states more clearly, while iOS settings and Talk tabs keep diagnostics, gateway rows, attachment labels, and unavailable Talk controls reachable.
- Memory: QMD search can use the new rerank toggle, and memory adapter status uses the resolved default model identity when checking plain status. (#61834)
- Docs/tooling: add Parallel search docs, refresh weather-skill guidance toward `web_fetch`, clarify legacy `openai-codex` auth, document release/test helper scripts, and tighten changed-test routing docs for CI/debugging work. (#90028, #90250) Thanks @fuller-stack-dev.
- Release/process: switch release trains to `YYYY.M.PATCH` monthly patch numbering, keep pre-transition tags compatible, and pin the June 2026 floor at `2026.6.5` after the published beta.
- Platform maintenance: refresh Android, Swift/macOS, Docker, CodeQL, Buildx, Docker build/push, and Codex Action dependencies for this release train. (#74980, #81757, #86481, #86483, #90601)

## Fixes

- Channel content boundaries: QQBot now strips reasoning/thinking tags before sending, preserving final answers while hiding internal model narration from users. (#89913, #90132) Thanks @openperf.
- Agents/MCP/providers: coerce non-text/image MCP tool-result blocks before they reach provider converters, preserving valid images and turning richer MCP content into text instead of malformed image blocks. (#90710, #90728) Thanks @RanSHammer and @849261680.
- Anthropic/Codex/ACP/agent recovery: defer Anthropic stream start events until `message_start`, strip stale compaction thinking signatures before Anthropic replay, detect unsigned thinking-only stalls, refresh prompt fences after compaction writes, reject empty completion handoffs, preserve parent streaming-off overrides/shared progress commentary, forward heartbeat metadata to context-engine hooks, and cover Codex session/thread migration edge cases. (#90667, #90697, #90163, #90108, #89874, #89505, #90632, #89302, #90729, #90317, #90319) Thanks @openperf, @100yenadmin, and @ooiuuii.
- Provider/model resolution: preserve Google Vertex ADC auth markers in generated catalogs, re-probe a single-provider primary after cooldown, share Codex model visibility, fail closed for unknown model auth, preserve Codex alias availability, keep unresolved profile refs unknown, and avoid resolving auth while listing models. (#90506, #90609, #90717, #90702) Thanks @849261680.
- Gateway/macOS/mobile: avoid duplicate Gateway probe warnings by identity, rate-limit node pairing requests while preserving paired-node reconnects, keep macOS node mode on a healthy direct Gateway session, keep iOS diagnostics and gateway rows reachable, and avoid Linux ARM Gradle resource tasks during Android builds. (#85791, #90147, #90668, #90815) Thanks @giodl73-repo and @vrurg.
- TUI/chat/Workboard/auto-reply: optimistic user messages stay stable across stale history reloads, runId reassignment, and abort windows instead of disappearing, jumping, or lingering as ghost rows; Workboard stale lifecycle bulk updates no longer overwrite newer status/provenance; message-tool sends now count as delivery. (#86205, #89600, #88592, #90123) Thanks @RomneyDa.
- Cron/update/service env: doctor config preflight now migrates legacy cron JSON stores into SQLite before runtime reads, service env planning skips unresolved placeholders that would mask state-dir `.env` values, and session transcript rewrites keep registry markers/discriminants consistent. (#90072, #90208, #90277, #90488) Thanks @MonkeyLeeT and @sallyom.
- Security/config/tooling: guard MCP HTTP redirects, protect global agent config defaults, and keep release/test/tooling proof failures bounded and explicit. (#89732, #90145)
- Channels: WhatsApp restarts when per-account config changes, bounds background startup waits, closes failed sockets, and preserves reconnect behavior; Mattermost slash commands keep their state on `globalThis`; Feishu streaming cards preserve full merged content; voice-call tracks Twilio streams after connect; ClickClack reply tools respect `toolsAllow`. (#87951, #87965, #90486, #68113, #90534, #90181, #90607, #89500) Thanks @MukundaKatta, @mcaxtr, @infoanton, @mushuiyu886, and @sahibzada-allahyar.
- Release/CI/E2E: main CI guard drift, PR merge diff scoping, live Docker credential staging, base-image qualification, installer Docker classification, Playwright dependency install recovery, API-key auth for Codex live Docker lanes, Parallels option terminators, and JSON-mode progress handling are tighter so release proof fails cleaner. (#90532, #90287, #90058) Thanks @RomneyDa, @hxy91819, and @mrunalp.
- Tests/state isolation: provider, media, auth, cron, task, session, sandbox, Gateway, and Codex timeout fixtures now scope more home/state/env data per test, reducing cross-test leakage and making release validation failures less noisy. (#90027, #89974)


---

## 💡 深度点评

### 核心亮点

这版最值得关注的有四块：

1. **QQBot 终于修复了思维链泄漏问题** — 之前`<thinking>`标签经常原样发到聊天里，现在会在投递前剥离，对日常体验影响很大。
2. **MCP 工具结果兼容性大幅提升** — `resource_link`、`resource`、`audio`等非标准字段现在会正确转码，不会再导致Anthropic 400错误或对话污染。
3. **Anthropic extended-thinking 会话恢复机制** — prompt cache过期或Gateway重启后能自动恢复，不会再因签名错误死锁。
4. **Parallel 搜索插件加入核心** — 现在是内置`web_search` provider之一，配置更简单了。

### 值得关注的修复
- auth profile 迁移到 SQLite，更持久可靠
- macOS node mode 不再无故重连到非首选 Gateway，减少配对设备掉线
- cron 遗留 JSON 迁移、WhatsApp 启动超时等升级路径更安全
- 插件安装记录保留 trusted pin，prerelease 回滚检查不再带过期完整性

### 个人评价
2026.6.5 是一个典型的"积累型"版本——没有大功能发布，但修复了多个日常高频痛点（QQBot 泄漏、MCP 兼容性、会话恢复、配对稳定性），对实际使用体验的提升很明显。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-06-07 09:16:41*
