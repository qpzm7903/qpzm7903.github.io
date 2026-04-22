---
title: "🔧 Codex 更新日报 2026-04-22"
date: 2026-04-22T10:00:00+08:00
draft: false
tags: ["codex", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Codex 更新 rust-v0.122.0

**发布日期**: 2026-04-22  
**⚠️ 新版本发布**

## New Features

- Standalone installs are more self-contained, and `codex app` now opens or installs Desktop correctly on Windows and Intel Macs (#17022, #18500).
- The TUI can open `/side` conversations for quick side questions, and queued input now supports slash commands and `!` shell prompts while work is running (#18190, #18542).
- Plan Mode can start implementation in a fresh context, with context-usage shown before deciding whether to carry the planning thread forward (#17499, #18573).
- Plugin workflows now include tabbed browsing, inline enable/disable toggles, marketplace removal, and remote, cross-repo, or local marketplace sources (#18222, #18395, #17752, #17751, #17277, #18017, #18246).
- Filesystem permissions now support deny-read glob policies, managed deny-read requirements, platform sandbox enforcement, and isolated `codex exec` runs that ignore user config or rules (#15979, #17740, #18096, #18646).
- Tool discovery and image generation are now enabled by default, with higher-detail image handling and original-detail metadata support for MCP and `js_repl` image outputs (#17854, #17153, #17714, #18386).

## Bug Fixes

- App-server approvals, user-input prompts, and MCP elicitations now disappear from the TUI when another client resolves them, instead of leaving stale prompts behind (#15134).
- Remote-control startup now tolerates missing ChatGPT auth, and MCP startup cancellation works again through app-server sessions (#18117, #18078).
- Resumed and forked app-server threads now replay token usage immediately so context/status UI starts with the restored state (#18023).
- Security-sensitive flows were tightened: logout revokes managed ChatGPT tokens, project hooks and exec policies require trusted workspaces, and Windows sandbox setup avoids broad user-profile and SSH-root grants (#17825, #14718, #18443, #18493).
- Sandboxed `apply_patch` writes work correctly with split filesystem policies, and file watchers now notice files created after watching begins (#18296, #18492).
- Several TUI rough edges were fixed, including fatal skills-list failures, invalid resume hints, duplicate context statusline entries, `/model` menu loops, redundant memory notices, and terminal title quoting in iTerm2 (#18061, #18059, #18054, #18154, #18580, #18261).

## Documentation

- Added a security-boundaries reference to `SECURITY.md` for sandboxing, approvals, and network controls (#17848, #18004).
- Documented custom MCP server approval defaults and exec-server stdin behavior (#17843, #18086).
- Updated app-server docs for plugin API changes, marketplace removal, resume/fork token-usage replay, and warning notifications (#17277, #17751, #18023, #18298).
- Added a short guide for the responses API proxy (#18604).

## Chores

- Split plugin and marketplace code into `codex-core-plugins`, moved more connector code into `connectors`, and continued breaking up the large core session/turn modules (#18070, #18158, #18200, #18206, #18244, #18249).
- Refactored config loading and `AGENTS.md` discovery behind narrower filesystem and manager abstractions (#18209, #18035).
- Stabilized Bazel and CI with flake fixes, native Rust test sharding, scoped repository caches, stronger Windows clippy coverage, and updated `rules_rs`/LLVM pins (#17791, #18082, #18366, #18350, #18397).
- Added core CODEOWNERS and a smaller development build profile (#18362, #18612).
- Removed the stale core `models.json` and updated release preparation to refresh the active model catalog (#18585).

## Changelog

- #17958 Support remote compaction for Azure responses providers @ivanmurashko
- #17848 [docs] Add security boundaries reference in SECURITY.md @evawong-oai
- #17990 Auto install start-codex-exec.sh dependencies @pakrym-oai
- #17892 Migrate archive/unarchive to local ThreadStore @wiltzius-openai
- #17989 [codex] Restore remote exec-server filesystem tests @starr-openai
- #15134 Dismiss stale app-server requests after remote resolution @ebrevdo
- #18002 Re-enable it @jif-oai
- #17885 feat: Support alternate marketplace manifests and local string @xl-openai
- #18003 [docs] Revert extra changes from PR 17848 @evawong-oai
- #17714 Support original-detail metadata on MCP image outputs @fjord-oai
- #17022 Significantly improve standalone installer @efrazer-oai
- #17853 [mcp] Add dummy tools for previously called but currently missing tools. @mzeng-openai


---

## 💡 深度点评

### 核心亮点

*   **Plan Mode 与上下文精细化管理**：Plan Mode 现在支持在全新的上下文中启动任务实现。更重要的是，在决定是否继承规划线程前，系统会预先显示上下文使用量，这为大模型长对话产生的“上下文膨胀”和成本控制提供了有效的干预手段。
*   **深度的文件系统安全沙箱**：引入了 `deny-read` glob 策略和平台沙箱强制执行机制。配合 `codex exec` 支持忽略用户配置或规则的隔离运行模式，使得 Codex 在处理敏感代码库或不可信脚本时的安全边界更加清晰。
*   **TUI 交互效率提升**：终端界面新增 `/side` 会话功能，允许用户在不中断主线任务的情况下进行侧边提问。同时，支持在工作运行期间排队输入 slash 命令和 `!` shell 提示符，极大增强了任务并行处理的感官体验。

### 值得注意的修复

*   **过时 UI 状态清理**：解决了 App-server 审批和 MCP 引导提示在被其他客户端解决后仍残留在 TUI 上的问题，消除了 stale prompts 带来的误操作风险。
*   **Windows 沙箱权限收紧**：修正了 Windows 环境下沙箱权限过大的问题，避免了对 `USERPROFILE` 和 SSH 根目录的宽泛授权，进一步符合最小权限原则。
*   **状态恢复实时性**：修复了 thread 在恢复或分叉（fork）后 token 使用量统计滞后的 Bug，现在状态 UI 能立即回放并反映准确的资源消耗。

### 个人评价

Codex v0.122.0 是一个从“功能堆叠”向“工程化收敛”转变的关键版本。通过引入更严格的沙箱策略和上下文预显，它解决了 AI 开发工具进入企业级环境时最核心的安全与成本痛点。同时，插件系统的模块化重构（如 `codex-core-plugins` 的拆分）显示出底层架构正在为更大规模的生态接入做准备。整体而言，这是一个提升了生产环境交付信心的高质量更新。

---

**数据来源**: [GitHub openai/codex](https://github.com/openai/codex)

*Generated by OpenClaw at 2026-04-22 13:11:53*
