---
title: "🤖 Claude Code 更新日报 2026-05-30"
date: 2026-05-30T10:00:00+08:00
draft: false
tags: ["Claude Code", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🤖 Claude Code 更新 v2.1.157

**发布日期**: 2026-05-30  
**⚠️ 新版本发布**

## ✨ 新增功能

- Added `claude plugin init <name>` to scaffold a new plugin in `.claude/skills`
- Added autocomplete for `/plugin` arguments: subcommands, installed plugin names, and plugins from known marketplaces
- Added a "Workflow keyword trigger" setting in /config to stop the word "workflow" in a prompt from triggering a dynamic workflow

## 🐛 重要修复

- Fixed unprocessable images (zero-byte, corrupt) attached via paste, MCP, or dialog crashing the request instead of becoming a text placeholder
- Fixed sandbox network permission prompts appearing in auto and bypass-permissions mode when using the desktop app, IDE extensions, or SDK
- Fixed `claude agents` completed sessions not retiring when an idle subagent was still parked or had leaked a backgrounded shell
- Fixed `claude agents` pressing Esc not cancelling a slow "opening…", leaving the list unresponsive
- Fixed background agent worktrees under `.claude/worktrees/` being orphaned after the 30-day job retention sweep
- Fixed background sessions re-attached after a sleep/wake not telling the model the correct date
- Fixed copy-on-select in `claude agents` not reaching the system clipboard inside tmux with `set-clipboard on` (regression in 2.1.153)
- Fixed `--resume` not reporting background subagents that were running when the previous Claude Code process exited
- Fixed the `--resume` session picker leaving its contents on the terminal after exiting in fullscreen mode
- Fixed `--worktree` and `--worktree --tmux` returning to the canonical repo root instead of the current linked worktree

## ⚡ 优化改进

- Improved performance of long and resumed conversations by eliminating redundant message-rendering recomputations
- Removed the "bash commands will be sandboxed" startup banner — sandbox status still shows in `/status` and when a command is blocked
- Removed the "/ide for …" startup hint toast
- [VSCode] Fixed the fast mode indicator not appearing on Opus 4.8
