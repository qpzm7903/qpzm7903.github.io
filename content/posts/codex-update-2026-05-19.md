---
title: "🔧 Codex 更新日报 2026-05-19"
date: 2026-05-19T10:00:00+08:00
draft: false
tags: ["codex", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Codex 更新 rust-v0.131.0

**发布日期**: 2026-05-19  
**⚠️ 新版本发布**

## New Features

- The TUI now offers richer session controls and display: data-driven service-tier commands, blended token usage, permissions/approval mode, effective workspace roots, and responsive Markdown tables. (#21745, #21906, #21991, #21669, #21677, #22052, #22612)
- `@` mentions now search files, directories, plugins, and skills in one picker, backed by app-server plugin metadata. (#19068, #22375)
- Plugin workflows gained marketplace CLI commands, version-aware sharing, share checkout, clearer shared-workspace buckets, and default-enabled plugin hooks. (#21396, #22397, #22425, #22435, #22549)
- Remote workflows now support daemon-managed `codex remote-control`, runtime enable/disable APIs, status reads, and registry-backed/configured remote environments. (#20718, #22218, #22562, #22578, #22877, #20667, #21323)
- The Python SDK moved to `openai-codex` / `openai_codex`, with pinned runtime-generated types, concurrent turn routing, approval modes, and integration coverage. (#21778, #21891, #21893, #21896, #21905, #21910, #22014)
- Added `codex doctor` for support-ready diagnostics across runtime, auth, terminal, network, config, and local state. (#22336)

## Bug Fixes

- Fixed several TUI interaction and rendering issues, including URL wrapping, light-mode selection contrast, Shift+Enter in tmux, `/review` MCP startup status, `/side` Esc handling, and network approval history text. (#21760, #21950, #21943, #21624, #22710, #22229)
- Hardened Windows sandbox behavior around deny-read rules, scoped write roots, ineffective firewall policy, and PowerShell edge cases. (#18202, #21479, #22353, #21400, #22643)
- Preserved managed read restrictions during permission escalation and cleaned up workspace-root permission profile resolution. (#15977, #22624, #22683)
- Made app-server and local state startup safer by preserving SQLite data, failing closed when state cannot open, adding recovery paths, and softening optional metadata sync failures. (#21831, #21847, #22580, #22734, #22899)
- Improved Git and auth reliability by using root worktree hooks consistently, ignoring repo hook/fsmonitor config in helper commands, binding local MCP OAuth callbacks, and revoking superseded login tokens. (#21969, #22843, #22652, #20237, #21747)
- Reduced remote and Windows cleanup friction with longer exec-server transport timeouts, quieter `taskkill` cleanup, and non-queued plugin reads. (#21825, #21759, #22058, #22703)

## Documentation

- Clarified that general Codex product docs should not be added to this repo, while app-server API docs remain in scope. (#21772)
- Updated plugin-creator guidance for the simplified local plugin handoff links. (#22240)
- Documented new app-server/API contracts for remote environments and the desktop-owned config namespace. (#21323, #22584)

## Chores

- Improved CI and release reliability across Rust CI, exact PR-head checkout, Windows Bazel sharding, unsigned macOS artifacts, and signed macOS promotion. (#21604, #21628, #21835, #22408, #22559, #22649, #22737, #22788, #22900)
- Split large TUI ChatWidget, history, and composer code into focused modules without intended behavior changes. (#21866, #22269, #22407, #22433, #22518, #22537, #22704, #22581, #22656)
- Continued extracting extension and tool internals, including shared tool contracts plus guardian and memory extension plumbing. (#21736, #21737, #21738, #22138, #22147, #22216, #22258, #22344, #22476, #22480, #22485, #22498)
- Removed obsolete tool paths, feature flags, config gates, and legacy hooks as defaults stabilized. (#21651, #21805, #22173, #22246, #22565, #22711, #22717, #22724, #22730)

## Changelog

- #21550 [codex] make shutdown pending-touch test deterministic @jif-oai
- #21697 Allow string service tiers in config TOML @aibrahim-oai
- #21687 [codex] Enable apply_patch freeform by default @aibrahim-oai
- #19896 Update models.json @github-actions
- #21669 Display blended token count in status line @etraut-openai
- #21677 Show permissions and approval mode in the TUI status line @etraut-openai
- #21757 api: send hyphenated session and thread headers @jif-oai
- #21763 nit: comment @jif-oai
- #21749 codex-otel: validate provider span attributes consistently @bbrown-oai
- #21767 chore: thread tui @jif-oai
- #21443 [sandboxing] Remove Darwin user cache write from Seatbelt network policy @evawong-oai
- #21604 Fix `rust-ci-full` failures due to missing `bwrap` @zanie-oai


---

## 💡 深度点评

### 核心亮点
- **终端交互（TUI）多维增强**：引入数据驱动的服务层级控制、混合 Token 消耗面板与权限/审批模式的实时显示，并支持响应式 Markdown 表格渲染，显著提升了 CLI 环境下的信息密度与可读性。
- **Python SDK 深度重构**：正式更名为 `openai-codex`，底层改为运行时生成的固定强类型（pinned types），新增并发对话路由与代码审批模式，并全面接入 app-server 集成测试框架。
- **插件体系与远程工作流完善**：插件系统新增 Marketplace CLI 工具、带版本感知的分享及 Checkout 机制；远程开发场景引入了由 Daemon 托管的 `codex remote-control`，支持运行时 API 动态启停及多环境配置注册表。
- **全局搜索体验统一**：`@` 提及功能现已打通底层 app-server 的插件元数据，支持在一个选择器内同时检索文件、目录、插件与 Skills。

### 值得注意的修复
- **Windows 沙箱安全加固**：针对 Windows 环境下的 deny-read 规则执行、写权限根目录隔离、无效防火墙策略及 PowerShell 解析边缘场景进行了底层行为修复。
- **本地状态与 SQLite 容错机制**：重写了应用服务端的启动校验逻辑，当状态数据库无法打开时采取“故障关闭（fail closed）”策略以保护 SQLite 数据免遭破坏，并补充了数据恢复路径。
- **Git 辅助命令与 Auth 稳定性**：修复了在软链接工作树（linked worktrees）中无法正确使用 Root 级 hooks 的问题，强制在内部 Git 调用中忽略 fsmonitor 及用户自定义 hooks；同时完善了本地 MCP OAuth 鉴权，支持自动吊销过期的登录 Token。

### 个人评价
Codex v0.131.0 是一个高度聚焦于系统健壮性与架构扩展性的工程优化版本。不仅通过 `codex doctor` 和大量底层清理（移除旧的工具路径、Feature flags）降低了维护成本，还在鉴权隔离和沙箱逃逸防御上做了极具针对性的收紧。Python SDK 的重命名及类型固化，配合 TUI 中新加入的权限与审批流展示，暗示了其正在向更规范、更适合企业级安全审查的自动化开发环境演进。

---

**数据来源**: [GitHub openai/codex](https://github.com/openai/codex)

*Generated by OpenClaw at 2026-05-19 08:04:12*
