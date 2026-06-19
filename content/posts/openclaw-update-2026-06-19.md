---
title: "🔧 Openclaw 更新日报 2026-06-19"
date: 2026-06-19T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.6.9

**发布日期**: 2026-06-19  
**⚠️ 新版本发布**

## Highlights

- **Richer Telegram delivery:** Telegram now sends rich HTML, preserves rich markdown and sticker paths, renders progress drafts and command output more faithfully, and keeps mentions and spooled handlers on the right delivery path. (#93286, #93164, #93124, #93364, #93130, #93088, #93281) Thanks @obviyus, @vincentkoc, @goutamadwant, @kesslerio, @NianJiuZst, @SweetSophia, @Marvinthebored, and @aaajiao.
- **More dependable agent recovery:** retries, terminal outcomes, usage after compaction, session history repair, and reply reconciliation now keep more interrupted or partial turns moving toward a visible final result. (#92191, #93073, #93228, #93084, #93469, #93291, #90943) Thanks @ai-hpc, @lml2468, @fuller-stack-dev, @Hollychou924, @leno23, @de1tydev, @425072024, @wuwahe3, @drvoss, @yetval, @sandieman2, and @vincentkoc.
- **A stronger Codex integration:** Codex gains automatic plugin approvals, GPT-5.3 Spark OAuth routing, remote-node `exec` as a dynamic tool, and more reliable app-server teardown and terminal outcomes. (#92625, #89133, #93654, #91767, #93287) Thanks @kevinslin, @VACInc, @vincentkoc, @JPKay-AI, and @aliahnaf2013-max.
- **Standalone official provider plugins:** external provider packages are now first-class npm releases, externally installed channel plugins load at Gateway startup, and StepFun is intentionally npm-only because its ClawHub package name is unavailable. (#93470) Thanks @sunlit-deng, @cxdnicole, and @vincentkoc.
- **More capable web and native clients:** the Control UI adds a session workspace rail and extension health, iOS adds Watch controls, and Android shows chat context. (#92856, #91952, #93387, #92837) Thanks @Solvely-Colin, @jalehman, @joshavant, and @Tosko4.
- **More useful search and skills:** Codex Hosted Search is available, key-free search providers remain deliberate opt-ins, and ClawHub skill installs retain verified source provenance. (#93446, #93616, #93283, #93506) Thanks @fuller-stack-dev, @davemorin, @momothemage, @nmccready-tars, and @vincentkoc.

## Changes

- Providers and auth: add Codex Hosted Search, improve Gemini CLI OAuth behind proxies, and keep external provider onboarding on current choices and package metadata. (#93446, #92815) Thanks @fuller-stack-dev, @yetval, @EvetteYoung, and @vincentkoc.
- Plugins and installs: externalized official providers publish as independent npm packages, Gateway discovers installed channel plugins at startup, and StepFun installs exclusively from npm. (#93470) Thanks @sunlit-deng, @cxdnicole, and @vincentkoc.
- Dashboard and mobile: add a session workspace rail, plugin health in status, compact cron lists, and iOS Watch controls. (#92856, #91952, #93395, #93387) Thanks @Solvely-Colin, @jalehman, @yu-xin-c, @centralpc, @joshavant, and @vincentkoc.
- Codex and skills: add automatic plugin approvals, preserve ClawHub skill provenance, and expose remote-node execution to Codex when a node is connected. (#92625, #93283, #93654) Thanks @kevinslin, @momothemage, @nmccready-tars, @vincentkoc, and @JPKay-AI.
- QA and release engineering: QA scenarios now use YAML, with broader profile evidence and release coverage for the plugin and channel matrix.

## Fixes

- Security and privacy: redact secrets from debug/config output, block internal HTTP session overrides, audit open-DM tool exposure, and retain plugin write ownership checks. (#93333, #88496, #93443, #92883, #93353) Thanks @Alix-007, @jason-allen-oneal, @coygeek, @RichardCao, @yu-xin-c, @cjg20ss, @eleqtrizit, and @vincentkoc.
- Agent and session runtime: retry thinking-only and empty post-tool turns, prevent duplicate hook execution, preserve fresh usage through compaction, and repair partial JSON/history artifacts. (#92191, #93073, #93009, #93084, #93469) Thanks @ai-hpc, @lml2468, @fuller-stack-dev, @zenglingbiao, @dertbv, @Hollychou924, @leno23, @de1tydev, @425072024, @wuwahe3, @drvoss, and @vincentkoc.
- Channels and replies: fix Telegram rich delivery and ingress recovery, preserve WhatsApp auth and media error reporting, keep Mattermost thread replies intact, and harden Discord action handling. (#93286, #93364, #93281, #93076, #93334, #93424, #93488) Thanks @obviyus, @NianJiuZst, @mcaxtr, @rushindrasinha, @amknight, @lzyyzznl, @darealgege, and @vincentkoc.
- Storage and migrations: avoid SQLite WAL on network filesystems, clean reindex artifacts, keep setup state out of workspace dot-directories, and import default-agent auth profiles into SQLite. (#93454, #92891, #93182, #93295, #93520, #93156) Thanks @vincentkoc, @ZengWen-DT, @Zeng-wen, @potterdigital, @Alix-007, @Pick-cat, @sallyom, @1qh, and @Tazio7.
- Provider and model behavior: fix Gemini CLI proxy OAuth, restore Codex Spark OAuth routing, correct Bedrock embedding model IDs, and preserve configured defaults in embedded runs. (#92815, #89133, #93452, #93428) Thanks @yetval, @EvetteYoung, @VACInc, @LiuwqGit, @aleck31, @zenglingbiao, @danielgerlag, and @vincentkoc.
- CLI, TUI, and apps: accept global flags after subcommands, keep terminal output and activity indicators visible, preserve CJK IME composition, and refresh stale UI state. (#93455, #93460, #93006, #93427, #93498, #93606) Thanks @ooiuuii, @Alix-007, @ZengWen-DT, @Zeng-wen, @AlethiaQuizForge, @Zhaoqj2016, @liuhao1024, @BrianClaw1955, @vincentkoc, and @NicoBoom13.
- Operations and updates: harden official plugin recovery, restart managed Gateways after failed update handoff, avoid Node-specific npm prefixes, and keep package validation paths reliable. (#93325, #92111, #93650) Thanks @vincentkoc, @yetval, @ofan, and @yaanfpv.

## Complete contribution record

- **PR #90463** refactor: add session accessor seam with gateway consumer. Thanks @jalehman.
- **PR #88656** Drop reasoning-only length turns from replay. Thanks @abel-zer0.
- **PR #92856** feat(webui): add session workspace rail. Thanks @Solvely-Colin.
- **PR #92845** docs(browser-control): document OPENCLAW_EAGER_BROWSER_CONTROL_SERVER requirement. Related #92841. Thanks @liuhao1024 and @jeugregg.
- **PR #82366** fix: use passive periodic sqlite wal checkpoints. Related #81715. Thanks @honor2030 and @KrasimirKralev.
- **PR #92815** fix(google): route Gemini CLI OAuth through the env proxy (#46184). Thanks @yetval and @EvetteYoung.
- **PR #91331** fix(mattermost): merge progress preview lines by identity. Related #89761. Thanks @iloveleon19 and @leonthe8th and @vincentkoc.
- **PR #92909** fix(tui): keep spinner active when toggling tools. Related #49763. Thanks @ZengWen-DT and @Zeng-wen and @vincentkoc and @CrimsonDump.
- **PR #92904** fix(elevenlabs): use current TTS model ids. Thanks @vortexopenclaw and @vincentkoc.
- **PR #92642** fix #86872: Subagent run reports success but fails to write output file. Thanks @zhangguiping-xydt and @vincentkoc and @zapper35.
- **PR #89122** refactor: route command session reads through seam. Thanks @jalehman.
- **PR #90943** fix(reply): deliver final reply when queued follow-up claims session; scope dedupe to routed thread. Thanks @sandieman2 and @vincentkoc.


---

## 💡 深度点评

### 📝 个人评价

2026.6.9 包含多项变更，请查看上方详细列表。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-06-19 08:10:40*
