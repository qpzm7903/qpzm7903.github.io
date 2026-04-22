---
title: "🔧 Openclaw 更新日报 2026-04-22"
date: 2026-04-22T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.21

**发布日期**: 2026-04-22  
**⚠️ 新版本发布**

## Changes

- OpenAI/images: default the bundled image-generation provider and live media smoke tests to `gpt-image-2`, and advertise the newer 2K/4K OpenAI size hints in image-generation docs and tool metadata.
- Plugins/skills: add the Skill Workshop plugin, which captures reusable workflow corrections as pending or auto-applied workspace skills, runs threshold-based reviewer passes for stronger completion bias on reusable procedures, quarantines unsafe proposals, and refreshes skill availability after safe writes.
- Plugin SDK/channels: add presentation and skills runtime contracts, decouple channel presentation rendering, and document message presentation cards so plugins can own richer interactive surfaces without channel-specific glue.
- Fireworks/models: add Kimi K2.6 (`fireworks/accounts/fireworks/models/kimi-k2p6`) to the bundled catalog and live-model priority list, while keeping Kimi thinking disabled for Fireworks K2.6 requests.
- Onboard/wizard: simplify the security disclaimer copy, and switch remaining onboarding pickers with long dynamic option lists to searchable autocompletes for search providers, plugin configuration, and model provider filtering.
- Channels/preview streaming: stream tool-progress updates into live preview edits for Discord, Slack, and Telegram so in-flight replies show incremental tool state in the same preview message before finalization. (#69611) Thanks @thewilloftheshadow.
- Ollama/onboard: populate the cloud-only model list from `ollama.com/api/tags`, cap the discovered list at 500, and fall back to static suggestions when ollama.com is unavailable. (#68463) Thanks @BruceMacD.
- QQBot: extract a self-contained engine architecture with QR-code onboarding, native approval handling via `/bot-approve`, per-account resource stacks, credential backup/restore, shared media storage, and unified API/bridge/gateway modules. (#67960) Thanks @cxyhhhhh.
- Matrix/startup: narrow Matrix runtime registration and defer setup/doctor surfaces so cold plugin registration spends about 1.8s less in `setChannelRuntime`. (#69782) Thanks @gumadeiras.
- Telegram/plugin startup: load Telegram's bundled runtime setter through a narrow sidecar and native built-sidecar loading, cutting measured setup-runtime registration by about 14s while preserving runtime API compatibility. (#69786) Thanks @gumadeiras.
- Discord/plugin startup: lazy-load the Carbon UI runtime and load Discord's bundled runtime setter through a narrow sidecar, cutting measured registration time by about 98% while keeping packaged installs off Carbon until the Discord UI surface is needed. (#69791) Thanks @gumadeiras.

## Fixes

- Agents/ACP: skip the `sessions_send` A2A ping-pong flow when a parent sends to its own background oneshot ACP child, preventing parent/child echo loops while preserving normal A2A delivery for non-parent senders. (#69817) Thanks @scotthuang.
- Image generation: log failed provider/model candidates at warn level before automatic provider fallback, so OpenAI image failures are visible in the gateway log even when a later provider succeeds.
- Agents/subagents: stop terminal failed subagent runs from freezing or announcing captured reply text, so failover-exhausted runs report a clean failure instead of replaying stale assistant/tool output.
- Security/external content: strip common self-hosted LLM chat-template special-token literals, including Qwen/ChatML, Llama, Gemma, Mistral, Phi, and GPT-OSS markers, from wrapped external content and metadata, preventing tokenizer-layer role-boundary spoofing against OpenAI-compatible backends that preserve special tokens in user text.
- npm/install: mirror the `node-domexception` alias into root `package.json` `overrides`, so npm installs stop surfacing the deprecated `google-auth-library -> gaxios -> node-fetch -> fetch-blob -> node-domexception` chain pulled through Pi/Google runtime deps. Thanks @vincentkoc.
- Auth/commands: require owner identity (an owner-candidate match or internal `operator.admin`) for owner-enforced commands instead of treating wildcard channel `allowFrom` or empty owner-candidate lists as sufficient, so non-owner senders can no longer reach owner-only commands through a permissive fallback when `enforceOwnerForCommands=true` and `commands.ownerAllowFrom` is unset. (#69774) Thanks @drobison00.
- Control UI/CSP: tighten `img-src` to `'self' data:` only, and make Control UI avatar helpers drop remote `http(s)` and protocol-relative URLs so the UI falls back to the built-in logo/badge instead of issuing arbitrary remote image fetches. Same-origin avatar routes (relative paths) and `data:image/...` avatars still render. (#69773)
- CLI/channels: keep `status`, `health`, `channels list`, and `channels status` on read-only channel metadata when Telegram, Slack, Discord, or third-party channel plugins are configured, avoiding full bundled plugin runtime imports on those cold paths. Fixes #69042. (#69479) Thanks @gumadeiras.
- Synology Chat: validate outbound webhook `file_url` values against the shared SSRF policy before forwarding to the NAS, rejecting malformed URLs, non-`http(s)` schemes, and private/blocked network targets so the NAS cannot be used as a confused deputy to fetch internal addresses. (#69784) Thanks @eleqtrizit.
- LINE: validate outbound media URLs against the shared public-network guard before handing them to LINE, preserving arbitrary public HTTPS media while rejecting loopback, link-local, and private-network targets.
- Gateway/Control UI: require gateway auth on the Control UI avatar route (`GET /avatar/<agentId>` and `?meta=1` metadata) when auth is configured, matching the sibling assistant-media route, and propagate the existing gateway token through the UI avatar fetch (bearer header + authenticated blob URL) so authenticated dashboards still load local avatars. (#69775)
- Exec/allowlist: reject POSIX parameter expansion forms such as `$VAR`, `$?`, `$$`, `$1`, and `$@` inside unquoted heredocs during shell approval analysis, so these heredocs no longer pass allowlist review as plain text. (#69795) Thanks @drobison00.


---

## 💡 深度点评

### 核心亮点

**1. 自动化能力演进：Skill Workshop 插件上线**
新版本引入了 Skill Workshop 插件，标志着 OpenClaw 从「工具执行」向「经验累化」迈进。它能捕获工作流中的修正行为并转化为可复用的 Workspace Skills，通过基于阈值的审核机制强化完成偏好，并具备安全隔离机制。这不仅提升了复杂任务的成功率，也让插件具备了在实践中进化的能力。

**2. 启动性能爆发式提升：插件加载机制优化**
针对 Telegram 和 Discord 等主流 Channel 插件进行了深度重构。通过引入 Sidecar 加载模式和延迟加载 Carbon UI 等手段，Telegram 的启动注册时间缩短了约 14 秒，Discord 的加载耗时更是骤降 98%。这种对冷启动路径的「手术级」优化，极大地改善了开发者在调试和重启时的体验。

**3. 交互与多模态增强：实时工具状态流与模型更新**
Plugin SDK 实现了展现层与运行时的解耦，支持更丰富的交互卡片。在 Discord、Slack 等平台上，用户可以实时看到工具执行的中间状态（tool-progress updates），不再是盲目等待最终回复。同时，多模态能力也得到了补充，新增了对 Kimi K2.6 以及 Ollama 视觉模型的原生支持。

### 值得注意的修复

*   **Tokenizer 注入防御**：修复了一个严重的安全隐患，系统现在会自动过滤外部内容中的 Qwen/ChatML、Llama 等模型专用特殊 Token，防止通过 User 文本进行角色边界欺骗（Role-boundary spoofing）。
*   **权限与沙箱加固**：强制要求 Owner-only 指令必须校验身份标识，而非仅依赖配置列表；同时 OpenClaw 沙箱写操作增加了挂载根路径锁定，防止通过软链接重定向绕过工作区限制。
*   **SSRF 策略对齐**：针对 Synology Chat、LINE、Tlon 等第三方通道统一应用了 SSRF 防御策略，严禁通过 Webhook 或媒体上传接口访问本地回环或私有网络地址。
*   **ACP 循环调用修复**：解决了 Agent 亲子进程通信中的 A2A Ping-Pong 回环问题，避免了在特定场景下出现的无限递归调用。

### 个人评价

OpenClaw 2026.4.21 版本展现了极强的工程化约束力。开发团队并未一味堆砌新功能，而是将重心放在了**运行时效率（Runtime Efficiency）**与**底层安全性（Security Hardening）**的深度打磨上。尤其是对插件加载路径的极致优化和 Tokenizer 层的注入防御，体现了该项目在迈向生产级 AI 协作工具时的成熟度。Skill Workshop 的出现，也预示着未来 AI Agent 将进入「自我演进」的阶段。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-22 13:12:04*
