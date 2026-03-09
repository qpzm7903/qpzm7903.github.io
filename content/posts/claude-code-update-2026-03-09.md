---
title: "🤖 Claude Code 更新日报 2026-03-09"
date: 2026-03-09T10:00:00+08:00
draft: false
tags: ["Claude Code", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🤖 Claude Code 更新 v2.1.71

**发布日期**: 2026-03-09

## ✨ 新增功能

- Added `/loop` command to run a prompt or slash command on a recurring interval (e.g. `/loop 5m check the deploy`)
- Added cron scheduling tools for recurring prompts within a session
- Added `voice:pushToTalk` keybinding to make the voice activation key rebindable in `keybindings.json` (default: space) — modifier+letter combos like `meta+k` have zero typing interference
- Added `fmt`, `comm`, `cmp`, `numfmt`, `expr`, `test`, `printf`, `getconf`, `seq`, `tsort`, and `pr` to the bash auto-approval allowlist
- Added the `/claude-api` skill for building applications with the Claude API and Anthropic SDK
- Added Ctrl+U on an empty bash prompt (`!`) to exit bash mode, matching `escape` and `backspace`
- Added numeric keypad support for selecting options in Claude's interview questions (previously only the number row above QWERTY worked)
- Added optional name argument to `/remote-control` and `claude remote-control` (`/remote-control My Project` or `--name "My Project"`) to set a custom session title visible in claude.ai/code


## 🐛 重要修复

- Fixed stdin freeze in long-running sessions where keystrokes stop being processed but the process stays alive
- Fixed a 5–8 second startup freeze for users with voice mode enabled, caused by CoreAudio initialization blocking the main thread after system wake
- Fixed startup UI freeze when many claude.ai proxy connectors refresh an expired OAuth token simultaneously
- Fixed forked conversations (`/fork`) sharing the same plan file, which caused plan edits in one fork to overwrite the other
- Fixed the Read tool putting oversized images into context when image processing failed, breaking subsequent turns in long image-heavy sessions
- Fixed false-positive permission prompts for compound bash commands containing heredoc commit messages
- Fixed plugin installations being lost when running multiple Claude Code instances
- Fixed claude.ai connectors failing to reconnect after OAuth token refresh


## ⚡ 优化改进

- Improved startup time by deferring native image processor loading to first use
- Improved bridge session reconnection to complete within seconds after laptop wake from sleep, instead of waiting up to 10 minutes
- Improved `/plugin uninstall` to disable project-scoped plugins in `.claude/settings.local.json` instead of modifying `.claude/settings.json`, so changes don't affect teammates
- Improved plugin-provided MCP server deduplication — servers that duplicate a manually-configured server (same command/URL) are now skipped, preventing duplicate connections and tool sets. Suppressions are shown in the `/plugin` menu.
- Updated `/debug` to toggle debug logging on mid-session, since debug logs are no longer written by default
- Removed startup notification noise for unauthenticated org-registered claude.ai connectors
- Improved error message when microphone captures silence to distinguish from "no speech detected"
- Improved compaction to preserve images in the summarizer request, allowing prompt cache reuse for faster and cheaper compaction


---

**数据来源**: [官方 CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

