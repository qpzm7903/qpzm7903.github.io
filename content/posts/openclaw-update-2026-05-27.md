---
title: "🔧 Openclaw 更新日报 2026-05-27"
date: 2026-05-27T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.26

**发布日期**: 2026-05-27  
**⚠️ 新版本发布**

## Highlights

- Faster replies and startup: visible reply delivery now separates user-facing sends from slower follow-up work, command/model/plugin metadata is reused on hot paths, and Gateway startup avoids repeated plugin, channel, session, usage-cost, and filesystem scans.
- Better voice and Talk: realtime Talk runs can be inspected, steered, cancelled, or followed up from Web UI and Discord voice; wake-name handling is more tolerant without letting ambient speech trigger agents.
- More channels are production-ready: Telegram keeps typing/progress context and forum topics, iMessage handles attachment roots and duplicate local Messages sources, WhatsApp restores group/media behavior, Discord improves voice playback and model picking, and Signal/iMessage get reaction approvals.
- Safer agents: Codex app-server auth, compaction, source replies, sandbox path handling, and usage-limit recovery are more robust; OpenAI-compatible providers avoid empty-tool and malformed payload failures.
- More reliable replay and installs: legacy tool results, subagent spawn payloads, stale lock ownership, Windows stack-heavy startup, macOS restart validation, and Docker package preparation all fail less surprisingly.
- Better install/update/release confidence: Alpine installs, stable update channels, Docker/package timeouts, Windows/macOS proof lanes, Testbox/Crabbox delegation, and plugin publish checks all got hardened.
- New observability: Activity tab, gateway secret-prep traces, tool/model stream progress, OpenTelemetry LLM spans, release performance evidence, and richer missing telemetry signals make failures easier to inspect.

## Changes

