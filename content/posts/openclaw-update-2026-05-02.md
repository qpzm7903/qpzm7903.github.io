---
title: "🔧 Openclaw 更新日报 2026-05-02"
date: 2026-05-02T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.30

**发布日期**: 2026-05-02  
**⚠️ 新版本发布**

## Changes

- Dependencies: refresh bundled runtime and plugin dependency pins, including Pi 0.71.1, OpenAI 6.35.0, Codex 0.128.0, Zod 4.4.1, and Matrix 41.4.0. Thanks @mariozechner.
- Agents/workspace: add `agents.defaults.skipOptionalBootstrapFiles` for skipping selected optional workspace files during bootstrap without disabling required workspace setup. (#62110) Thanks @mainstay22.
- Plugins/CLI: add first-class `git:` plugin installs with ref checkout, commit metadata, normal scanner/staging, and `plugins update` support for recorded git sources. Thanks @badlogic.
- Google Meet: add live caption health for Chrome transcribe mode, including caption observer state, transcript counters, last caption text, and recent transcript lines in status and doctor output. Refs #72478. Thanks @DougButdorf.
- Voice Call/Google Meet: add Twilio Meet join phase logs around pre-connect DTMF, realtime stream setup, and initial greeting handoff for easier live-call debugging. Thanks @donkeykong91 and @PfanP.
- macOS app: move recent session context rows into a Context submenu while keeping usage and cost details root-level, so the menu bar companion stays compact with many active sessions. Thanks @guti.
- Gateway/SDK: add SDK-facing tools.invoke RPC with shared HTTP policy, typed approval/refusal results, and SDK helper support. Refs #74705. Thanks @BunsDev and @ai-hpc.
- Discord: keep active buttons, selects, and forms working across Gateway restarts until they expire, so multi-step Discord interactions are less likely to break during upgrades or restarts. Thanks @amknight.
- Messages/docs: clarify that `BodyForAgent` is the primary inbound model text while `Body` is the legacy envelope fallback, and add Signal coverage so channel hardening patches target the real prompt path. Refs #66198. Thanks @defonota3box.
- Slack: publish a safe default App Home tab view on `app_home_opened` and include the Home tab event in setup manifests. Fixes #11655; refs #52020. Thanks @TinyTb.
- Slack: keep track of bot-participated threads across restarts, so ongoing threaded conversations can continue auto-replying after the Gateway is restarted. Thanks @amknight.
- Control UI/Usage: add UTC quarter-hour token buckets for the Usage Mosaic and reuse them for hour filtering, keeping the legacy session-span fallback for older summaries. (#74337) Thanks @konanok.

## Fixes

- fix: block workspace CLOUDSDK_PYTHON override and always set trusted interpreter for gcloud. (#74492) Thanks @pgondhi987.
- Providers/Z.AI: move the bundled GLM catalog and auth env metadata into the plugin manifest, so `models list --all --provider zai` shows the full known catalog without duplicated runtime seed data. Thanks @shakkernerd.
- Providers/Qianfan and Providers/Stepfun: declare setup auth metadata (`api-key` method, `QIANFAN_API_KEY`, `STEPFUN_API_KEY`) in the plugin manifest so onboarding and `models setup` surface the expected env var without falling back to legacy `providerAuthEnvVars` runtime seed data. Thanks @shakkernerd.
- fix(infra): block ambient Homebrew env vars from brew resolution. (#74463) Thanks @pgondhi987.
- Onboarding/configure: avoid staging every default plugin runtime dependency after config writes, so skipped setup flows only prepare config-selected plugin deps instead of pulling broad feature-plugin packages. Thanks @vincentkoc.
- Thinking/providers: resolve bundled provider thinking profiles through lightweight provider policy artifacts when startup-lazy providers are not active, so OpenAI Codex GPT-5.x keeps xhigh available in Gateway session validation. Fixes #74796. Thanks @maxschachere.
- Security/Windows: ignore workspace `.env` system-path variables and resolve stale-process `taskkill.exe` from the validated Windows install root, preventing repository-local env files from redirecting cleanup helpers. Thanks @pgondhi987.
- CLI/plugins: refresh persisted plugin registry policy in place for `plugins enable` and `plugins disable`, so routine toggles no longer rebuild and hash every plugin source when the target is already indexed. Thanks @vincentkoc.
- CLI/plugins: scope install and enable slot selection to the selected plugin manifest/runtime fallback, so plugin installs no longer load every plugin runtime or broad status snapshot just to update memory/context slots. Thanks @vincentkoc.
- Plugins/TTS: keep bundled speech-provider discovery available on cold package Gateway paths and add bundled plugin matrix runtime probes for health, readiness, RPC, TTS discovery, and post-ready runtime-deps watchdog coverage. Refs #75283. Thanks @vincentkoc.
- Google Meet/Twilio: show delegated voice call ID, DTMF, and intro-greeting state in `googlemeet doctor`, and avoid claiming DTMF was sent when no Meet PIN sequence was configured. Refs #72478. Thanks @DougButdorf.
- Plugins/tools: prefer built bundled plugin code during tool discovery and skip channel runtime hydration while preserving companion provider registrations, reducing per-run plugin-tool prep cost without dropping executable plugin tools. Fixes #75290. Thanks @thanos-openclaw.


---

## 💡 深度点评

这是 openclaw 2026.4.30 版本的深度技术点评。

### 核心亮点

*   **插件系统 Git 原生支持**：新增 `git:` 协议直接安装插件的能力。支持特定 ref 检出、提交元数据记录以及通过 `plugins update` 追踪 Git 源。这一变更显著提升了开发者分发和测试非官方插件的效率，标志着插件管理从单一注册表向分布式生态演进。
*   **跨重启的状态持久化（Discord/Slack）**：优化了网关重启时的交互连续性。Discord 的交互按钮、选择菜单和表单在重启后仍能保持活性直至过期；Slack 能够追踪机器人参与的线程。对于长对话或多步工作流应用，这极大降低了因系统升级或维护导致的中断率。
*   **企业级配置与 SDK 增强**：引入了 `tools.invoke` RPC 调用规范，支持统一的 HTTP 策略和类型化审批流。同时，配置系统新增 `$include` 指令，允许从审核过的根目录导入外部配置。这些底层改动强化了 OpenClaw 在复杂基础设施中的管控能力。

### 值得注意的修复

*   **大规模会话稳定性（OOM 防护）**：针对超长对话记录（Transcripts），引入了带边界的流式读取和分页加载机制，避免在生成摘要、清理快照或客户端请求历史时因一次性加载海量数据导致网关内存溢出（OOM）。
*   **关键安全漏洞修复**：拦截了工作区 `.env` 文件对系统级环境变量（如 Windows 的 `COMSPEC`、`taskkill.exe` 路径及 `CLOUDSDK_PYTHON`）的篡改风险。这一修复防止了恶意代码通过仓库本地环境配置文件重定向系统执行流，增强了沙箱安全性。
*   **多模态交互可靠性**：修复了 Google Meet 和 Twilio 语音通话中的多个时序问题，包括 DTMF 拨号音发送时机、实时流建立与初始欢迎语的竞态逻辑，以及 iMessage (BlueBubbles) 音频附件 UTI 识别失效的问题。

### 个人评价

2026.4.30 版本是一个明显的「生产环境加固」迭代。它没有堆砌浮夸的新模型接口，而是将重心放在了提升复杂交互的容错性（如重启不丢状态）和极端情况下的系统稳健性（如超长日志的内存控制）上。对于在生产环境中使用 OpenClaw 的开发者来说， Git 插件支持和安全路径锁定是该版本最具实操价值的改进。整体来看，OpenClaw 正在从一个 AI 工具箱向一个更标准、更安全的代理中间件平台转变。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-02 09:01:47*
