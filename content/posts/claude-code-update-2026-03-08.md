---
title: "🤖 Claude Code 更新日报 2026-03-08"
date: 2026-03-08T10:00:00+08:00
draft: false
tags: ["Claude Code", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🤖 Claude Code 更新 v2.1.71

**发布日期**: 2026-03-08

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

## 💡 深度点评

### 🎯 核心亮点

**1. `/loop` 命令 — 定时任务终于来了！**
这是本次更新最重磅的功能。现在可以在会话中设置定时执行的任务，比如 `/loop 5m check the deploy` 每 5 分钟检查部署状态。这对于需要持续监控的任务非常实用，再也不用手动重复输入了。

**2. 语音体验大幅优化**
- 新增 10 种语言支持（俄语、波兰语、土耳其语、荷兰语等），现在支持 20 种语言
- Push-to-Talk 按键可以自定义了（默认是空格），再也不用担心按空格时会触发语音
- 修复了语音模式启动时 5-8 秒卡顿的问题

**3. 开发者工作流优化**
- 增加了大量 bash 命令到自动批准列表（fmt, comm, cmp, numfmt, expr, test, printf, getconf, seq, tsort, pr）
- `/plugin uninstall` 现在只修改项目本地的 `settings.local.json`，不影響团队成员
- MCP 服务器去重优化，避免重复连接

### 🔧 值得注意的修复

- **stdin 冻结问题**：长时间会话中按键无响应的问题终于修复
- **图片处理优化**：超大图片处理失败不再影响后续对话
- **启动性能**：图片处理模块改为懒加载，开机速度提升
- **睡眠唤醒**：电脑唤醒后几秒内就能恢复连接（之前最长 10 分钟）

### 📝 个人评价

v2.1.71 是一个**实用性很强的版本**。`/loop` 命令填补了 Claude Code 定时任务的能力空白，语音体验的改进也解决了用户的痛点。整体来看，Anthropic 正在不断完善开发者工作流和用户体验，尤其是 macOS 平台的兼容性。

如果你经常需要监控部署、轮询状态，或者使用语音功能，这个版本值得更新！

---

**数据来源**: [官方 CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