- Transcripts: add core transcript capture and source-provider support for transcript-backed meeting summaries, including the renamed Transcripts docs and CLI surface.
- Auth: add named model login profiles and supported credential migration for Hermes, OpenCode, and Codex auth profiles, with explicit opt-out and non-interactive controls. (#85667) Thanks @fuller-stack-dev.
- Diagnostics: trace gateway secret preparation, classify skill/tool usage, surface model stream progress, add OpenTelemetry LLM content spans, and expose alertable telemetry for blocked tools, failover, stale sessions, liveness, oversized payloads, and webhook ingress. (#83019, #80370, #86191)
- Channels: add Signal reaction approvals, iMessage thumb approval reactions, and WhatsApp thumb approval reaction support so mobile approval flows work without textual `/approve` commands. (#85894, #85952, #85477)
- Agents/API: forward OpenAI sampling params through the Gateway and expose estimated context-budget status for active agent runs. (#84094)
- Android/iOS: add the Android pair-new-gateway action and improve mobile Talk mode surfaces, including iOS realtime Talk mode and Android offline voice/gateway recovery. (#86798, #86355) Thanks @ngutman.
- Performance: cache plugin metadata snapshots, package realpaths, stable gateway metadata, model cost indexes, channel resolution, usage-cost indexes, and session/auth hot-path facts so common Gateway and reply paths do less rediscovery. (#84649, #85843, #86517, #86678)
- Voice: expose shared realtime turn-context tracking through the realtime voice SDK and reuse it for Discord speaker attribution and wake-name context recovery.
- Voice: reuse shared realtime output activity tracking in Google Meet command and node audio bridges, including recent-output checks for local barge-in detection.
- Voice: expose shared realtime output activity tracking through the realtime voice SDK and reuse it for Discord playback activity and barge-in decisions.
- Voice: expose shared realtime consult question matching, speakable-result extraction, and alias-aware forced-consult coordination through the realtime voice SDK, then reuse it in Gateway Talk, Voice Call, and Discord voice paths.
- Voice: share activation-name matching and consult-transcript screening through the realtime voice SDK so Discord, browser voice, and meeting surfaces can reuse one implementation.

## Fixes

- Reply/perf: reduce visible reply delivery latency by preserving Telegram typing/progress context, lazy-loading slash-command startup metadata, avoiding hot-path model hydration, flag-gating Codex profiler timing, deferring context compaction maintenance, and tracking delivery timing. (#86989, #86990, #86991, #86992, #86993, #86994) Thanks @keshavbotagent.
- Reply/source delivery: keep TUI, Control UI, media, TTS, transcript, and Codex source-reply finals live without duplicate terminal events or stale replay artifacts.
- Agents/replay: repair legacy tool results before replay, preserve `sessions_spawn` transcript payloads, restore current guard checks, stage sandboxed workspace media, and keep duplicate transcripts tool display metadata from reappearing. (#82203, #86934, #87025) Thanks @martingarramon, @vincentkoc, and @joshavant.
- Codex: project newer OpenClaw chat history into resumed app-server threads and keep Codex turn timeouts inside the Codex runtime boundary so timeouts do not poison shared app-server clients or fall through to unrelated provider fallback. (#86677, #86476) Thanks @TurboTheTurtle and @pashpashpash.
- Config/doctor/update: narrow profiled tool-section doctor repair, keep runtime-injected legacy web-search provider config out of user-authored config validation, and keep prerelease tags excluded from stable updater resolution. (#87030, #86818, #86559) Thanks @joshavant, @luoyanglang, and @stevenepalmer.
- CLI/Windows: add a Windows-only stack-size respawn for stack-heavy startup paths, default CLI logs to local timestamps, and validate timeout/banner TTY state more strictly. (#87031, #85387) Thanks @giodl73-repo and @vincentkoc.
- Locking/security: require owner identity proof before stale plugin lock removal, memoize session lock owner arguments, and avoid writing default exec approval stores unless policy state actually changed. (#86814, #86964) Thanks @Alix-007 and @vincentkoc.
- Install/release: bound Docker package build, inventory, pack, and tarball preparation with process-group timeouts; pin shrinkwrap patch drift to the pnpm lock; harden macOS restart and dSYM packaging; and run release Docker/live timeout wrappers in the foreground so child processes cannot wedge gates.
- Telegram/network: treat `ENETDOWN` as a transient pre-connect network failure so Telegram sends, gateway unhandled-rejection handling, and cron network retries follow the same recovery path as sibling network outages. (#86762) Thanks @TurboTheTurtle.
- Telegram: preserve inbound text entities, overlapping DM replies, account topic cache sidecars, outbound reply context, targeted bot-command mentions, durable group retry targets, forum topic names, and native progress callbacks. (#83873, #85361, #85555, #85656, #85709, #86299, #86553) Thanks @SebTardif, @luoyanglang, and @neeravmakwana.
- iMessage: read image attachments from local Messages attachment roots, dedupe duplicate local Messages-source accounts, seed direct DM history, fix image/group media attachment commands, advance catchup cursors after live handling, and keep slash-command acknowledgements in the source conversation. (#82642, #85475, #86569, #86705, #86706, #86770) Thanks @homer-byte, @TurboTheTurtle, @swang430, and @OmarShahine.
- WhatsApp/QQ/Twitch/IRC/Slack: restore WhatsApp ack identity and group-drop warnings, make QQ Bot media respect `OPENCLAW_HOME`, serialize Twitch auth disconnects, store IRC channel routes canonically, and keep Slack downloaded files out of reply media. (#83833, #85309, #85777, #85794, #85906, #86318, #86697) Thanks @sliverp, @neeravmakwana, and @Kailigithub.


---

## 💡 深度点评

### 核心亮点

- **响应链路分离与缓存机制设计**：将用户可见的回复投递与低优先级的后续计算分离。在请求热路径与 Gateway 启动阶段全面引入缓存复用（涵盖插件元数据、模型成本索引、会话上下文及文件系统依赖），消除了重复的文件扫描和状态重载。
- **图像处理底层框架更替**：彻底移除 Sharp 和适用于 WhatsApp 的 Jimp 降级方案，全面迁移至 Rastermill。新后端统一接管了图像元数据提取、尺寸重置、EXIF 方向修正以及 PNG 透明通道优化，降低了跨平台环境下的原生编译门槛。
- **全链路可观测性增强**：引入 OpenTelemetry 对 LLM 内容 span 的追踪支持，新增 Gateway 密钥装载追踪与流式进度暴露。Control UI 新增无状态的 Activity 面板，支持在不落盘的情况下对工具调用进行实时审计。

### 值得注意的修复

- **并发锁泄漏与会话队列恢复**：强制实施会话锁的最大持有时间回收（max-hold reclaim），并确保任何形式的退出分支都会释放 embedded-attempt 锁。清理了因进程挂起引发的持续性 `SessionWriteLockTimeoutError` 队列阻塞问题。
- **Codex 运行时边界隔离**：将 Codex 轮次超时逻辑收敛于其自身的运行时边界内，防止异常超时状态向上层传播，避免了共享 app-server 客户端污染及错误的全局提供商降级。
- **本地通道（iMessage/Telegram）逻辑修正**：iMessage 修复了多个账户指向同一本地源时的多重实例化问题，消除了重复的 RPC 进程和双重消息派发；Telegram 将底层 `ENETDOWN` 正确归类为瞬时网络故障并接入标准重试恢复流。
- **容器化与进程生命周期控制**：为 Docker 镜像的依赖构建、包清点和压缩阶段引入了进程组级别的严格超时阻断，防止因僵尸子进程导致 CI 流水线或本地更新处于假死状态。

### 个人评价

本次更新将核心发力点集中在运行时健壮性与跨平台部署的稳定性上。通过热路径的计算拆分与强制死锁回收，框架在应对高并发和异常退出的容错表现有了底层支撑。图像处理组件向 Rastermill 迁移则直接减少了环境碎片化带来的部署摩擦。整体而言，这是一个工程化表现成熟的版本，将系统的可维护性与长期运行指标推向了企业级标准。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-27 08:23:17*
