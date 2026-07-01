---
title: "🔧 Openclaw 更新日报 2026-07-01"
date: 2026-07-01T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.6.11

**发布日期**: 2026-07-01  
**⚠️ 新版本发布**

## Highlights

- **More capable channel control:** Slack relay mode, native Mattermost `/oc_queue`, and per-DM model overrides make channel operations easier to automate and tune. (#94707, #95546, #95120) Thanks @sjf-oa, @amknight, @xydigit-zt, @thomaszta, and @gandalf-at-lerian.
- **Richer operator workflows:** `openclaw agent --message-file` and the RAFT CLI wake bridge add practical file-driven and remote wake-up paths. (#93351, #95497) Thanks @ooiuuii and @vincentkoc.
- **Safer plugin distribution:** additional official plugins are externalized cleanly, with bundled plugin icon metadata available to installed clients. (#95683, #95845) Thanks @vincentkoc and @Patrick-Erichsen.
- **Stronger mobile operations:** Android settings detail panels improve configuration visibility and control on mobile. (#95148) Thanks @Tosko4.
- **More reliable agent turns:** Codex partial deltas, harness activation, and long-context prompt-cache stability reduce lost progress and inconsistent runs. (#95404, #95652, #95624) Thanks @agonza1 and @vincentkoc.

## Changes

- **Gateway and plugin tooling:** channel identity hook context and per-agent usage-cost reporting give integrations and operators more precise routing and accounting. (#91903, #94483) Thanks @lanzhi-lee, @vincentkoc, and @ly-wang19.
- **Provider and model coverage:** catalog parsing, reasoning controls, provider model resolution, and encrypted reasoning support now handle more live provider variants. (#95283, #95710, #95268, #95744, #95686, #93956) Thanks @ZengWen-DT, @vincentkoc, @Marvinthebored, @Darren2030, @daniel-alejandro-t, @parveshsaini, @geraint0923, @fuller-stack-dev, and @jason-allen-oneal.

## Fixes

- **Channel delivery:** Telegram progress rendering, webhook lifecycle, reaction directives, duplicate mirror writes, queued update draining, and WhatsApp durable reply targets are now more reliable. (#95532, #93002, #95183, #94506, #94977, #95069, #95577, #95007, #95914) Thanks @amknight, @snowzlmbot, @zhangguiping-xydt, @shadow-enthusiast, @xialonglee, @travellingsoldier85, @obviyus, @hugenshen, @Cuttingwater, @heichaowo, @LiuwqGit, @freidrich-goldenflow, @mcaxtr, and @vincentkoc.
- **WhatsApp and message identity:** native quotes, Baileys group reliability, and approval reactions across JID drift now preserve the intended conversation context. (#95483, #94338, #95935) Thanks @mcaxtr, @xialonglee, and @octopuslabs-fl.
- **Gateway and session safety:** stuck release claims, draining-state reporting, remote probe timeouts, malformed paired access lists, and non-delivery session identity are handled without silent routing loss. (#95299, #94915, #89859, #92178, #95467) Thanks @mikasa0818, @kriegerbangerz-ship-it, @markoub, @vincentkoc, @maxschachere, @mushuiyu886, @gozzbb2, @wangmiao0668000666, @ly-wang19, @EmilioNicolas, @yetval, and @hellocli.
- **Agent and fallback behavior:** aborted runs stop cleanly, provider response bodies stay bounded, Claude CLI credit failures continue through fallback, and Codex usage-limit responses classify correctly. (#94412, #95218, #95508, #95420, #95418, #95417, #95400) Thanks @szsip239, @vincentkoc, @Alix-007, @mikasa0818, @sallyom, @riazrahaman, and @jason-allen-oneal.
- **Provider and model edge cases:** OpenRouter IDs, Ollama discovery and embeddings, Gemini freshness, and model-catalog prefixes now resolve against the right runtime metadata. (#95268, #94811, #93956, #95682, #95744) Thanks @Darren2030, @daniel-alejandro-t, @mushuiyu886, @jason-allen-oneal, @Sunjae-k, @parveshsaini, @vincentkoc, and @shakkernerd.
- **Configuration and UI guardrails:** non-interactive configure fails closed, TLS paths reject empty values, memory artifacts are sanitized, and the UI uses the patched DOMPurify release. (#94238, #94054, #95791, #95691) Thanks @ruomuxydt, @NianJiuZst, @miorbnli, @vincentkoc, @SweetSophia, and @YB0y.
- **Cron and delivery validation:** no-config delivery checks, thread-aware dedupe, and pending recurring runs retain their intended destinations. (#95754, #95794, #94323) Thanks @vincentkoc and @yetval.

## Complete contribution record

- **PR #95406** test(qa): make release scorecard categories explicit. Thanks @RomneyDa.
- **PR #94700** test: fold HTTP API script proof into QA Lab. Thanks @RomneyDa.
- **PR #95499** fix(test): unit-fast flow mocks. Thanks @RomneyDa.
- **PR #95308** fix(ci): filter ClawSweeper comment dispatches before token minting. Thanks @vincentkoc.
- **PR #95532** fix(telegram): materialize rich message line breaks as <br>. Related #95409. Thanks @amknight and @snowzlmbot.
- **PR #91786** fix(plugins): reconcile managed npm root overrides with managed peer pins. Related #91772. Thanks @amknight and @mkdelta221.
- **PR #93002** Fix Telegram progress draft cleanup before tool output. Related #90753. Thanks @zhangguiping-xydt and @shadow-enthusiast.
- **PR #95175** fix: route mobile exec approvals to reviewer device. Thanks @joshavant.
- **PR #94506** fix(telegram): stop clearing registered webhook on channel restart. Related #90254. Thanks @xialonglee and @travellingsoldier85.
- **PR #95183** fix(telegram): materialize streaming progress placeholders. Related #95004. Thanks @snowzlmbot and @obviyus.
- **PR #95483** fix(whatsapp): preserve native quote replies. Thanks @mcaxtr.
- **PR #94338** fix(whatsapp): wire missing Baileys retry/cache hooks for group message reliability. Related #7433. Thanks @xialonglee and @mcaxtr and @octopuslabs-fl.


---

## 💡 深度点评

### 📝 个人评价

2026.6.11 包含多项变更，请查看上方详细列表。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-07-01 08:01:43*
