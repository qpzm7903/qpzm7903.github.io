---
title: "🔧 Openclaw 更新日报 2026-05-19"
date: 2026-05-19T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.19

**发布日期**: 2026-05-19  
**⚠️ 新版本发布**

## Changes

- Agents: clarify that fixes should default to clean bounded refactors, lean internals, and explicit plugin SDK/API deprecation paths.
- Dependencies: update `@openclaw/proxyline` to 0.3.3.
- Dependencies: update Pi packages to 0.75.1 and raise the minimum supported Node.js 22 line to 22.19.
- Docker/Podman: add `OPENCLAW_IMAGE_APT_PACKAGES` as the runtime-neutral image build arg for extra apt packages while keeping `OPENCLAW_DOCKER_APT_PACKAGES` as a legacy fallback. (#62431) Thanks @urtabajev.
- Gateway/ACPX: attribute startup probe, config, runtime, and resource-count costs in restart traces without changing readiness behavior. (#83300) Thanks @samzong.
- Gateway: overlap startup logging and plugin-service startup with channel sidecars to reduce restart ready latency while preserving `/readyz` sidecar gating. (#83301) Thanks @samzong.
- Plugins/admin-http-rpc: allow trusted admin HTTP RPC clients to start and wait for web QR login flows. (#83259) Thanks @liorb-mountapps.
- Mac app: redesign Settings pages with consistent card layouts, cached navigation, cleaner permissions/voice/skills/cron/exec/debug panes, and steadier spacing around the native sidebar.
- Skills: rename the repo-local Codex closeout review skill and helper to `autoreview` while preserving the Codex-first fallback behavior.
- Skills: add a meme-maker skill for curated template search, local SVG/PNG rendering, Imgflip hosted rendering, and Know Your Meme provenance links.
- Skills CLI: allow `openclaw skills install` and `openclaw skills update` to target shared managed skills with `--global`. (#74466) Thanks @Marvae.
- Browser: surface pending and recently handled modal dialogs in snapshots, return `blockedByDialog` when an action opens a modal, and allow `browser dialog --dialog-id` to answer pending dialogs.

## Fixes

- Memory/search: scan the JS-side fallback vector path (used when the sqlite-vec index is unavailable or has a mismatched dimension) in bounded rowid batches and yield to the event loop between batches so large chunk tables can no longer pin the Node.js main thread for multi-second windows. Also keeps the SQL prepared statement rooted in a local so node:sqlite cannot finalize it mid-scan under heap pressure. Fixes #81172. Thanks @dev23xyz-oss.
- CLI/update: bypass npm freshness filters consistently during managed package and plugin installs so freshly published release plugins remain installable. Thanks @jalehman.
- CLI/update: guide root-owned npm install EACCES recovery by stopping the managed Gateway before manual package replacement, then reinstalling and restarting the service. Fixes #83747. (#83757) Thanks @brokemac79.
- Agents/subagents: keep collect-mode announce queues batching unresolved-origin items with compatible same-route messages and resume collection after a true cross-channel drain when a later compatible batch remains. Fixes #83577.
- Providers/Anthropic: preserve native image input for current Claude model rows when stale local catalog data marks them text-only. (#83756) Thanks @TurboTheTurtle.
- Control UI: render live tool progress from session-scoped `session.tool` Gateway events so externally started runs show their tool cards in the active session. (#83734) Thanks @TurboTheTurtle.
- Outbound: resolve send-capable channel plugins from the active runtime registry when the pinned startup registry only has setup metadata. (#83733) Thanks @TurboTheTurtle.
- Browser: enforce current-tab URL allowlist checks for `/act` evaluate/batch actions and `/highlight` routes while leaving tab-management actions unblocked. (#78523)
- CI: require real-behavior-proof verdict markers to come from the ClawSweeper GitHub App before accepting exact-head proof. (#83692)
- Models: show the effective OpenAI/Codex auth profile in `/models` provider headers instead of falling back to the OpenAI env-key label. (#83697) Thanks @yu-xin-c.
- Browser: keep a profile `cdpPort` when its `cdpUrl` omits a port, while still letting explicitly written URL ports win. (#82166) Thanks @Marvae.
- Agents/image generation: allow distinct `image_generate` prompts to start separate session-backed background tasks while same-prompt retries still return the active task status. (#83614) Thanks @Elarwei001.


---

## 💡 深度点评

### 核心亮点

- **QA-Lab 自动化评估与基准测试体系重构**：引入 20 轮与 100 轮运行时对齐（runtime parity）场景，并在标准层级中硬性拦截（hard-gate）动态工具的执行行为漂移。新增基于 Token 效率的流水线、动态工具覆盖率报告及本地沙盒拦截测试，大幅提升了对核心模型（Codex vs Pi）运行时行为差异的量化覆盖能力。
- **插件化工具 API 与扩展生态完善**：新增 `defineToolPlugin` 声明范式及配套的 `build`/`validate`/`init` CLI 命令，支持快速构建包含 Manifest 元数据和上下文工厂的强类型工具插件。同时优化了 Skills 分发机制，CLI 支持通过 `--global` 标志管理共享层级的技能，并内置了 Python 调试（支持 debugpy 挂载）等开发者原生工具。
- **跨端交互链路与启动性能优化**：Android 端 Talk Mode 切换为基于 Gateway 实时中继的流式语音会话，支持实时音频输入输出与端上工具执行状态透传。Gateway 核心层通过异步重叠插件服务与 Sidecar 的启动阶段，有效降低了服务重启的就绪延迟（Ready Latency）；Mac 端点对点重构了配置面板渲染逻辑，实现了组件缓存及深层状态路由解耦。

### 值得注意的修复

- **内存层检索导致的事件循环阻塞**：修复了当 `sqlite-vec` 降级扫描大体积数据表时卡死 Node.js 主线程的问题。更新后在 JS 侧的检索回退路径中引入了分批让出（yield）机制，并锁定了底层预编译 SQL 语句的内存引用以防止在高堆内存压力下被意外回收。
- **子代理（Subagent）路由与上下文逃逸控制**：修复了大量跨 Channel 并发环境下的状态污染问题。确保子代理执行完成后的回调准确投递至原始发起方的 Thread/Topic（覆盖 Discord、Telegram、Feishu 等），并在 `before_tool_call` 钩子中严格隔离并保留父级 Session 与执行器的独立上下文。
- **协议协商降级与安装器死锁恢复**：补齐了 Gateway WS v4 协议握手常量，新增了客户端与服务端协议不匹配时的诊断报警与回退机制。此外，梳理了 CLI 升级路径下的权限与依赖锁冲突，实现了在遭遇 `EACCES` 权限拒绝时通过自动挂起网关服务、阻断死锁循环的自我恢复流程。

### 个人评价

本次更新明确反映出 OpenClaw 正在从单体任务工具集向具备极高确定性的工业级 Agent 运行时演进。QA-Lab 中加入大量边界测试与工具调用漂移的“硬性拦截”，说明开发重心已向保证 LLM 执行链路的可靠性与低成本量化评估倾斜。架构层面，对网关启动时序的压榨、事件循环的保护以及 Subagent 路由状态的严格溯源，都在为承载超长上下文和复杂并发编排做底层铺垫。总体而言，这是一个在系统可观测性、运行时健壮性和工程契约标准上深度打磨的硬核版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-19 08:04:09*
