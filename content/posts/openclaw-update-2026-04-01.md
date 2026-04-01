---
title: "🔧 Openclaw 更新日报 2026-04-01"
date: 2026-04-01T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.3.31

**发布日期**: 2026-04-01  
**⚠️ 新版本发布**

## Breaking

- Nodes/exec: remove the duplicated `nodes.run` shell wrapper from the CLI and agent `nodes` tool so node shell execution always goes through `exec host=node`, keeping node-specific capabilities on `nodes invoke` and the dedicated media/location/notify actions.
- Plugin SDK: deprecate the legacy provider compat subpaths plus the older bundled provider setup and channel-runtime compatibility shims, emit migration warnings, and keep the current documented `openclaw/plugin-sdk/*` entrypoints plus local `api.ts` / `runtime-api.ts` barrels as the forward path ahead of a future major-release removal.
- Skills/install and Plugins/install: built-in dangerous-code `critical` findings and install-time scan failures now fail closed by default, so plugin installs and gateway-backed skill dependency installs that previously succeeded may now require an explicit dangerous override such as `--dangerously-force-unsafe-install` to proceed.
- Gateway/auth: `trusted-proxy` now rejects mixed shared-token configs, and local-direct fallback requires the configured token instead of implicitly authenticating same-host callers. Thanks @zhangning-agent, @jacobtomlinson, and @vincentkoc.
- Gateway/node commands: node commands now stay disabled until node pairing is approved, so device pairing alone is no longer enough to expose declared node commands. (#57777) Thanks @jacobtomlinson.
- Gateway/node events: node-originated runs now stay on a reduced trusted surface, so notification-driven or node-triggered flows that previously relied on broader host/session tool access may need adjustment. (#57691) Thanks @jacobtomlinson.

## Changes

- ACP/plugins: add an explicit default-off ACPX plugin-tools MCP bridge config, document the trust boundary, and harden the built-in bridge packaging/logging path so global installs and stdio MCP sessions work reliably. (#56867) Thanks @joe2643.
- Agents/LLM: add a configurable idle-stream timeout for embedded runner requests so stalled model streams abort cleanly instead of hanging until the broader run timeout fires. (#55072) Thanks @liuy.
- Agents/MCP: materialize bundle MCP tools with provider-safe names (`serverName__toolName`), support optional `streamable-http` transport selection plus per-server connection timeouts, and preserve real tool results from aborted/error turns unless truncation explicitly drops them. (#49505) Thanks @ziomancer.
- Android/notifications: add notification-forwarding controls with package filtering, quiet hours, rate limiting, and safer picker behavior for forwarded notification events. (#40175) Thanks @nimbleenigma.
- Background tasks: turn tasks into a real shared background-run control plane instead of ACP-only bookkeeping by unifying ACP, subagent, cron, and background CLI execution under one SQLite-backed ledger, routing detached lifecycle updates through the executor seam, adding audit/maintenance/status visibility, tightening auto-cleanup and lost-run recovery, improving task awareness in internal status/tool surfaces, and clarifying the split between heartbeat/main-session automation and detached scheduled runs. Thanks @mbelinky and @vincentkoc.
- Background tasks: add the first linear task flow control surface with `openclaw flows list|show|cancel`, keep manual multi-task flows separate from one-task auto-sync flows, and surface doctor recovery hints for obviously orphaned or broken flow/task linkage. Thanks @mbelinky and @vincentkoc.
- Channels/QQ Bot: add QQ Bot as a bundled channel plugin with multi-account setup, SecretRef-aware credentials, slash commands, reminders, and media send/receive support. (#52986) Thanks @sliverp.
- Diffs: skip unused viewer-versus-file SSR preload work so `diffs` view-only and file-only runs do less render work while keeping mode outputs aligned. (#57909) thanks @gumadeiras.
- Tasks: add a minimal SQLite-backed task flow registry plus task-to-flow linkage scaffolding, so orchestrated work can start gaining a first-class parent record without changing current task delivery behavior. Thanks @mbelinky and @vincentkoc.
- Tasks: persist blocked state on one-task task flows and let the same flow reopen cleanly on retry, so blocked detached work can carry a parent-level reason and continue without fragmenting into a new job. Thanks @mbelinky and @vincentkoc.
- Tasks: route one-task ACP and subagent updates through a parent task-flow owner context, so detached work can emerge back through the intended parent thread/session instead of speaking only as a raw child task. Thanks @mbelinky and @vincentkoc.
- LINE/outbound media: add LINE image, video, and audio outbound sends on the LINE-specific delivery path, including explicit preview/tracking handling for videos while keeping generic media sends on the existing image-only route. (#45826) Thanks @masatohoshino.

## Fixes

- Slack: stop retry-driven duplicate replies when draft-finalization edits fail ambiguously, and log configured allowlisted users/channels by readable name instead of raw IDs.
- Agents/OpenAI Responses: normalize raw bundled MCP tool schemas on the WebSocket/Responses path so bare-object, object-ish, and top-level union MCP tools no longer get rejected by OpenAI during tool registration. (#58299) Thanks @yelog.
- ACP/security: replace ACP's dangerous-tool name override with semantic approval classes, so only narrow readonly reads/searches can auto-approve while indirect exec-capable and control-plane tools always require explicit prompt approval. Thanks @vincentkoc.
- ACP/sessions_spawn: register ACP child runs for completion tracking and lifecycle cleanup, and make registration-failure cleanup explicitly best-effort so callers do not assume an already-started ACP turn was fully aborted. (#40885) Thanks @xaeon2026 and @vincentkoc.
- ACP/tasks: mark cleanly exited ACP runs as blocked when they end on deterministic write or authorization blockers, and wake the parent session with a follow-up instead of falsely reporting success.
- ACPX/runtime: derive the bundled ACPX expected version from the extension package metadata instead of hardcoding a separate literal, so plugin-local ACPX installs stop drifting out of health-check parity after version bumps. (#49089) Thanks @jiejiesks and @vincentkoc.
- Agents/Anthropic failover: treat Anthropic `api_error` payloads with `An unexpected error occurred while processing the response` as transient so retry/fallback can engage instead of surfacing a terminal failure. (#57441) Thanks @zijiess and @vincentkoc.
- Agents/compaction: keep late compaction-retry completions from double-resolving finished compaction futures, so interrupted or timed-out compactions stop surfacing spurious second-completion races. (#57796) Thanks @joshavant.
- Agents/disabled providers: make disabled providers disappear from default model selection and embedded provider fallback, while letting explicitly pinned disabled providers fail with a clear config error instead of silently taking traffic. (#57735) Thanks @rileybrown-dev and @vincentkoc.
- Agents/OAuth output: force exec-host OAuth output readers through the gateway fs policy so embedded gateway runs stop crashing when provider auth writes land outside the current sandbox workspace. (#58249) Thanks @joshavant.
- Agents/system prompt: fix `agent.name` interpolation in the embedded runtime system prompt and make provider/model fallback text reflect the effective runtime selection after start. (#57625) Thanks @StllrSvr and @vincentkoc.
- Android/device info: read the app's version metadata from the package manager instead of hidden APIs so Android 15+ onboarding and device info no longer fail to compile or report placeholder values. (#58126) Thanks @L3ER0Y.


---

## 💡 深度点评

这是针对 openclaw 2026.3.31 版本的深度点评：

### 核心亮点

*   **后台任务控制平面的大一统**：本版本将 ACP（代理协作协议）、子代理、Cron 以及后台 CLI 执行完全统一到了基于 SQLite 的共享控制平面下。这一变更不仅提供了任务审计、状态可见性和丢失运行恢复的能力，更重要的是通过 `openclaw flows` 引入了线性任务流控制。这标志着 openclaw 从零散的任务执行转向了有状态、可追踪的工程化调度。
*   **安全执行边界的全面收紧**：安全策略在这一版本中变得更加“激进”。插件和技能安装中的 `critical` 风险项现在默认“闭合失败（fail closed）”，强制要求 `--dangerously-force-unsafe-install` 才能继续。同时，在宿主执行环境（Host Exec）中封锁了代理、TLS 和 Docker 端点的环境变量覆盖，有效切断了通过 request-scoped 命令重定向流量或篡改信任根的攻击路径。
*   **原生交互与审批链路的优化**：Slack 原生审批路由的加入是一个重要的体验改进，审批操作可以停留在即时通讯工具内，无需跳转 Web UI 或终端。此外，针对 Matrix 的流式输出支持以及对 QQ Bot 的原生集成，进一步增强了 openclaw 在主流社交/协作渠道作为生产力工具的连贯性。

### 值得注意的修复

*   **模型失效切换与异常处理改进**：修复了 Anthropic `api_error` 的瞬态错误识别，使其能正确触发重试而非直接崩溃；优化了 OpenAI Responses 路径下的 MCP 工具 Schema 标准化，解决了复杂联合类型（Union Types）在工具注册时的报错问题。
*   **系统稳定性与并发控制**：解决了代理压缩（compaction）重试导致的双重解析竞争问题，以及移动端（Android 15+ 和 iOS Xcode 26.4 严格并发检查）的兼容性构建故障，确保了在现代操作系统环境下的运行稳定性。
*   **配置隔离与清理**：修复了 `openclaw doctor` 误将插件注入的频道默认值持久化到主配置的问题，避免了后续升级时出现的配置校验失效。

### 个人评价

2026.3.31 版本是一个从“功能堆砌”转向“架构加固”的典型版本。通过重构后台任务系统和收紧插件安装权限，openclaw 正在构建更深的技术护城河，尤其是在生产环境所需的任务确定性和运行安全性方面。虽然这些 Breaking Changes 提升了开发者和运维的操作门槛，但对于构建长期可靠的 AI 自主代理体系是必经之路。整体方向上，openclaw 正在变得更像是一个 AI 原生的操作系统内核，而不仅仅是一个 CLI 工具。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-01 08:02:08*
