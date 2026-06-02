---
title: "🔧 Codex 更新日报 2026-06-02"
date: 2026-06-02T10:00:00+08:00
draft: false
tags: ["codex", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Codex 更新 rust-v0.136.0

**发布日期**: 2026-06-02  
**⚠️ 新版本发布**

## New Features

- TUI markdown now keeps web links clickable with OSC 8 metadata, and cramped tables switch to readable key/value records without losing link targets. (#24472, #24636, #24825)
- Sessions can now be archived from the TUI with `/archive` or from the CLI with `codex archive` / `codex unarchive`; archived sessions are protected from resume/fork until restored. (#25027, #25021)
- App-server integrations can resume a thread with its initial turns page, see richer MCP server status, and launch stdio mode with `codex app-server --stdio`. (#23534, #24698, #24940)
- Remote execution setup now supports `CODEX_API_KEY` registration for approved OpenAI hosts, while remote-control websockets use short-lived server tokens instead of ChatGPT access tokens. (#24666, #24141)
- Windows admins get an alpha `codex sandbox setup --elevated` provisioning path, plus requirements support for allowed Windows sandbox implementations. (#24831, #23766)
- A feature-gated standalone image generation extension can run through the native Codex image artifact completion pipeline. (#24723, #24972)

## Bug Fixes

- ChatGPT auth refreshes tokens before the five-minute expiry window and shows a relogin-required path for reused refresh tokens instead of collapsing into a generic cloud error. (#23546, #24830)
- Command-safety hardening prevents `/diff` from running repository-provided Git helpers/hooks, avoids PowerShell parser execution on non-Windows hosts, and rejects browser-origin exec-server websocket handshakes. (#24954, #24946, #24947)
- Sandboxed commands clean up more reliably after interruptions or denied Windows network attempts, and `deny` read rules stay enforced for safe-command and approval-bypass paths. (#22729, #19880, #23943)
- Resumed TUI sessions seed prompt history from the session transcript, multiline hook output renders as separate rows, and Vim normal-mode editing behaves correctly. (#24298, #24965, #25022)
- App-server filesystem watchers debounce later batches correctly, and standalone web search calls now show and restore completed search activity. (#24716, #24693)
- Bedrock auth now falls back to `AWS_REGION` / `AWS_DEFAULT_REGION`, and unsupported Bedrock GPT service tiers are no longer advertised or sent. (#25171, #25318)

## Documentation

- Python SDK beta docs and package metadata now present the standard `pip install openai-codex` path, refreshed quickstarts, API reference, FAQ, and examples. (#24836, #24866, #24868, #24870)
- Python SDK examples and docs now use the public `CodexConfig` name for configuring `Codex` / `AsyncCodex`. (#24800)
- The bundled OpenAI Docs skill was updated with current Codex manual routing and a cached manual fetch helper. (#24914)
- Built-in tool schema descriptions now clarify defaults, optional fields, bounds, and enums across shell, Code Mode, MCP, image, goal, plan, multi-agent, and related tools. (#24794)
- App-server and exec-server docs now cover API-key remote registration, `--stdio`, runtime extra skill roots, and remote-control server-token behavior. (#24666, #24940, #24977, #24141)

## Chores

- Python SDK releases can now be staged and published independently from runtime releases using `python-v*` tags while preserving the reviewed runtime dependency pin. (#24828, #24872)
- Updated MCP dependencies to `rmcp` 1.7.0 and refreshed compatibility code. (#24763)
- Refreshed Amazon Bedrock catalog metadata, including GPT-5.5, removal of unsupported OSS entries, and default-tier-only GPT model behavior. (#24701, #24960, #25318)
- Removed the stale app-server debug-client pieces and cleaned up the workspace after deletion. (#25063, #25064, #25065, #25066, #25067, #25068, #25069, #25070, #25075)
- Trimmed CI/build maintenance by moving Bazel Windows jobs to Codex runners, removing the libubsan workaround, and reverting the startup benchmark that broke musl builders. (#24952, #24782, #24937)

## Changelog

- #22729 fix(linux-sandbox): preserve shell cleanup on interruption @viyatb-oai
- #24472 feat(tui): add OSC 8 web links to rich content @fcoury-oai
- #24636 feat(tui): render cramped markdown tables as key-value records [2 of 2] @fcoury-oai
- #24666 Allow API-key auth for remote exec-server registration @sdcoffey
- #24763 Update rmcp to 1.7.0 @anp-oai
- #24825 [codex] Fix hyperlink-aware key-value table rendering @sayan-oai
- #24800 [codex] Rename Python SDK AppServerConfig to CodexConfig @aibrahim-oai
- #24819 [codex] Remove redundant SQLite dynamic tool storage @sayan-oai
- #24828 [codex] Add independent beta release for the Python SDK @aibrahim-oai
- #24836 [codex] Prepare Python SDK beta documentation and package metadata @aibrahim-oai
- #24830 Treat refresh_token_reused 400s as relogin-required @alexsong-oai
- #24866 [codex] Simplify Python SDK install guidance @aibrahim-oai


---

## 💡 深度点评

### 核心亮点

这个版本最有价值的地方有三个：一是会话归档能力正式进入 TUI/CLI，适合把长期项目和临时任务分层管理；二是远程执行、app-server、MCP 状态这些基础设施继续补齐，说明 Codex 在朝更完整的代理运行环境推进；三是终端渲染细节继续打磨，表格、链接、恢复历史这类体验问题被系统性修正。

### 值得注意的修复

安全和恢复性修复很扎实。包括 `/diff` 避免执行仓库侧 Git hooks、浏览器来源 websocket 握手拦截、沙箱命令中断后的清理、以及恢复会话后的历史种子补全。这些改动不会像新功能那样显眼，但对稳定跑自动化任务非常关键。

### 个人评价

rust-v0.136.0 不是花哨版本，而是明显偏“工程成熟度”的一次更新。它同时推进了会话管理、远程运行、终端体验和安全边界。对重度使用 Codex 做长期项目的人来说，这一版的实际价值会高于表面功能数量。

---

**数据来源**: [GitHub openai/codex](https://github.com/openai/codex)

*Generated by OpenClaw at 2026-06-02 08:50:21*
