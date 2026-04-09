---
title: "🔧 Openclaw 更新日报 2026-04-09"
date: 2026-04-09T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.9

**发布日期**: 2026-04-09  
**⚠️ 新版本发布**

## Changes

- Memory/dreaming: add a grounded REM backfill lane with historical `rem-harness --path`, diary commit/reset flows, cleaner durable-fact extraction, and live short-term promotion integration so old daily notes can replay into Dreams and durable memory without a second memory stack. Thanks @mbelinky.
- Control UI/dreaming: add a structured diary view with timeline navigation, backfill/reset controls, traceable dreaming summaries, and a grounded Scene lane with promotion hints plus a safe clear-grounded action for staged backfill signals. (#63395) Thanks @mbelinky.
- QA/lab: add character-vibes evaluation reports with model selection and parallel runs so live QA can compare candidate behavior faster.
- Plugins/provider-auth: let provider manifests declare `providerAuthAliases` so provider variants can share env vars, auth profiles, config-backed auth, and API-key onboarding choices without core-specific wiring.
- iOS: pin release versioning to an explicit CalVer in `apps/ios/version.json`, keep TestFlight iteration on the same short version until maintainers intentionally promote the next gateway version, and add the documented `pnpm ios:version:pin -- --from-gateway` workflow for release trains. (#63001) Thanks @ngutman.

## Fixes

- Browser/security: re-run blocked-destination safety checks after interaction-driven main-frame navigations from click, evaluate, hook-triggered click, and batched action flows, so browser interactions cannot bypass the SSRF quarantine when they land on forbidden URLs. (#63226) Thanks @eleqtrizit.
- Security/dotenv: block runtime-control env vars plus browser-control override and skip-server env vars from untrusted workspace `.env` files, and reject unsafe URL-style browser control override specifiers before lazy loading. (#62660, #62663) Thanks @eleqtrizit.
- Gateway/node exec events: mark remote node `exec.started`, `exec.finished`, and `exec.denied` summaries as untrusted system events and sanitize node-provided command/output/reason text before enqueueing them, so remote node output cannot inject trusted `System:` content into later turns. (#62659) Thanks @eleqtrizit.
- Plugins/onboarding auth choices: prevent untrusted workspace plugins from colliding with bundled provider auth-choice ids during non-interactive onboarding, so bundled provider setup keeps operator secrets out of untrusted workspace plugin handlers unless those plugins are explicitly trusted. (#62368) Thanks @pgondhi987.
- Security/dependency audit: force `basic-ftp` to `5.2.1` for the CRLF command-injection fix and bump Hono plus `@hono/node-server` in production resolution paths.
- Android/pairing: clear stale setup-code auth on new QR scans, bootstrap operator and node sessions from fresh pairing, prefer stored device tokens after bootstrap handoff, and pause pairing auto-retry while the app is backgrounded so scan-once Android pairing recovers reliably again. (#63199) Thanks @obviyus.
- Matrix/gateway: wait for Matrix sync readiness before marking startup successful, keep Matrix background handler failures contained, and route fatal Matrix sync stops through channel-level restart handling instead of crashing the whole gateway. (#62779) Thanks @gumadeiras.
- Slack/media: preserve bearer auth across same-origin `files.slack.com` redirects while still stripping it on cross-origin Slack CDN hops, so `url_private_download` image attachments load again. (#62960) Thanks @vincentkoc.
- Reply/doctor: use the active runtime snapshot for queued reply runs, resolve reply-run SecretRefs before preflight helpers touch config, surface gateway OAuth reauth failures to users, and make `openclaw doctor` call out exact reauth commands. (#62693, #63217) Thanks @mbelinky.
- Control UI: guard stale session-history reloads during fast session switches so the selected session and rendered transcript stay in sync. (#62975) Thanks @scoootscooob.
- Gateway/chat: suppress exact and streamed `ANNOUNCE_SKIP` / `REPLY_SKIP` control replies across live chat updates and history sanitization so internal agent-to-agent control tokens no longer leak into user-facing gateway chat surfaces. (#51739) Thanks @Pinghuachiu.
- Auto-reply/NO_REPLY: strip glued leading `NO_REPLY` tokens before reply normalization and ACP-visible streaming so silent sentinel text no longer leaks into user-visible replies while preserving substantive `NO_REPLY ...` text. Thanks @frankekn.


---

## 💡 深度点评

作为开发者工具观察者，OpenClaw 在 2026.4.9 的更新中展现了其在「长效记忆架构」和「系统级安全防护」上的深度演进。以下是针对本次更新的技术点评：

### 核心亮点

*   **增强型 REM 记忆回填系统 (Grounded REM Backfill)**：引入了历史数据回填路径（`rem-harness`）和持久化事实提取流程。通过将旧的每日笔记重播至「梦境」（Dreams）和持久化存储，实现了短长期记忆的无缝整合。这解决了智能体在长时间跨度下记忆断层的问题，且无需维护两套独立的内存栈。
*   **Provider 鉴权别名机制 (Provider Auth Aliases)**：插件系统现在支持通过 `providerAuthAliases` 声明鉴权别名。这意味着不同变体的模型供应商可以共享环境变量、配置和 API 密钥初始化逻辑，极大简化了多模型环境下的鉴权配置冗余。
*   **QA 实验室「角色氛围」评估**：新增 Character-vibes 评测报告，支持模型对比与并行运行。这标志着 OpenClaw 的测试维度从单纯的逻辑正确性，扩展到了对智能体「人设一致性」和「行为风格」的量化评估。

### 值得注意的修复

*   **交互式 SSRF 隔离防护**：修复了一个关键安全漏洞（#63226），确保在点击、评估或钩子触发的页面跳转后，重新执行黑名单地址检测，防止通过交互式导航绕过 SSRF 隔离区。
*   **远程执行事件净化**：将远程节点的 `exec` 开始/结束/拒绝摘要标记为「不可信系统事件」，并严格过滤输出文本。此举有效防止了远程节点利用输出内容向后续会话注入伪造的 `System:` 指令。
*   **多端连接与消息泄露修复**：解决了 `NO_REPLY` 令牌泄露至用户界面的问题，并优化了 Slack 媒体附件在重定向时的鉴权保留逻辑；同时针对 Android 端 QR 扫码配对的稳定性进行了深度加固。

### 个人评价

2026.4.9 版本的 OpenClaw 已经从单纯的「模型转发层」进化为具备复杂状态管理能力的「智能体操作系统」。通过 Grounded REM 机制，它在探索大模型长效上下文管理上给出了非常工业化的方案。同时，该版本展现了极强的安全防御意识，尤其是在处理不可信工作区环境和远程节点输出时，采用了严格的非对称信任模型。整体方向明确：在保证极致安全的前提下，追求更具人格化和记忆深度的自主智能体体验。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-09 12:33:20*
