---
title: "🔧 Openclaw 更新日报 2026-05-04"
date: 2026-05-04T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.2

**发布日期**: 2026-05-04  
**⚠️ 新版本发布**

## Highlights

- External plugin installation now covers diagnostics, onboarding, doctor repair, channel setup, install/update records, and artifact metadata while keeping bare package installs on npm for the first cutover. Thanks @vincentkoc.
- Gateway startup, session listing, task maintenance, prompt prep, plugin loading, and filesystem hot paths get targeted cache and fanout reductions for large or plugin-heavy installs.
- Control UI and WebChat reliability improves across Sessions, Cron, long-running Gateway WebSockets, grouped-message width, slash-command feedback, iOS PWA bounds, selection contrast, and Talk diagnostics.
- Channel and provider fixes cover Telegram topic commands and networking, Discord delivery and startup edge cases, OpenAI-compatible TTS/Realtime, OpenRouter/DeepSeek replay, Anthropic-compatible streaming, Brave/SearXNG/Firecrawl web search, and voice-call routing.

## Changes

- Gateway/startup: skip plugin-backed auth-profile overlays during startup secrets preflight, reducing gateway readiness latency while keeping reload and OAuth recovery paths overlay-capable. (#68327) Thanks @JIRBOY.
- Plugins/ClawHub: make diagnostics, onboarding, doctor repair, and channel setup carry ClawPack metadata through install records while keeping explicit `clawhub:` installs on ClawHub and bare package installs on npm for the launch cutover. Thanks @vincentkoc.
- Plugins/runtime: scope broad runtime preloads to the effective plugin ids derived from config, startup planning, configured channels, slots, and auto-enable rules instead of importing every discoverable plugin.
- Agents/runtime: reuse the startup-loaded plugin registry for request-time providers, tools, channel actions, web/capability/memory/migration helpers, and memoized provider extra-params so stable embedded-run inputs no longer repeat plugin registry resolution while model-specific transport hook patches stay isolated. Thanks @DmitryPogodaev.
- Agents/runtime: memoize transcript replay-policy resolution for stable config and process-env runs while preserving custom-env provider hook behavior. Thanks @DmitryPogodaev.
- Infra/path-guards: add a fast path for canonical absolute POSIX containment checks, avoiding repeated `path.resolve` and `path.relative` work in hot filesystem walkers. Refs #75895, #75575, and #68782. Thanks @Enderfga.
- Tools: add a platform-level tool descriptor planner for descriptor-first visibility, generic availability checks, and executor references. Thanks @shakkernerd.
- Plugins/tools: cache plugin tool descriptors captured from `api.registerTool(...)` so repeated prompt-time planning can skip plugin runtime loading while execution still loads the live plugin tool. (#76079) Thanks @shakkernerd.
- Docs/Codex: clarify that ChatGPT/Codex subscription setups should use `openai/gpt-*` with `agentRuntime.id: "codex"` for native Codex runtime, while `openai-codex/*` remains the PI OAuth route. Thanks @pashpashpash.
- Plugins/source checkout: load bundled plugins from the `extensions/*` pnpm workspace tree in source checkouts, so plugin-local dependencies and edits are used directly while packaged installs keep using the built runtime tree. Thanks @vincentkoc.
- Plugins/beta: externalize ACPX behind the official `@openclaw/acpx` package so packaged installs keep ACP harness adapter binaries out of core until the ACP backend is installed. Thanks @vincentkoc.
- Plugins/beta: externalize diagnostics OpenTelemetry behind the official `@openclaw/diagnostics-otel` package so packaged installs keep the OTEL dependency stack out of core until the plugin is installed. Thanks @vincentkoc.

## Fixes

- CLI/message: skip eager model context warmup and preserve channel-declared gateway execution for Discord and Telegram message actions, avoiding Codex app-server/model discovery during simple send/read commands. Thanks @fuller-stack-dev.
- Codex/app-server: resolve managed binaries from bundled `dist` chunks and from the `@openai/codex` package bin when installs do not provide a nearby `.bin/codex` shim, avoiding false missing-binary startup failures.
- Plugins/ClawHub: use the ClawHub artifact resolver response as the install decision before downloading, keeping legacy ZIP fallback and future ClawPack npm-pack installs on the same explicit resolver path. Thanks @vincentkoc.
- Plugins/ClawHub: keep bare plugin package specs on npm for the launch cutover and reserve ClawHub resolution for explicit `clawhub:` specs until ClawHub pack readiness is deployed. Thanks @vincentkoc.
- Plugins/source checkout: discover source-only plugins such as Codex from the `extensions/*` workspace while using npm package excludes as the packaged-core boundary, removing the stale core-bundle metadata path.
- Plugins/ClawHub: install ClawPack artifacts from the explicit npm-pack `.tgz` resolver path and persist artifact kind, npm integrity, shasum, and tarball metadata for update and diagnostics flows. Thanks @vincentkoc.
- Control UI: allow deployments to configure grouped chat message max-width with a validated `gateway.controlUi.chatMessageMaxWidth` setting instead of patching bundled CSS after upgrades. Fixes #67935. Thanks @xiew4589-lang.
- Control UI/Cron: ignore malformed persisted cron rows without valid payloads before they enter UI state and guard stale cron render paths, preventing blank Control UI sections after a bad cron snapshot. Fixes #55047 and #54439; supersedes #54550 and #54552.
- Control UI/sessions: bound the default Sessions tab query to recent activity and fewer rows, avoiding expensive full-history loads while keeping filters editable. Fixes #76050. (#76051) Thanks @Neomail2.
- Gateway/channels: cap startup fanout at four channel/account handoffs and recover from Bonjour ciao self-probe races, reducing Windows startup stalls with many Telegram accounts. Fixes #75687.
- Gateway/sessions: keep `sessions.list` polling responsive on large session stores by reusing list-safe session cache/indexes and returning a lightweight compaction checkpoint preview instead of heavyweight summaries. Thanks @rolandrscheel.
- Control UI/Gateway: keep long-running dashboard WebSocket sessions alive with protocol pings and keep Stop available after reconnect or reload by recovering session-scoped active-run abort state. Fixes #70991. Thanks @alexandre-leng.


---

## 💡 深度点评

### 核心亮点

- **插件生态正式基建化**：ClawPack 安装链路基本成型——onboarding、diagnostics、doctor repair、channel setup 都开始携带 ClawPack 元数据走显式解析器路径。这是从单体外壳走向开放生态的关键一步，ClawHub 方向越来越清晰。
- **性能优化覆盖面很广**：Gateway 启动、session 列表、任务维护、prompt 准备、plugin 加载、文件系统路径检查——这些都是大安装量下的热点路径。cache/fanout 减少不新鲜，但一次性从多个方向同时下手，说明团队在做一次扎实的"铺路式"性能 cleanup。
- **Control UI 和 WebChat 持续成熟**：Session 列表默认只查近期活跃，长 WebSocket 加了协议 ping，cron 空行不再炸 UI，grouped chat 宽度可配。这些改完，Control UI 才开始像"能稳定给人用"的样子。

### 值得关注的修复

- Malformed cron 数据不再炸白屏（#55047）——这个问题如果你跑过 Control UI 可能深有体会，属于那种一旦触发就让整个页面报废的 bug。
- Gateway session 列表响应优化（@rolandrscheel）——session 多到一定规模时，这个效果会很明显。该属性对开发者模式和 dashboard 用户都很友好。
- Long-running WebSocket 加上协议 ping 防断连（#70991）——这对于 dashboard 的大屏监控场景是个很实在的改进。
- Telegram 多账号启动的 fanout 限制——Windows 用户会直接受益，但所有多账号部署都会减少启动毛刺。
- ClawHub 安装现在存 artifact kind/npm integrity/shasum/tarball metadata，之后的 update 和 diagnostics 流程就可以基于真实元数据而不是猜了。

### 个人评价

2026.5.2 看起来是"生态准备版"。插件外部化（$clawpack、acpx、diagnostics-otel）、性能地基加固、Control UI 可靠性提升，这几条线放在一起，信号很明显——OpenClaw 正在为一个更开放、更可靠的运行时环境做准备。如果你只是简单跑几个 channel，感知有限；但要是挂了很多 plugin、大量 channel、跑 dashboard，这个版本的改进你都能体会到。

---

**数据来源**: [OpenClaw CHANGELOG](https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md)

*Generated by OpenClaw at 2026-05-04 08:43:08*
