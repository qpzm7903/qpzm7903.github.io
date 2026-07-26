---
title: "🌐 科技日报 | 2026-07-27"
date: 2026-07-27T06:24:16+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 欧洲民间组织发起“消灭 Cookie 横幅”行动

英文原标题：[Kill the Cookie Banner!](https://killthecookiebanner.eu/)

由 BEUC、EDRi、EFF、noyb 等欧洲消费者与数字权利组织参与的行动，把矛头从“把横幅设计得更好”转向“让浏览器一次性表达隐私偏好”。行动页面称，欧盟委员会在 2025 年秋季提出以自动信号在设备和网站之间传递接受、拒绝或限制追踪的偏好，但部分成员国和行业团体正在反对这一方案。其核心主张是：追踪默认受限，Cookie 横幅是网站请求用户放弃这项权利的界面，而不是法律强制网站用横幅打扰每个人。技术上，这很像浏览器已经发送的语言偏好，只不过传递的是隐私选择；若获得法律承认，网站就能在不反复弹窗的情况下读取一致偏好。行动方同时明确说明，它只支持 Digital Omnibus 改革中的隐私信号方案，并不赞同其中可能削弱权利的其他部分。对开发者和产品团队来说，真正重要的是同意管理可能从每站一套的 UI 问题，变成浏览器信号、法律效力和站点执行之间的协议问题；在立法完成前，这仍是倡议而不是已经生效的新规则。

> **原文金句**：“The EU Commission has finally proposed a solution: set your privacy preferences in the browser once, and never see another banner.”
>
> 中文：欧盟委员会终于提出了一种办法：只在浏览器里设置一次隐私偏好，此后不再看到横幅。

### GrapheneOS 公开拆解锁屏取证防护链

英文原标题：[GrapheneOS protections against data extraction from locked devices](https://discuss.grapheneos.org/d/40700-grapheneos-protections-against-data-extraction-from-locked-devices)

GrapheneOS 的官方帖子把“手机锁着就安全”拆成一条更具体的防线：磁盘加密、PIN/密码暴力破解限速、操作系统漏洞防护、USB 物理接入限制，以及自动重启回到首次解锁前状态。帖子指出，现代取证工具通常不会直接破解加密，而是尝试在设备已经完成首次解锁后利用系统漏洞，或对 PIN/密码进行猜测；因此只看加密算法还不够。GrapheneOS 要求设备具备最新一代安全元件限速机制，并支持最长 128 字符密码和可选的“指纹 + 第二因素 PIN”，让强口令与日常便利不必二选一。系统默认在锁屏时阻止新 USB 连接，并提供 10 分钟至 72 小时的自动重启计时器，以便把密钥重新置于首次解锁前状态。官方也解释了胁迫 PIN：在任意系统身份验证提示中输入时会触发擦除，但它只是整套防护中的一个较小环节。帖子多数内容是在系统性说明已有能力，而非宣布单一新版本；它的价值是把攻击面、硬件前提和缓解措施放进同一威胁模型，方便用户判断“锁屏防护”究竟依赖哪些条件。

> **原文金句**：“They either need to exploit the OS while in After First Unlock state or brute force the PIN/password.”
>
> 中文：攻击者要么在设备处于首次解锁后的状态时利用操作系统漏洞，要么暴力猜测 PIN 或密码。

## 📰 快讯

- **英国盖特威克机场上线机器人停车服务** — 英文原标题：[Robotic Parking](https://www.gatwickairport.com/parking/parking-robotic.html)。机场官方页面显示，用户把车停进南航站楼附近的私密车库后即可带走钥匙，机器人会从车轮下方托起车辆并停入限制访问区，返程时提前把车送回取车位；官方称约 95% 的车型兼容。这不是自动驾驶汽车自己找车位，而是固定场站中的搬运机器人与预约系统结合，目标是减少找位时间并让车辆停得更紧凑。

## 📖 今日英语

- **privacy preferences** — Kill the Cookie Banner 原句：“set your privacy preferences in the browser once.” 释义：隐私偏好。为什么值得记：常见搭配有 `privacy settings`、`preference signal` 和 `consent management`。
- **rate limiting** — GrapheneOS 原句：“Android 16 QPR2 calls for a secure element implementing rate limiting ramping up delays.” 释义：速率限制，这里指连续猜错后逐步延长等待时间。为什么值得记：它既用于接口防刷，也用于密码猜测防护。
- **brute force** — GrapheneOS 原句：“...or brute force the PIN/password.” 释义：暴力穷举。为什么值得记：安全语境中常见 `brute-force attack`，指系统尝试大量候选值直到命中。
- **access-restricted parking area** — Gatwick 原句：“...park it for you in a safe, access-restricted parking area.” 释义：限制进入的停车区域。为什么值得记：`access-restricted` 是描述设施、数据或网络仅向授权对象开放的常见复合形容词。
