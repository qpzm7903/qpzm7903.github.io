---
title: "🌐 科技日报 | 2026-07-28"
date: 2026-07-28T06:36:10+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 用现成标准重新拼一套 HTTP 邮件协议

英文原标题：[Modern email can be built from borrowed parts](https://en.andros.dev/blog/d7ed8b07/modern-email-can-be-built-from-borrowed-parts/)

Andros Fenollosa 做的不是又一个邮件客户端，而是一场协议设计练习：保留 `user@domain` 地址外形，把 SMTP、收取、身份、加密和同步全部换成已有的 Web 标准。文章把设想命名为 HMTP，并用 HTTP/TLS 传输、WebFinger 发现用户、向 inbox 发 POST 送信、Ed25519 签名、HPKE 内容加密、sigchain 处理密钥轮换、JMAP 同步和 WebPush 推送。关键思想是“不发明任何底层技术，只发明组合方式”；每一块都已有 RFC 或被 Mastodon、Signal、Fastmail、Bluesky 等大规模系统使用。HTTP 状态码还能直接表达排队、限流、邮箱不存在、迁移和负载过大，现成代理、负载均衡器与语言库也无需重造。静态网站甚至可以通过 WebFinger JSON 把不同用户的邮箱委派给不同服务商，比 MX 记录更细粒度。它并不打算兼容 Gmail，也不是可立即替换现有邮件的标准；价值在于具体展示，协议现代化有时不是创造新密码学，而是把经过实战的组件用更清晰的信任边界组装起来。

> **原文金句**：“This design doesn't invent a single technology: everything already exists.”
>
> 中文：这套设计没有发明任何单项技术：一切都已经存在。

### 一个未鉴权入口如何暴露 67.6 万辆商用车

英文原标题：[Exploiting Volvo/Eicher’s fleet management platform to gain control over all users and vehicles](https://eaton-works.com/2026/07/27/my-eicher-hack/)

安全研究员 Eaton 披露了对 Volvo Group 与 Eicher Motors 合资企业 VE Commercial Vehicles 的 My Eicher 车队平台研究。My Eicher 用于商用车实时定位、仪表数据、电子围栏和车队管理；研究者发现部分 API 可在未认证状态下暴露隐藏的内部与管理员接口。按照披露中的快照，这条路径能够造成账户接管，进而控制企业的整个车队；API 中可见约 74.8 万客户、17.4 万用户、18.6 万人员、67.6 万辆车和 7.6 万份证件记录，证件包括 Aadhaar 卡和驾驶证。这里的“控制车辆”主要指获得平台内对车队数据与管理功能的高权限，并不等于远程操纵方向盘或刹车。事件说明车联网风险不只在车载固件：连接车辆、人员、证件和运营权限的 SaaS 管理面本身就是高价值控制平面。披露文章提供了技术路径与影响范围，但这些数字来自研究者看到的 API 数据，平台方最终修复与审计结论仍需继续关注。

> **原文金句**：“A vulnerability was found in the APIs that made it possible to discover hidden, unauthenticated internal/admin APIs.”
>
> 中文：API 中的一个漏洞使隐藏且无需认证的内部/管理员接口能够被发现。

## 📰 快讯

- **[VLC for Unity 正式列出 Linux 支持](https://code.videolan.org/videolan/vlc-unity)**：官方仓库现将 Ubuntu 22.04 LTS 或同等系统、x86_64 和 OpenGL 列入支持范围，并说明已在 Ubuntu 22.04/24.04 测试。当前走 X11 的 GLX 或 XWayland 的 EGL，需要 DRI3 与实体 GPU；原生 Wayland 和非 Android 平台的 Vulkan 仍在路线图中。

## 📖 今日英语

- **borrowed parts** — HMTP 标题：“Modern email can be built from borrowed parts.” 释义：借来的现成组件。为什么值得记：工程语境里强调复用成熟构件，而非从零创造。
- **battle-tested at scale** — HMTP 原句：“Every piece we are going to use is standardized, deployed and battle-tested at scale.” 释义：经过大规模实战检验。为什么值得记：比单纯的 `production-ready` 更强调长期真实负载验证。
- **account takeover** — My Eicher 原句：“These APIs could be used to gain high-level access to systems and even enable account takeover.” 释义：账户接管。为什么值得记：安全报告里常缩写为 ATO，表示攻击者获得受害者账户控制权。
- **performance oriented video rendering** — VLC for Unity 原句：“the native Unity plugin that bridges LibVLCSharp with LibVLC for performance oriented video rendering.” 释义：面向性能的视频渲染。为什么值得记：`performance-oriented` 常用于说明设计优先级。
