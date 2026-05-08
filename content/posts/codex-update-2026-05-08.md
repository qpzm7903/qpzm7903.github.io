---
title: "🔧 Codex 更新日报 2026-05-08"
date: 2026-05-08T10:00:00+08:00
draft: false
tags: ["codex", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Codex 更新 rust-v0.129.0

**发布日期**: 2026-05-08  
**⚠️ 新版本发布**

## New Features

- The TUI now supports modal Vim editing in the composer, including `/vim`, default-mode config, and Vim-specific keymap contexts. (#18595)
- TUI workflows are easier to resume and copy from with a redesigned resume/fork picker, raw scrollback mode, `/ide` context injection, and workspace-aware `/diff`. (#20065, #20819, #20294, #21001)
- The status line can show theme-aware colors plus optional PR and branch-change summaries, and `/keymap debug` helps inspect terminal key events. (#19631, #20892, #20794)
- Plugin management now supports workspace sharing, share access controls, source filtering, local share path tracking, marketplace removal/upgrades, remote bundle sync, and admin-disabled status handling. (#20278, #21124, #21419, #20560, #19843, #20478, #20268, #20298)
- Hooks can be browsed and toggled from `/hooks`, can run before/after compaction, and can add `PreToolUse` context; Codex Apps auth and eligible MCP elicitations now surface through TUI/Guardian flows. (#19882, #19905, #20692, #19193, #19431)
- Experimental goals are now discoverable, stay paused across resume unless the user opts back in, and show clearer validation and multi-day duration output. (#20083, #20790, #20746, #20558)

## Bug Fixes

- `/copy` works better in tmux, Alt+Enter and modified Delete/Backspace keys behave correctly, and Windows typing/paste latency was reduced. (#20207, #20535, #21058, #18914)
- Large paste placeholders and Ctrl+C-stashed drafts now survive clear/editor workflows without corrupting draft history. (#21091, #21190, #21351, #21397)
- TUI startup and accessibility were tightened by bounding terminal probes, clearing the first inline viewport render, and honoring `animations = false` for live rows. (#20654, #21450, #20564)
- Linux sandbox startup is more reliable across older `bwrap`, slow mount probes, symlink-protected paths, and shared `/tmp` setups. (#20628, #20111, #21127, #21234)
- Windows sandbox and exec policy now handle named pipes, ConPTY teardown, PowerShell-wrapped allow rules, worktree `safe.directory`, and unsafe Git options more reliably. (#20270, #20685, #20336, #21409, #21275)
- Fixed custom CA login behind TLS-inspecting proxies, Bedrock runtime endpoint reporting, dangerous project config keys, heredoc redirect approval matching, and unbounded MCP/hook output growth. (#20676, #20275, #20098, #20113, #20260, #21069)

## Documentation

- Updated the embedded OpenAI Docs sample skill so API-key setup guidance stays aligned with other docs variants. (#21263)
- Documented how generated git commit attribution is gated by `codex_git_commit` and configured in `config.toml`. (#21379)
- Removed local-only planning/spec docs and redirected config docs toward the maintained external documentation surface. (#20896)

## Chores

- Linux releases now build, publish, bundle, and verify a standalone `bwrap` fallback for npm and DotSlash installs. (#21255, #21256, #21257, #21312, #21285)
- Vendored Bubblewrap was updated to 0.11.2, including upstream security changes around setuid support. (#21389)
- Windows Bazel CI now uses faster cross-compilation for tests, clippy, and release-build checks, and Bazel now runs sharded Rust integration tests. (#20585, #20701, #21057)
- App-server and protocol internals were split and slimmed down, including transport extraction, protocol module decomposition, thread/message history moves, and tool-handler cleanup. (#20324, #20325, #20348, #20545, #21251, #21278, #21395)
- Analytics and diagnostics coverage expanded for tool lifecycles, goals, plugin skills, thread sources, service tiers, and PR issue labeling. (#17089, #17090, #20799, #20923, #20949, #20969, #20893)

## Changelog

- #20278 feat: Add workspace plugin sharing APIs @xl-openai
- #20334 Make missing config clears no-ops @etraut-openai
- #20246 Gate multi-agent v2 tools independently of collab @jif-oai
- #20361 realtime: rename provider session ids @aibrahim-oai
- #20260 fix(core): truncate large mcp tool outputs in rollouts @owenlin0
- #20083 Mark goals feature as experimental @etraut-openai
- #19843 /plugins: remove marketplace @canvrno-oai
- #20458 [Extension] Allowlist Chrome Extension in the tool_suggest tool @teddywyly-oai
- #20324 Remove core protocol dependency [1/2] @etraut-openai
- #20299 Move item event mapping into app-server-protocol @pakrym-oai
- #20325 Remove core protocol dependency [2/2] @etraut-openai
- #20471 Stop emitting item/fileChange/outputDelta output delta notifications @pakrym-oai


---

## 💡 深度点评

Codex Rust-v0.129.0 版本发布，本次更新重点围绕终端交互体验、插件系统架构以及底层沙箱稳定性进行了深度优化。

### 核心亮点

*   **TUI 引入 Vim 模式**：Composer 正式支持模态编辑（通过 `/vim` 开启），并允许通过配置文件设置默认模式。这对于依赖 HJKL 导航和 Vim 快捷键的开发者来说，大幅降低了在 AI 对话框中进行代码微调的摩擦力。
*   **插件系统协作化与管控增强**：新增了插件的工作区共享（Workspace Sharing）与访问控制功能。同时，移除了内置 Marketplace 转向更灵活的远程 Bundle 同步，支持管理员禁用状态处理，标志着插件系统正从“本地辅助”向“团队协作”演进。
*   **TUI 工作流深度集成**：新增了 `/ide` 上下文注入以及具备工作区感知能力的 `/diff` 功能。配合重新设计的会话 Fork 选择器和原始滚动模式（Raw scrollback），Codex 在终端内的上下文处理能力变得更加精准且易于追溯。

### 值得注意的修复

*   **跨平台沙箱稳定性**：针对 Linux 环境优化了 `bwrap` 在旧版本内核或特殊挂载环境下的兼容性；针对 Windows 修复了 ConPTY 生命周期管理及命名管道访问权限问题，提升了执行策略（Exec Policy）的可靠性。
*   **交互数据防丢**：修复了大型粘贴占位符和通过 `Ctrl+C` 暂存的草稿在执行 `/clear` 或编辑器流转时可能被破坏的 Bug，确保长对话或大代码块操作的安全性。
*   **复杂网络环境适配**：修复了在 TLS 检测代理（TLS-inspecting proxies）环境下的自定义 CA 登录问题，这对于企业级内网用户而言是关键的生产力修复。

### 个人评价

v0.129.0 是一个从“好用”向“专业”迈进的稳定版本。Vim 模式的加入补齐了终端交互最后一块短板，而底层协议（App-server protocol）的拆分与重构，则显示出团队正在清理架构债，为更复杂的并发任务和多智能体协作做准备。整体来看，Codex 正在变得更加稳健，且越来越像一个原生的、可高度定制的开发者环境而非单纯的 CLI 工具。

---

**数据来源**: [GitHub openai/codex](https://github.com/openai/codex)

*Generated by OpenClaw at 2026-05-08 08:01:35*
