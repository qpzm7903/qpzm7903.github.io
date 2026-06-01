---
title: "🔧 Openclaw 更新日报 2026-06-01"
date: 2026-06-01T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.31

**发布日期**: 2026-06-01  
**⚠️ 新版本发布**

## Highlights

- Agents and CLI-backed runtimes recover more cleanly from interrupted tool calls, stale session bindings, compaction handoffs, and media delivery retries. (#88129, #88136, #88141, #88162, #88182)
- Channels and mobile delivery are steadier across Telegram, WhatsApp, iMessage, Slack, Discord, Microsoft Teams, Google Chat, Google Meet, and iOS realtime Talk. (#88096, #88105, #88183, #88231)
- Provider and plugin requests now bound more timers, retries, OAuth/device-code lifetimes, media downloads, local service probes, and generated-content polling paths before they can hang a run.
- Skills, session metadata, gateway runtime state, plugin metadata, and store writes do less repeated work on hot paths while keeping config and dispatch behavior stable.
- Skills and plugin loading now handle stale disabled snapshots and loader failures more clearly, so channel turns avoid disabled SecretRefs and operators get better recovery guidance. (#79072, #79173) Thanks @zeus1959.
- Workboard, SecretRef plugin manifests, hosted iOS push relay, and external Copilot/Tokenjuice packaging add broader orchestration, integration, and plugin delivery surfaces. (#82326, #87469, #87796, #88107, #88117)
- Release, CI, Docker, E2E, and diagnostics lanes now cap more logs, response bodies, readiness probes, artifact checks, and status polling so failures report bounded proof instead of stalling.

## Changes

- Docs: add a dedicated Skill Workshop guide covering governed skill creation, reviewable proposals, CLI, Gateway, agent tool behavior, approval policy, support files, and recovery. Thanks @shakkernerd.
- Skills: let the `skill_workshop` agent tool apply, reject, and quarantine explicit proposals through the guarded review flow. Thanks @shakkernerd.
- Skills: let proposals carry approved support files under standard skill folders, with scanner, hash, and rollback safeguards. Thanks @shakkernerd.
- Skills: let pending proposals be revised in place with versioned, dated proposal frontmatter before approval. Thanks @shakkernerd.
- Skills: add Skill Workshop with pending proposals, CLI/Gateway review actions, rollback metadata, and the `skill_workshop` agent tool. Thanks @shakkernerd.
- Plugins: externalize Tokenjuice as the official `@openclaw/tokenjuice` plugin with npm and ClawHub publish metadata.
- Plugins: externalize the GitHub Copilot agent runtime as the official `@openclaw/copilot` plugin with npm and ClawHub publish metadata.
- iOS: add hosted push relay defaults, realtime Talk playback, and a guarded WebSocket ping path for more reliable mobile sessions. (#88096, #88105, #88231)
- Workboard: add orchestration primitives and agent coordination tools for multi-agent planning and run tracking. (#87469)
- Code mode: add internal namespaces for scoped agent/global sessions and exact namespace tool dispatch. (#88043)
- Control UI: add a Dreaming-tab agent selector and propagate the selected agent through Dreaming status, diary, and diary actions. (#78748) Thanks @stevenepalmer.
- Plugins: add a SecretRef provider integration manifest contract and extract shared LLM core packages for provider/plugin reuse. (#82326, #88117)

## Fixes

- Agents/TUI: keep local custom provider runs from loading plugin runtime and auth alias metadata when plugins are disabled.
- Agents/media: keep async image, music, and video generation starts from ending the Codex turn, so mixed requests can continue with summaries or other work while media renders in the background.
- Agents/Codex: keep public OpenAI API-key profiles from being treated as native Codex app-server auth while preserving persisted Codex OAuth sessions.
- Control UI: keep collapsed tool cards labeled with the tool name and action instead of generic output text. Thanks @shakkernerd.
- Agents/Codex: surface Skill Workshop guidance in Codex app-server prompts when `skill_workshop` is available. Thanks @shakkernerd.
- Agents/auth: write auth profiles atomically, add force re-login recovery, preserve workspaces during state-only uninstall, and compact before oversized turns so recovery paths avoid partial state.
- Skills: skip disabled skill env overrides from stale persisted snapshots so disabled skill `apiKey` SecretRefs cannot abort embedded or channel turns. (#79072, #79173) Thanks @zeus1959.
- CLI: avoid live catalog validation during `openclaw agents add`, so adding a secondary agent no longer depends on provider catalog availability. (#76284, #88314) Thanks @zhangguiping-xydt.
- CLI: keep `plugins list --json` on the snapshot-only path so plugin sweeps avoid loading the full runtime status graph.
- Plugins: make PixVerse external-plugin ClawHub metadata explicit and keep it out of bundled dist builds.
- Plugins: clarify plugin loader failure guidance so missing or incompatible plugin packages point operators at the right repair path.
- Cron: keep SQLite cron migrations compatible with legacy run-log tables, archived job stores, diagnostic cron names, and legacy one-shot delete-after-run behavior. (#88285)


---

## 💡 深度点评

### 核心亮点

- **引入 Skill Workshop 与规范化技能生命周期**
  本版本实现了结构化的技能提案审查与加载流。新增的 `skill_workshop` 工具允许智能体直接介入提案的审批、拒绝与隔离。同时，底层统一了核心技能的加载和状态过滤，并加入了回滚机制和哈希安全校验，大幅提升了扩展体系的安全可控性。
- **架构级插件解耦与 Workboard 多智能体编排**
  核心生态进一步模块化，官方将 GitHub Copilot 和 Tokenjuice 抽离为独立的 npm 插件（`@openclaw/copilot` 和 `@openclaw/tokenjuice`）。同时，Workboard 引入了底层编排原语和协调工具，正式为多智能体协同规划和运行状态追踪提供框架层面的支持。
- **异步媒体生成与多端连接稳定性重构**
  在交互层面，异步生成图片、音视频等任务不再阻塞并强制结束当前的 Codex 轮次，使混合并发请求成为可能。针对 iOS 平台及主流通讯渠道（Telegram、Slack、WhatsApp 等），补充了推送中继默认配置、WebSocket 探活机制以及更稳健的重试策略，移动端会话抖动大幅减少。

### 值得注意的修复

- **修复失效技能中断会话流的 Bug**：针对携带失效 `apiKey` SecretRefs 的已禁用技能快照，运行时将正确跳过其环境变量覆盖，彻底解决了由此导致的嵌入式或渠道轮次意外中止问题（#79072, #79173）。
- **解除 CLI 添加智能体时的网络强依赖**：优化了 `openclaw agents add` 的逻辑，绕过了实时的 Provider 目录验证，确保在目录服务不可达或离线状态下，依然能顺利添加辅助智能体（#76284, #88314）。
- **Codex 认证隔离与原子化状态恢复**：修复了公开的 OpenAI API Key 配置污染原生 Codex 认证源的问题。同时通过原子化的配置文件写入和强制重新登录恢复机制，保证了在工具调用中断或压缩交接等极端场景下状态的完整性。
- **全局防御性超时与边界限制**：系统级地对各 Provider 的外部请求（如大体积媒体下载、OAuth 生命周期、长时间轮询）增加了严格的超时边界与重试上限，有效防止了死锁或挂起导致的运行时停滞。

### 个人评价

本次更新体现了 openclaw 从“功能堆叠”向“生产级健壮性”演进的明确技术路线。大量针对超时控制、资源竞态、死锁恢复以及遗留状态清理的防御性重构，显著增强了系统在长周期运行和复杂网络环境下的底盘稳定性。同时，核心插件的外部化抽离与 Skill Workshop 审查流的建立，表明官方正在着手规范化开发者生态边界。整体而言，这是一个重在“还技术债”与“立规范”的版本，对依赖多智能体复杂编排的高阶用户极具工程价值。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-06-01 08:05:42*
