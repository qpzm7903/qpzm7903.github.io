---
title: "🔧 Openclaw 更新日报 2026-07-02"
date: 2026-07-02T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.7.1

**发布日期**: 2026-07-02  
**⚠️ 新版本发布**

## Highlights

- **OpenAI GPT-5.6 support:** OpenClaw now recognizes the GPT-5.6 model family across catalog, capability, and runtime selection paths. (#98333) Thanks @steipete-oai.
- **External harness attachment:** `openclaw attach` launches an external harness against an existing Gateway session, making interactive Codex-style workflows easier to resume and inspect. (#96454) Thanks @anagnorisis2peripeteia and @obviyus.
- **Telegram Codex workflows:** Telegram can now start Codex pairing with `/login`, steer active Codex runs, and recover final replies across transient API failures. (#98006, #98126, #98786) Thanks @100yenadmin, @Kyzcreig, and @obviyus.
- **Event-driven cron runs:** the new `on-exit` schedule kind wakes an agent when a watched command exits, while session-targeted runs can detach cleanly. (#92037, #98755) Thanks @anagnorisis2peripeteia, @obviyus, and @EthanSK.
- **Native app refresh:** iOS adopts the iOS 26 visual system with clearer Chat, Talk, and onboarding flows, while native app localization expands across Apple and Android surfaces. (#98452, #98736, #97110, #97111, #97112, #97113) Thanks @vincentkoc.
- **Richer messaging:** iMessage gains native poll creation, reading, and voting, and built-in usage footers provide clearer per-turn accounting in chat. (#98421, #92657, #92877) Thanks @omarshahine, @lobster, and @Marvinthebored.
- **Safer scoped conversations:** capability profiles prepare per-conversation tool and access boundaries without weakening the existing default profile. (#98536)

## Changes

- **Model and provider coverage:** add GPT-5.6 support, use Nemotron Super's 1M context window, and preserve explicit OpenRouter authentication headers. (#98333, #98726, #98187) Thanks @steipete-oai, @eleqtrizit, @sunlit-deng, and @laurencebrown.
- **CLI and node workflows:** add `openclaw attach`, node context-path support, actionable device-approval recovery guidance, and clearer plugin install exit diagnostics. (#96454, #97679, #98115, #98146, #98497) Thanks @anagnorisis2peripeteia, @obviyus, @wm0018, @welfo-beo, @RomneyDa, @Sanjays2402, and @vincentkoc.
- **Cron and usage:** add exit-triggered schedules, detached session-targeted runs, an in-flight job doctor warning, and a built-in full usage footer. (#92037, #98755, #98620, #92657, #92877) Thanks @anagnorisis2peripeteia, @obviyus, @EthanSK, @masatohoshino, and @Marvinthebored.
- **Native apps and localization:** modernize iOS presentation and Talk controls, add Gateway speech providers, improve QR onboarding and protocol recovery, localize core Apple and Android surfaces, and add Swedish mobile localization. (#98452, #98736, #98376, #98302, #98385, #97110, #97111, #97112, #97113, #98043) Thanks @Tony-ooo, @joelnishanth, @cursoragent, @joshavant, @vincentkoc, and @yeager.
- **Messaging capabilities:** add native iMessage polls and Telegram Codex pairing and steering flows. (#98421, #98006, #98126) Thanks @omarshahine, @lobster, @100yenadmin, and @Kyzcreig.
- **Doctor and diagnostics:** expose auth-profile, workspace, device-pairing, channel-plugin, memory-provider, systemd exhaustion, and Windows LAN firewall findings. (#97125, #97358, #97366, #97496, #97968, #98291, #98666) Thanks @giodl73-repo, @masatohoshino, and @joshavant.
- **Conversation and review controls:** prepare scoped conversation capability profiles and add Cursor Agent as an autoreview engine. (#98536, #97348) Thanks @hxy91819.

## Fixes

- **Telegram durability:** recover stalled ingress claims, retry restart-dropped media, survive transient polling errors, dead-letter poison updates, preserve forwarded rich text, route plugin callbacks correctly, and fall back safely when rich final replies are rejected. (#97118, #98102, #98735, #98775, #98776, #97174, #98786) Thanks @vincentkoc, @luoyanglang, @DaveArcher18, @obviyus, and @goldmar.
- **Agent and context reliability:** preserve runtime overrides and steered subagent tasks, improve harness-aware context estimation and compaction prechecks, time out silent local streams, recover mid-stream failures, and cap Gateway run-cache growth. (#92237, #77539, #97928, #97861, #98525, #95430, #77973) Thanks @sercada, @amittell, @liuhao1024, @yetval, @osolmaz, @lzyyzznl, @vincentkoc, @alexelgier, and @fede-kamel.
- **Provider and network safety:** bound oversized or malformed responses across Moonshot, MiniMax, Anthropic OAuth, Discord, Matrix, SMS, browser, update, embeddings, Tlön, and Inworld paths. (#96502, #96322, #96644, #97693, #97662, #97999, #98455, #98508, #98554, #98496, #98660) Thanks @hugenshen, @cursoragent, @lsr911, @solodmd, @Alix-007, @wings1029, @lzyyzznl, @sunlit-deng, @vincentkoc, and @Pandah97.
- **Channel delivery and routing:** keep Slack replies in the active thread, preserve account-bound delivery routes, apply response prefixes, suppress internal traces and unwanted fallback replies, and retain WeChat session routing for opaque account ids. (#97168, #98240, #89949, #93639, #97989, #80928, #93686) Thanks @LiuwqGit, @gorkem2020, @yetval, @wangwllu, @ZengWen-DT, @alexuser, @UnClouded77, @zhangguiping-xydt, and @htkillermax-gif.
- **Cron correctness:** preserve provider and model selections on timeouts, retain startup catch-up deferrals, keep action-required output, clear blank thinking overrides, and preserve provider-owned daily-reset sessions. (#95943, #94022, #93810, #96393, #96293, #98356) Thanks @ZengWen-DT, @cursoragent, @luke-renjoy, @RichChen01, @vincentkoc, @yetval, @snowzlmbot, @nz365guy, and @takamasa-aiso.
- **Memory and session recovery:** detect unindexed transcripts, preserve notes through transient reads, avoid cross-directory resumes, disambiguate reserved wiki index pages, and skip empty QMD sync work. (#97857, #98360, #97785, #94326, #90030) Thanks @zw-xysk, @CHE10X, @qingminglong, @yetval, @vincentkoc, @sahibzada-allahyar, and @ruben2000de.
- **Windows and execution:** bind allowlisted execution to the validated Windows path, propagate `PATHEXT`, normalize inbound paths case-insensitively, and prevent cleanup crashes on Windows. (#98260, #98093, #97630, #97901) Thanks @eleqtrizit, @wendy-chsy, @VectorPeak, and @paulcam206.
- **Mobile and UI stability:** preserve iOS chat line breaks and final replies, improve Android pairing and TLS recovery, hide expired pairing cards, and keep workspace file rails scrollable. (#98304, #98117, #98366, #98439, #98483, #98049, #98646, #98611) Thanks @joshavant, @Jabato01, @ooiuuii, @wuqxuan, @645648406-max, and @zw-xysk.
- **Codex and approval flows:** report ChatGPT authentication correctly, rename destructive approval mode to `ask`, classify dynamic goal and session tool results accurately, and derive terminal-idle timeouts from the explicit run deadline. (#91240, #98501, #98659, #96856, #85296) Thanks @849261680, @ukstem, @kevinslin, @yetval, @nxmxbbd, @alkor2000, and @vincentkoc.
- **Configuration and plugin health:** surface unloadable channel plugins, preserve defaulted provider base URLs during patches, validate bundled plugin updates by manifest contract, and retain legacy ClawHub families where required. (#96397, #98396, #98010, #98249) Thanks @849261680, @momothemage, @weltmaister, @LiLan0125, @herove, and @Patrick-Erichsen.

## Complete contribution record

- **PR #96502** fix(moonshot): bound video description JSON response reads. Thanks @hugenshen and @cursoragent.
- **PR #98249** Preserve legacy ClawHub family for selected plugins. Thanks @Patrick-Erichsen.
- **PR #93767** fix(reasoning-tags): strip MiniMax `mm:` namespaced reasoning tags. Thanks @DrHack1.
- **PR #93820** fix(imessage): recognize MiniMax mm: reasoning tags in reflection guard (completes #93767). Thanks @Alix-007.
- **PR #94096** fix(usage): reject inverted startDate-endDate range in usage.cost and sessions.usage. Thanks @Alix-007.
- **PR #97125** Doctor: expose auth profile findings. Thanks @giodl73-repo.
- **PR #98256** fix(mcp): require owner for Claude permission replies. Thanks @eleqtrizit.
- **PR #98142** fix(cli): stop `pairing list` crashing with empty channel enum. Thanks @RomneyDa.
- **PR #98260** fix(exec): bind Windows allowlist execution path. Thanks @eleqtrizit.
- **PR #97118** fix(telegram): recover stalled ingress spool claims. Thanks @vincentkoc.
- **PR #97168** fix(slack): prefer current thread session for inherited outbound replies. Related #96535. Thanks @LiuwqGit and @gorkem2020.
- **PR #97769** fix(plugins): apply output text transforms to toolcall_delta and toolcall_end events. Related #97761. Thanks @ZOOWH and @get-viti.


---

## 💡 深度点评

### 📝 个人评价

2026.7.1 包含多项变更，请查看上方详细列表。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-07-02 08:52:44*
