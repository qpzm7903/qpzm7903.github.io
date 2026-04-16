---
title: "🔧 Codex 更新日报 2026-04-16"
date: 2026-04-16T10:00:00+08:00
draft: false
tags: ["codex", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Codex 更新 rust-v0.121.0

**发布日期**: 2026-04-16  
**⚠️ 新版本发布**

## New Features

- Added `codex marketplace add` and app-server support for installing plugin marketplaces from GitHub, git URLs, local directories, and direct `marketplace.json` URLs (#17087, #17717, #17756).
- Added TUI prompt history improvements, including `Ctrl+R` reverse search and local recall for accepted slash commands (#17550, #17336).
- Added TUI and app-server controls for memory mode, memory reset/deletion, and memory-extension cleanup (#17632, #17626, #17913, #17937, #17844).
- Expanded MCP/plugin support with MCP Apps tool calls, namespaced MCP registration, parallel-call opt-in, and sandbox-state metadata for MCP servers (#17364, #17404, #17667, #17763).
- Added realtime and app-server APIs for output modality, transcript completion events, raw turn item injection, and symlink-aware filesystem metadata (#17701, #17703, #17719).
- Added a secure devcontainer profile with bubblewrap support, plus macOS sandbox allowlists for Unix sockets (#10431, #17547, #17654).

## Bug Fixes

- Fixed macOS sandbox/proxy handling for private DNS and removed the `danger-full-access` denylist-only network mode (#17370, #17732).
- Fixed Windows cwd/session matching so `resume --last` and `thread/list` work when paths use verbatim prefixes (#17414).
- Fixed rate-limit/account handling for `prolite` plans and made unknown WHAM plan values decodable (#17419).
- Made Guardian timeouts distinct from policy denials, with timeout-specific guidance and visible TUI history entries (#17381, #17486, #17521, #17557).
- Stabilized app-server behavior by avoiding premature thread unloads, tolerating failed trust persistence on startup, and skipping broken symlinks in `fs/readDirectory` (#17398, #17595, #17907).
- Fixed MCP/tool-call edge cases including flattened deferred tool names, elicitation timeout accounting, and empty namespace descriptions (#17556, #17566, #17946).

## Documentation

- Documented the secure devcontainer profile and its bubblewrap requirements (#10431, #17547).
- Added TUI composer documentation for history search behavior (#17550).
- Updated app-server docs for new MCP, marketplace, turn injection, memory reset, filesystem metadata, external-agent migration, and websocket token-hash APIs (#17364, #17717, #17703, #17913, #17719, #17855, #17871).
- Documented WSL1 bubblewrap limitations and WSL2 behavior (#17559).
- Added memory pipeline documentation for extension cleanup (#17844).

## Chores

- Hardened supply-chain and CI inputs by pinning GitHub Actions, cargo installs, git dependencies, V8 checksums, and cargo-deny source allowlists (#17471).
- Added Bazel release-build verification so release-only Rust code is compiled in PR CI (#17704, #17705).
- Introduced the `codex-thread-store` crate/interface and moved local thread listing behind it (#17659, #17824).
- Required reviewed pnpm dependency build scripts for workspace installs (#17558).
- Reduced Rust maintenance surface with broader absolute-path types and removal of unused helper APIs (#17407, #17792, #17146).

## Changelog

- #17087 Add marketplace command @xli-oai
- #17409 Fix Windows exec-server output test flake @etraut-openai
- #17381 representing guardian review timeouts in protocol types @won-openai
- #17399 TUI: enforce core boundary @etraut-openai
- #17370 fix: unblock private DNS in macOS sandbox @viyatb-oai
- #17396 update cloud requirements parse failure msg @alexsong-oai
- #17364 [mcp] Support MCP Apps part 3 - Add mcp tool call support. @mzeng-openai
- #17424 Stabilize marketplace add local source test @ningyi-oai
- #17414 Fix thread/list cwd filtering for Windows verbatim paths @etraut-openai
- #10431 feat(devcontainer): add separate secure customer profile @viyatb-oai
- #17314 Pass turn id with feedback uploads @ningyi-oai
- #17336 fix(tui): recall accepted slash commands locally @fcoury-oai


---

## 💡 深度点评

### 核心亮点

*   **插件市场（Marketplace）生态扩展**：新版本引入了 `codex marketplace add` 命令，支持从 GitHub、Git URL、本地目录及 `marketplace.json` 直接安装插件。这一变化标志着 Codex 从单一工具向平台化演进，大幅降低了第三方插件的分发与集成门槛。
*   **交互式记忆管理（Memory Management）**：新增了对“记忆模式”的全面控制，包括 TUI 和 API 层面的记忆重置、删除以及扩展清理功能。用户现在可以更精准地干预模型的长期上下文状态，解决了长期对话中信息冗余或偏差的痛点。
*   **MCP 协议与插件架构成熟化**：显著增强了 MCP（Model Context Protocol）支持，引入了工具调用的命名空间管理、并行调用（parallel-call）选择性开启以及沙箱状态元数据。这些底层改进提升了复杂任务下工具链执行的可靠性与并发效率。

### 值得注意的修复

*   **沙箱与网络安全强化**：修复了 macOS 沙箱下私有 DNS 的处理问题，并移除了风险较高的 `danger-full-access` 网络模式。同时，增加了对 Unix 域套接字的白名单支持，平衡了开发便利性与系统安全性。
*   **Guardian 响应逻辑透明化**：将 Guardian（安全防护）的“超时”与“策略拒绝”状态进行了明确区分，并在 TUI 中提供针对性的引导说明。这一改动提升了用户在触发安全规则时的排查效率。
*   **跨平台兼容性优化**：修复了 Windows 平台下因路径前缀处理不当导致 `resume --last` 和 `thread/list` 失效的 Bug，确保了 Windows 开发环境下会话恢复的一致性。

### 个人评价

Codex rust-v0.121.0 是一个侧重于“平台化升级”与“工程健壮性”的版本。通过开放插件市场和深化 MCP 支持，它正在构建更强大的扩展边界；而记忆管理功能的加入，则体现了对长程对话质量的精细化追求。此外，在沙箱安全和跨平台细节上的持续打磨，反映出该项目已进入从功能堆砌向专业化工具转型的稳定期。总体而言，这是一个让开发者对工具链拥有更高控制权的务实更新。

---

**数据来源**: [GitHub openai/codex](https://github.com/openai/codex)

*Generated by OpenClaw at 2026-04-16 08:01:32*
