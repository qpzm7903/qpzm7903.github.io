---
title: "🔧 Openclaw 更新日报 2026-04-16"
date: 2026-04-16T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.4.15-beta.1

**发布日期**: 2026-04-16  
**⚠️ 新版本发布**

## Changes

- Control UI/Overview: add a Model Auth status card showing OAuth token health and provider rate-limit pressure at a glance, with attention callouts when OAuth tokens are expiring or expired. Backed by a new `models.authStatus` gateway method that strips credentials and caches for 60s. (#66211) Thanks @omarshahine.
- Memory/LanceDB: add cloud storage support to `memory-lancedb` so durable memory indexes can run on remote object storage instead of local disk only. (#63502) Thanks @rugvedS07.
- GitHub Copilot/memory search: add a GitHub Copilot embedding provider for memory search, and expose a dedicated Copilot embedding host helper so plugins can reuse the transport while honoring remote overrides, token refresh, and safer payload validation. (#61718) Thanks @feiskyer and @vincentkoc.
- Agents/local models: add experimental `agents.defaults.experimental.localModelLean: true` to drop heavyweight default tools like `browser`, `cron`, and `message`, reducing prompt size for weaker local-model setups without changing the normal path. (#66495) Thanks @ImLukeF.
- Packaging/plugins: localize bundled plugin runtime deps to their owning extensions, trim the published docs payload, and tighten install/package-manager guardrails so published builds stay leaner and core stops carrying extension-owned runtime baggage. (#67099) Thanks @vincentkoc.

## Fixes

- Security/approvals: redact secrets in exec approval prompts so inline approval review can no longer leak credential material in rendered prompt content. (#61077, #64790)
- CLI/configure: re-read the persisted config hash after writes so config updates stop failing with stale-hash races. (#64188, #66528)
- CLI/update: prune stale packaged `dist` chunks after npm upgrades and keep downgrade/verify inventory checks compat-safe so global upgrades stop failing on stale chunk imports. (#66959) Thanks @obviyus.
- Onboarding/CLI: fix channel-selection crashes on globally installed CLI setups during onboarding. (#66736)
- Video generation/live tests: bound provider polling for live video smoke, default to the fast non-FAL text-to-video path, and use a one-second lobster prompt so release validation no longer waits indefinitely on slow provider queues.
- Memory-core/QMD `memory_get`: reject reads of arbitrary workspace markdown paths and only allow canonical memory files (`MEMORY.md`, `memory.md`, `DREAMS.md`, `dreams.md`, `memory/**`) plus exact paths of active indexed QMD workspace documents, so the QMD memory backend can no longer be used as a generic workspace-file read shim that bypasses `read` tool-policy denials. (#66026) Thanks @eleqtrizit.
- Cron/agents: forward embedded-run tool policy and internal event params into the attempt layer so `--tools` allowlists, cron-owned message-tool suppression, explicit message targeting, and command-path internal events all take effect at runtime again. (#62675) Thanks @hexsprite.
- Setup/providers: guard preferred-provider lookup during setup so malformed plugin metadata with a missing provider id no longer crashes the wizard with `Cannot read properties of undefined (reading 'trim')`. (#66649) Thanks @Tianworld.
- Matrix/security: normalize sandboxed profile avatar params, preserve `mxc://` avatar URLs, and surface gmail watcher stop failures during reload. (#64701) Thanks @slepybear.
- Telegram/documents: drop leaked binary caption bytes from inbound Telegram text handling so document uploads like `.mobi` or `.epub` no longer explode prompt token counts. (#66663) Thanks @joelnishanth.
- Gateway/auth: resolve the active gateway bearer per-request on the HTTP server and the HTTP upgrade handler via `getResolvedAuth()`, mirroring the WebSocket path, so a secret rotated through `secrets.reload` or config hot-reload stops authenticating on `/v1/*`, `/tools/invoke`, plugin HTTP routes, and the canvas upgrade path immediately instead of remaining valid on HTTP until gateway restart. (#66651) Thanks @mmaps.
- Agents/compaction: cap the compaction reserve-token floor to the model context window so small-context local models (e.g. Ollama with 16K tokens) no longer trigger context-overflow errors or infinite compaction loops on every prompt. (#65671) Thanks @openperf.


---

## 💡 深度点评

openclaw 2026.4.15-beta.1 版本发布，这一版在内存架构、本地模型适配以及安全性上进行了深度优化。以下是本次更新的技术点评：

### 核心亮点

*   **Memory/LanceDB 远程存储支持**：`memory-lancedb` 插件新增云端对象存储支持。这意味着持久化内存索引不再受限于本地磁盘，为分布式部署和多机协同提供了基础架构支撑，解决了大规模 Agent 内存冗余与同步的痛点。
*   **GitHub Copilot Embedding 集成**：新增 GitHub Copilot 作为内存搜索的嵌入提供者，并暴露了专用 host helper。开发者可以利用 Copilot 现成的向量化能力，同时复用其令牌刷新和安全校验机制，显著降低了插件开发中向量计算的门槛。
*   **本地模型轻量化模式 (`localModelLean`)**：针对弱算力或小上下文本地模型，新增实验性配置。通过剔除 `browser`、`cron` 等重型默认工具，有效精简 Prompt 规模，防止因工具描述过长导致的小模型推理性能下降或上下文溢出。

### 值得注意的修复

*   **安全性与权限兜底**：修复了多个高危逻辑漏洞，包括 `memory_get` 限制访问非规范 Markdown 路径，防止其被当作通用文件读取工具；同时在执行审批环节自动脱敏 Secrets，并强化了 `fs-safe` 助手对符号链接（Symlink）劫持的防御能力。
*   **上下文压缩循环优化**：修正了小上下文模型（如 16K 的 Ollama）在触发 Compaction 时的逻辑，设定了基于模型窗口的保留令牌下限，彻底解决了在此类场景下极易出现的无限压缩循环或上下文溢出报错。
*   **复杂消息链路稳定性**：针对 BlueBubbles 引入了基于文件 GUID 的持久化去重，解决了重启后的消息重喷问题；Telegram 链路则通过过滤二进制字节，避免了 `.mobi` 等文件导致 Prompt Token 计数异常爆表。

### 个人评价

2026.4.15-beta.1 是一个以「工业级稳健性」为导向的迭代版本。它不仅通过 LanceDB 云端化和插件依赖局部化完成了系统架构的减负，更在细节上对本地小模型的生存空间进行了精准调优。特别是针对内存访问安全和 Secrets 脱敏的加固，标志着 openclaw 正在从一个极客工具向生产力套件加速转型，其跨平台通信（Telegram/Slack/BlueBubbles）的防御性编程逻辑也日益成熟。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-04-16 08:02:19*
