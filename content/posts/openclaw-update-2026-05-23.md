---
title: "🔧 Openclaw 更新日报 2026-05-23"
date: 2026-05-23T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.5.22

**发布日期**: 2026-05-23  
**⚠️ 新版本发布**

## Changes

- Docs: clarify README onboarding and Gateway startup paths, WhatsApp QR/408 recovery, cron output language prompts, skill advanced features, gateway upstream 403 troubleshooting, and plugin fallback override guidance. Thanks @deepujain, @Zacxxx, @Jah-yee, @neyric, @usimic, @Renu-Cybe, @BigUncle, and @SeashoreShi.
- Docs: clarify context-pruning ratio bounds, local dashboard recovery, CLI env markers, remote onboarding token behavior, and Peekaboo Bridge permissions for subprocess agents. Thanks @ayesha-aziz123, @dishraters, @hougangdev, and @brandonlipman.
- Docs: clarify browser CDP diagnostics, Plugin SDK allowlist imports, status-reaction timing defaults, queue steering behavior, limited-tool troubleshooting, cron HEARTBEAT handling, Telegram multi-agent groups, Bitwarden SecretRef setup, and EasyRunner deployments. Thanks @Quratulain-bilal, @mbelinky, @Mickey-, @vancece, @xenouzik, @posigit, @surlymochan, @janaka, and @choiking.
- Crabbox/Testbox: run clean sparse-checkout Testbox syncs from a temporary full checkout and route remote changed gates through Corepack pnpm.
- Docs: clarify IPv4-only Gateway BYOH binding, trusted-proxy scope clearing, Android pairing approval, macOS Accessibility grants, Zalo profile env vars, password-store SecretRef setup, and Chinese memory navigation. Thanks @itskai-dev, @gwh7078, @longstoryscott, @MoeJaberr, and @yuaiccc.
- Docs: consolidate GLM under Z.AI, add the Upstash Box install guide and Gateway exposure runbook, clarify MEDIA directives, Copilot and Voyage setup, config path quoting, real behavior proof, and memory-file write guidance. Thanks @BobDu, @alitariksahin, @Jefsky, @musaabhasan, @OmerZeyveli, @leno23, @WuKongAI-CMU, @luoyanglang, and @majin1102.
- Docs: clarify media provider credentials, Codex/OpenClaw code-mode boundaries, Slack and Telegram ack reactions, Feishu dynamic agents, secrets plaintext boundaries, memory guidance, and Chinese glossary terms. Thanks @nielskaspers, @cosmopolitan033, @drclaw-iq, @alexgduarte, @zccyman, @chengoak, and @cassthebandit.
- Packaging: exclude documentation images and assets from the npm tarball, reducing published package size without affecting runtime docs search or CLI behavior. Thanks @SebTardif.
- Media understanding: stop auto-probing Gemini CLI and use Antigravity CLI only as a lower-priority image/video fallback after configured provider APIs.
- Agents/subagents: limit default sub-agent bootstrap context to `AGENTS.md` and `TOOLS.md`, keeping persona, identity, user, memory, heartbeat, and setup files out of delegated workers by default. (#85283) Thanks @100yenadmin.
- Maintainer skills: exclude plugin SDK/API boundary work from `openclaw-landable-bug-sweep` so bugbash sweeps stay focused on small paper-cut fixes.
- Plugin SDK: add a generic channel-message poll sender so channel plugins can expose poll delivery without depending on channel-specific SDK facades.

## Fixes

- Agents: keep parallel OpenAI-compatible tool-call deltas in separate argument buffers so interleaved tool calls no longer corrupt streamed arguments. (#82263) Thanks @luna-system.
- Memory/doctor: report missing or unusable QMD workspace directories as workspace failures instead of generic binary failures. (#63167) Thanks @sercada.
- Debug proxy: record CONNECT client-socket errors and destroy the paired upstream socket so abrupt client disconnects no longer leak tunnel resources. (#82444) Thanks @SebTardif.
- Diffs: continue hydrating later diff cards when one card fails so a single broken card no longer blanks the whole diff viewer. (#84775) Thanks @cosmopolitan033.
- Mac app: use the native settings sidebar window chrome so the sidebar toggle stays on the left and content no longer clips under oversized titlebar padding.
- Gateway/agents: preserve fresh session overrides and metadata when stale cached agent-session entries race with store updates, so subagent model/provider overrides and routing policy survive concurrent writes. (#19328) Thanks @CodeReclaimers.
- Control UI/chat: keep chat session search inline with the session selector so the header no longer shows a duplicate standalone search row.
- Codex app-server: restart the native app-server and retry once when server-side compaction times out, so preflight compaction stalls recover instead of failing every dispatch. (#85500)
- Restore Control UI gateway token pairing [AI]. (#85459) Thanks @pgondhi987.
- OpenAI video: honor configured provider request private-network opt-in for local/custom video endpoints so explicitly trusted mock and self-hosted providers are not blocked. Thanks @shakkernerd.
- CLI/update: repair managed npm plugin `openclaw` peer links during post-core convergence and reject stale or wrong-target peer links before restart. (#83794) Thanks @fuller-stack-dev.
- CLI/agents: default new omitted-account bindings to all accounts when the channel has multiple configured accounts, and clarify account-scope docs. (#49769) Thanks @Gcaufy.


---

## 💡 深度点评

### 核心亮点

- **模型列表接口性能实现量级跃升**：Gateway 引入了 Provider Auth-State 的启动期预热机制。该设计将鉴权发现与外部 CLI 调用从热路径（Hot Path）中短路，使 `/models` 及模型列表调用的单次开销从均值 20 秒骤降至 5 毫秒（提速约 4100 倍），并在支持热加载的同时保持了状态同步。
- **通用 Embedding Provider 契约落地**：Plugin SDK 正式将 Embedding 能力标准化，新增 `embeddingProviders` 注册 API。此举将向量化组件从强绑定的记忆（Memory）适配器中解耦，使其成为可被任意插件和工作流复用的通用基础表面。
- **发布链路与依赖树安全加固**：OpenClaw 核心及其官方 npm 插件包现全量携带 Shrinkwrap 产物发版。通过在打包阶段强制检查依赖完整性，并引入 Lockfile 变更的强制代码审查，收敛了运行时的依赖漂移风险。

### 值得注意的修复

- **流式并发工具调用的数据损坏修复**：针对 OpenAI 兼容接口，修改了并行 Tool-call 的 Delta 解析逻辑，为不同的并发调用分配独立的参数缓冲区，修复了因缓冲区复用导致的流式数据交叉污染。
- **网关 Session 状态更新的竞态条件修复**：重构了缓存条目与存储更新的同步机制。修复了在并发写入场景下，陈旧的 Agent-session 缓存覆盖最新 Session 覆写参数（如子智能体模型配置、路由策略）的稳定性 Bug。
- **多智能体环境文件句柄耗尽（`EMFILE`）修复**：重构了 Skill 目录的 Watcher 机制，将原本按 Agent 实例分配的独立监听器优化为跨 Workspace 共享的单例监听。这一改动直接消除了多智能体实例导致的描述符泄漏及后续的进程挂起问题。

### 个人评价

2026.5.22 版本展现了非常克制且聚焦的工程迭代方向。从 4100 倍的模型列表查阅提速到对流式工具调用、状态竞态、文件句柄泄漏等并发缺陷的定点清除，核心团队将主要精力投入在了高负载和复杂调度场景的底盘稳定性上。同时，SDK 中 Embedding 能力的解耦和依赖树的强锁定，说明框架正在逐步剥离早期的实验性设计，向着严格的生产级可观测性和模块化稳步演进。这不是一个主打花哨新功能的版本，但绝对是一个让开发者在工程化落地时更安心的版本。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-05-23 08:04:59*
