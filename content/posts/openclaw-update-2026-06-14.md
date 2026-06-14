---
title: "🔧 Openclaw 更新日报 2026-06-14"
date: 2026-06-14T10:00:00+08:00
draft: false
tags: ["openclaw", "AI 编程", "更新日志"]
categories: ["工具更新"]
---

# 🔧 Openclaw 更新 2026.6.8

**发布日期**: 2026-06-14  
**⚠️ 新版本发布**

## Highlights

- Telegram and WhatsApp channel delivery are richer and less brittle: Telegram can send structured rich text with tables, lists, expandable blockquotes, prompt-preserving CLI backend delivery, retired native draft migration, and safer rich-media boundaries, while WhatsApp now honors configured ACP bindings. (#92679, #84082, #89421, #92513) Thanks @obviyus, @jzakirov, @spacegeologist, and @TurboTheTurtle.
- Agent and Gateway recovery is sharper across account-scoped DM sends, generated media completions, restart shutdown aborts, yielded subagent pauses, yielded cron media, heartbeat dedupe, session identity prompts, and unknown OpenAI agent selector rejection. (#92788, #91246, #91357, #92631, #92146, #91287, #92468, #92510) Thanks @yetval, @TurboTheTurtle, @ooiuuii, @openperf, @IWhatsskill, @ZengWen-DT, and @zhangguiping-xydt.
- Provider/model handling expands and tightens with GLM-5.2, Claude Haiku 4.5 catalog rows, OpenRouter and Google Vertex provider-prefix normalization, managed SecretRef auth, bounded model browse discovery, storeless OpenAI Responses replay gating, and Claude 4.5 Copilot tool-streaming safety. (#92796, #90116, #92627, #91218, #90686, #92247, #90706, #75393) Thanks @arkyu2077, @liuhao1024, @bymle, @rohitjavvadi, @samson910022, @snowzlm, and @Kailigithub.
- `/usage` and reply payload hooks now have a native full footer renderer, default template, fixed-decimal formatting, credential-aware limits, better partial-count handling, and warnings for broken templates instead of silent bad output. (#92657, #89835, #89629) Thanks @Marvinthebored.
- UI and mobile flows are steadier: workspace files can collapse and start collapsed, WebChat backscroll survives streaming, the sidebar session picker remains interactive above the desktop workbench, reset soft args survive UI dispatch, stale dashboard session parent lineage is preserved, and iOS reconnects stale foreground gateways. (#92779, #92622, #92705, #91353, #90658, #92552) Thanks @shakkernerd, @TurboTheTurtle, @NianJiuZst, @zhouhe-xydt, @luoyanglang, and @Solvely-Colin.
- Memory, state, and diagnostics recover cleaner: oversized OpenAI embedding batches split before 431s, QMD memory search stays available in transient mode, SQLite avoids WAL on NFS state volumes, stuck-session recovery scheduling no longer resets warning backoff, and Infinity chunk limits stay genuinely unbounded. (#92650, #92618, #92639, #91247, #92752, #92735) Thanks @mushuiyu886, @TurboTheTurtle, @849261680, @gnanam1990, and @yhterrance.

## Changes

- Providers/models: add GLM-5.2 support and Claude Haiku 4.5 catalog entries while keeping provider-qualified model IDs normalized across OpenRouter and Google Vertex paths. (#92796, #90116, #92627, #91218) Thanks @arkyu2077, @liuhao1024, and @bymle.
- Channel plugins: ship Telegram rich-message delivery and WhatsApp ACP binding support, including rich prompt handoff to CLI backends and transport fixtures for richer drafts. (#92679, #92513) Thanks @obviyus and @TurboTheTurtle.
- Agent commands: support `/btw` in CLI-backed sessions and keep CLI usage-error exits classified as usage failures instead of successful runs. (#92669, #92162) Thanks @joshavant and @Pandah97.
- Usage hooks: add built-in full footer rendering, default footer templates, per-turn usage state, credential-aware limits, and fixed-decimal formatting for usage-bar templates. (#92657, #89835, #89629) Thanks @Marvinthebored.
- Docs and operator guidance: document node config examples, clarify before-install hook scope, correct agent default concurrency comments, refresh ZAI provider docs, and update channel/group docs for current Telegram and WhatsApp behavior. (#92677, #92766, #92695) Thanks @liuhao1024, @sallyom, and @ArielSmoliar.

## Fixes

- Channels and delivery: preserve account-scoped DM channel send policy, rich Telegram final replies, rich Telegram tables and lists, Telegram thread-create CLI remapping, Slack outbound `message_sent` hooks, contributed message-tool schema optionality, same-channel generated media completions, and channel chunking around surrogate pairs and Infinity limits. (#92788, #92679, #89421, #89943, #91137, #91246, #92735) Thanks @yetval, @obviyus, @spacegeologist, @rishitamrakar, @lundog, @TurboTheTurtle, and @yhterrance.
- Agent, cron, and Gateway runtime: mark active main sessions before restart shutdown aborts, pause yielded subagent runs whose terminal also signals abort, preserve yielded media completions, de-duplicate main-session heartbeat events, expose session identity in runtime prompts, reject unknown OpenAI agent selectors, keep generated media completions in WebChat, and require admin privileges for HTTP session/model override surfaces. (#91357, #92631, #92146, #91287, #92468, #92510, #91246, #92651, #92646) Thanks @ooiuuii, @openperf, @IWhatsskill, @ZengWen-DT, @zhangguiping-xydt, and @TurboTheTurtle.
- Providers and model replay: preserve storeless OpenAI Responses replay compatibility, avoid eager tool streaming for Claude 4.5 in Copilot, honor profile auth for SecretRef model entries, bound model browsing, strip provider prefixes where runtimes need bare IDs, and surface nested embedding fetch failures. (#90706, #75393, #90686, #92247, #92627, #91218, #92628) Thanks @snowzlm, @Kailigithub, @rohitjavvadi, @samson910022, @liuhao1024, @bymle, and @mushuiyu886.
- Memory, state, diagnostics, and config: split header-too-large embedding batches, keep QMD memory search enabled in transient mode, avoid SQLite WAL on NFS volumes, preserve recovery scheduling outside stuck-session warning backoff, and keep shell environment fallbacks contained in config write tests. (#92650, #92618, #92639, #91247, #92752) Thanks @mushuiyu886, @TurboTheTurtle, @849261680, and @gnanam1990.
- UI/mobile/TUI: preserve dashboard session parent lineage, WebChat backscroll, reset soft command args, sidebar session picker interactivity, collapsed workspace files, resolved `/model` confirmation refs, and stale foreground iOS Gateway reconnects. (#90658, #92622, #91353, #92705, #92779, #92773, #92552) Thanks @luoyanglang, @TurboTheTurtle, @zhouhe-xydt, @NianJiuZst, @shakkernerd, @NarahariRaghava, and @Solvely-Colin.
- Release and test reliability: extend slow Gateway/full-suite watchdogs, split local full-suite shards when throttled, stabilize plugin auth marker fixtures, avoid brittle provider-ref error text, and keep QA Lab bootstrap selection assertions aligned with flow-only scenarios. (#92652)


---

## 💡 深度点评

以下是对 openclaw 2026.6.8 更新内容的深度点评：

### 核心亮点

- **IM 渠道交付能力的质变**：Telegram 现已支持表格、列表及可折叠引用等富文本结构，并解决了原生草稿迁移的边界问题；同时 WhatsApp 实现了 ACP 绑定支持。这标志着 Agent 在即时通讯端的表现力从简单的“对话框”向“结构化界面”演进。
- **运行时鲁棒性（Recovery）的全面加固**：针对 Gateway 和 Agent 的恢复逻辑进行了深度梳理，涵盖了账号作用域下的 DM 发送、生成的媒体文件补全、心跳去重以及会话身份注入。这些变更显著提升了长连接和后台任务在异常中断后的自愈能力。
- **模型生态规范化与 Secret 鉴权升级**：除了新增 GLM-5.2 和 Claude Haiku 4.5 支持外，重点优化了 OpenRouter 和 Google Vertex 的 Provider 前缀规范化。配合受控的 SecretRef 认证机制，进一步统一了多模型调用的身份管理逻辑。

### 值得注意的修复

- **大规模 Embedding 处理优化**：针对超长请求导致的 431 错误，系统现在会自动拆分超大批次的 OpenAI Embedding 请求，确保了长文本索引的稳定性。
- **基础设施兼容性修正**：修复了 SQLite 在 NFS 网络文件系统卷上因 WAL 模式导致的状态冲突，并解决了 iOS 端前台 Gateway 状态过时后的自动重连问题。
- **安全与工具流治理**：限制了 HTTP 会话/模型覆盖接口必须具备管理员权限，并修正了 Claude 4.5 在 Copilot 中的工具流式传输安全性。

### 个人评价

2026.6.8 版本的核心关键词是“生产力交付”。它并没有盲目堆砌新模型，而是将重点放在了 IM 渠道的渲染质量、跨平台模型标识的标准化以及复杂存储环境（如 NFS）下的稳定性。通过 `/usage` 原生页脚渲染和更精细的 Embedding 批次拆分，openclaw 正在从一个开发工具演变为一个能够应对高并发、多端复杂环境的成熟 Agent 运行时基础设施。

---

**数据来源**: [GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)

*Generated by OpenClaw at 2026-06-14 08:13:22*
