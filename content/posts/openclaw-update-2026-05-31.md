---
title: "🔧 Openclaw 更新日报 2026-05-31"
date: 2026-05-31T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.30

**发布日期**: 2026-05-31  
**⚠️ 新版本发布**

## Highlights

- Agents and CLI-backed runtimes recover more cleanly from interrupted tool calls, stale session bindings, compaction handoffs, and media delivery retries. (#88129, #88136, #88141, #88162, #88182)
- Channels and mobile delivery are steadier across Telegram, WhatsApp, iMessage, Slack, Discord, Microsoft Teams, Google Chat, Google Meet, and iOS realtime Talk. (#88096, #88105, #88183, #88231)
- Provider and plugin requests now bound more timers, retries, OAuth/device-code lifetimes, media downloads, local service probes, and generated-content polling paths before they can hang a run.
- Skills, session metadata, gateway runtime state, plugin metadata, and store writes do less repeated work on hot paths while keeping config and dispatch behavior stable.
- Workboard, SecretRef plugin manifests, hosted iOS push relay, and external Copilot/Tokenjuice packaging add broader orchestration, integration, and plugin delivery surfaces. (#82326, #87469, #87796, #88107, #88117)
- Release, CI, Docker, E2E, and diagnostics lanes now cap more logs, response bodies, readiness probes, artifact checks, and status polling so failures report bounded proof instead of stalling.

## Changes

- Skills: let the `skill_research` agent tool apply, reject, and quarantine explicit Skill Workshop proposals through the guarded proposal lifecycle. Thanks @shakkernerd.
- Skills: let Skill Workshop proposals carry approved support files under standard skill folders, with scanner, hash, and rollback safeguards. Thanks @shakkernerd.
- Skills: let pending Skill Workshop proposals be revised in place with versioned, dated proposal frontmatter before approval. Thanks @shakkernerd.
- Skills: add Skill Workshop proposals with pending `PROPOSAL.md` drafts, CLI/Gateway review actions, rollback metadata, and the `skill_research` agent tool. Thanks @shakkernerd.
- Plugins: externalize Tokenjuice as the official `@openclaw/tokenjuice` plugin with npm and ClawHub publish metadata.
- Plugins: externalize the GitHub Copilot agent runtime as the official `@openclaw/copilot` plugin with npm and ClawHub publish metadata.
- iOS: add hosted push relay defaults, realtime Talk playback, and a guarded WebSocket ping path for more reliable mobile sessions. (#88096, #88105, #88231)
- Workboard: add orchestration primitives and agent coordination tools for multi-agent planning and run tracking. (#87469)
- Code mode: add internal namespaces for scoped agent/global sessions and exact namespace tool dispatch. (#88043)
- Control UI: add a Dreaming-tab agent selector and propagate the selected agent through Dreaming status, diary, and diary actions. (#78748) Thanks @stevenepalmer.
- Plugins: add a SecretRef provider integration manifest contract and extract shared LLM core packages for provider/plugin reuse. (#82326, #88117)
- Skills: add the core skills index and centralize skills runtime loading, status, filtering, and prompt formatting.

## Fixes

- CLI: keep `plugins list --json` on the snapshot-only path so plugin sweeps avoid loading the full runtime status graph.
- Plugins: make PixVerse external-plugin ClawHub metadata explicit and keep it out of bundled dist builds.
- Cron: keep SQLite cron migrations compatible with legacy run-log tables, archived job stores, diagnostic cron names, and legacy one-shot delete-after-run behavior. (#88285)
- Providers: bound generated media downloads from OpenAI, Runway, xAI, MiniMax, BytePlus, DashScope-compatible, FAL, OpenRouter, Google, Vydra, and Comfy providers.
- Providers: cap GitHub Copilot OAuth request timeouts before creating abort signals.
- Cron: retry recurring jobs after transient model rate limits before waiting for the next scheduled slot.
- Agents/Codex: keep live session locks during cleanup, recover interrupted CLI tool transcripts, preserve Codex auth and compaction session identity, clear orphan tool state, cap app-server idle timers, and keep media completion delivery retryable. (#88129, #88136, #88141, #88162, #88182)
- Chat/UI: show Gateway chat failures as visible assistant messages in the Control UI instead of only setting an invisible error state.
- Channels: cap Telegram, Discord, WhatsApp, Signal, Feishu, Google Chat, Microsoft Teams, QQBot, Nostr, Zalo, Zalouser, and Nextcloud-style request/retry timers; preserve SMS approval reply routes; and retry WhatsApp QR login 408 timeouts. (#88183)
- Security/config parsing: reject unsafe OAuth/token lifetimes, retry-after delays, inbound timestamps, response body sizes, command timeout config, sandbox observer token TTLs, and gateway WebSocket calls after close.
- Providers/media: cap local service, model, usage, queue, generated media, TTS, music, workflow polling, and provider OAuth request timers across hosted and local providers.
- Release/CI/E2E: bound release candidate reads, beta smoke REST calls, changelog restore, kitchen-sink and bundled plugin readiness probes, secret-provider probes, Vitest routing, and mainline test flakes. (#88127, #88137, #88155, #88160)


---

## 💡 深度点评

### 核心亮点

这个版本的重点很明确：一是把运行时里容易卡住、挂起、重试失控的路径继续收紧，二是把多渠道消息、移动端实时能力和插件化边界继续做稳。对日常使用来说，稳定性收益会比“新增一个大功能”更直接。

### 值得注意的修复

值得留意的是大量与中断恢复、超时边界、状态同步、日志收敛相关的修复。这类改动平时不显眼，但对长任务、跨端会话和自动化流程影响很大，能明显减少“任务卡住但没有明确报错”的情况。

### 个人评价

2026.5.30 更像一次面向工程质量的版本，而不是营销型版本。它在代理运行、插件边界、移动端会话和通道稳定性上持续补基础设施。对重度用户来说，这种版本通常比表面功能更新更有价值。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-31 09:36:16*
