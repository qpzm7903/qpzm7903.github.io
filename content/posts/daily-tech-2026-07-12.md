---
title: "🌐 科技日报 | 2026-07-12"
date: 2026-07-12T06:50:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. LWN 深度回顾：住宅代理与"AI刮客之战"对开放互联网的系统性破坏

LWN.net 创始编辑 Jonathan Corbet 写了一篇最新长文（HN 325 分 / 333 评论），回顾了一年半以来"AI 训练用网页抓取"对互联网生态的破坏现状——并给了具体方向。核心要点：

1. **攻击形态**：协调得当的抓取请求在几个小时内来自数百万不同 IP，每个 IP 只碰你两三次就把你跑完，完全防不住；user-agent 字段全是假造，等你看出来是个坏 IP 它已经换下一个了。
2. **流量来源分两类**：（a）恶意/被植入的"住宅代理"网络，比如 Google 今年初刚捣毁的 IPIDEA，以及最近 Krebs 披露的——某些媒体流设备被打包成 popa 僵尸网络，被一家公开上市的以色列公司运营；（b）"看似合法"的 SDK 厂商，例如 Bright Data 这种给你免费 VPN 但在条款里塞了你设备会变成它的住宅代理出口——所有装了这个 VPN 的手机都成为攻击互联网的端点。LWN 还提到有 SDK 公司居然向 LWN 询价投广告，被直接拒绝。
3. **谁在用这些代理？**：可归因的"前沿模型公司"自己爬但公开标 user-agent、大多也尊重 robots.txt；而实际产生 DDOS 量级压垮小站的，是那些尚未公开身份的"地下模型"训练方——政府、犯罪集团、闭源创业项目。LWN 的判断是这是一场"军火竞赛"，开放互联网被夹在交叉火力之间。
4. **防御现状**：Anubis（要求客户端做工作量证明）目前被广泛部署但厂商担心它终将被绕过；商业 "prove you are human" 服务、iocaine 这种主动"投毒"工具也渐成主流。LWN 自己选择了不公开讨论具体防御措施以避免直接帮到攻击方，但承认这是持续的 arms race。

对运维、做网站、做爬虫或反爬虫的工程师来说，这是一份相当硬的资源全文——既说了"问题有多严重"也说了"目前已知防御点是什么、它们各自的局限在哪里"。

- 原文：[An update on the scraper situation](https://lwn.net/SubscriberLink/1080822/990a8a5e2d379085/)

### 2. Show HN: Ant —— 9 MB 的轻量 JavaScript runtime，冷启动 5.4 ms 起 Hono

开发者社区爆出来一个新的 JS runtime 项目 Ant（Show HN 127 分）。和 Bun / Deno / Node 这些主流 runtime 的最大区别是：Ant 的整个发行是**单 9 MB 的二进制**，自带 hand-built 的 JS 引擎 "Ant Silver"（不是 V8/JSC/SpiderMonkey 的包装），在 compat-table 上达到 100% ES 兼容、已 WinterTC Conformant，并且实际跑 Hono+Elysia+TypeScript+React+Rolldown+Wasm 这些常见生态。展示数据：跑 "import Hono, register two routes, exit" 冷启动为 5.4 ms（同一基准下 Bun 12.8 ms、Deno 24.8 ms、Node 31.1 ms）；xxx `ant install` 比 `npm install` 快最多 40 倍；TypeScript 直接运行不需要 build 步骤。目前是一个单人项目阶段，作者在文章里没有透露完整所有权与品牌背景，所以它能走多远要看社区 uptake——但如果你正在折腾"function-as-a-service 冷启动"或"边缘 runtime"的取舍，把 Ant 拉进对照集是值得的。

- 原文：[Ant, a JavaScript runtime](https://antjs.org/)

---

## 📰 快讯

### SpaceX 向 FCC 申请部署 10 万颗第三代 Starlink 卫星，承诺百倍带宽（进展）

SpaceX 已向 FCC 正式提交申请，要求部署 10 万颗第三代（Gen3）Starlink 卫星，覆盖 Ku/Ka/V/E/W/D 多个频段。Gen3 单星重超 2 吨，需要 Starship 才能批量发射（过渡期由 Falcon Heavy 顶上）。如果获批，SpaceX 承诺整体带宽比现网增长约 100 倍，延迟从现在的 30~50 ms 降到 20 ms 以内。该申请明确写将服务对象扩展到"数十亿 AI 驱动设备"——把这个星座与算力/AI 数据传输需求直接绑定。与 [7 月 11 日日报](https://qpzm7903.github.io/posts/daily-stock-2026-07-11/) 报过的"马斯克十年蓝图"相比，这是从宣告到正式 FCC 文件的进展，并且把"为 AI 设备服务"写进了频谱使用申请。

- 原文：[SpaceX wants to launch 100,000 more Starlink satellites - for 100x the bandwidth](https://www.zdnet.com/home-and-office/networking/spacex-wants-to-launch-100000-more-starlink-satellites/)

### ClickHouse：用 so_reuseport 把 PgBouncer 横向扩展到 4 倍吞吐

ClickHouse 工程团队展示了 Managed Postgres 中 PgBouncer 的横向扩展方案。由于 PgBouncer 单线程、单进程只能用一个 CPU 核，他们按核数起一组 PgBouncer 进程，全部绑定同一端口（`so_reuseport`），内核把进站连接负载均衡到各进程；进程间通过 peering 互认，使 Postgres cancel 请求能跨进程转发到实际持有 session 的进程。相同 16 vCPU `c7i.4xlarge` 实例下，单进程版峰值约 87k TPS 并随连接增多掉到 77k TPS（一个核吃满），而 16 进程 fleet 跑到 336k TPS，约 **4 倍** 吞吐。把真干活的核从 1 个扩到约 8 个，但 16 vCPU 实例整体 CPU 仍在 50% 左右——还有余量。写得非常具体、可复制，是给所有 PgBouncer 上量后卡在单核的运维人员的一份可直接照抄的方案。

- 原文：[How we scaled PgBouncer to 4x throughput](https://clickhouse.com/blog/pgbouncer-clickhouse-managed-postgres)

### SQLite 建议："prefer strict tables"——不被坑过的人不会懂

dev Evan Hahn 的一篇 HN 175 分短文：SQLite 默认创建的是"flexible"表——任何列都能塞任何数据类型，没有外键、没有类型强制。这种"灵活"在你不注意时会让你的数据库慢慢积起脏数据（一个 INTEGER 列悄悄出现 'abc' 这种）。他主张新建表时主动用 `STRICT` 关键字，让 SQLite 像 PostgreSQL 那样执行严格类型检查——既挡脏数据也更靠近日用型应用的预期。如果你写过 SQLite 但没用过 `STRICT`，这篇文章是知道 SQLite 3.37 新特性的一篇 5 分钟小课。

- 原文：[Prefer strict tables in SQLite](https://evanhahn.com/prefer-strict-tables-in-sqlite/)

### The Economist：如何躲开"杀手无人机"——军事-民用界限正在模糊

The Economist 的一篇报道（HN 81 分 / 103 评论）综述了目前民用与军用的 FPV 无人机能力如何在战场被互相借用，以及地面人员如何反制（热伪装、信号干扰、机动掩蔽等）。乌克兰战场是这场"技术互相学习"的现场：无人机让"小队级别的精确打击"成本变得极低，反过来又催生了一整套"低成本反无人机"民间智慧。文章不是财经/AI新闻，但在科技读者关注"科技如何重组战争与公共安全边界"的角度值得一看。

- 原文：[How to hide from killer drones](https://www.economist.com/science-and-technology/2026/07/08/how-to-hide-from-killer-drones)

### Amber：可编译到 Bash/Ksh/Zsh 的编程语言

Amber（HN 62 分 / 39 评论）是一种带类型、类似 TypeScript 语法的高级语言，编译目标是 Bash/Ksh/Zsh 脚本。它的卖点和 ShellCheck、bash Strict Mode 类似——让人写得像现代语言但底层跑的是 POSIX shell，主要解决"shell 脚本难维护"这个长期痛点。如果你的 CI/CD 或运维脚本已经超过百行，Amber 是一个可以考虑的"是否值得迁移"对照方案。

- 原文：[Amber the programming language compiled to Bash/Ksh/Zsh](https://amber-lang.com/)

---

## 📖 今日英语

**residential proxy** — "The term 'residential proxies' is used to describe systems that are used in this way."（出处：LWN scraper 文章原文）
"住宅代理"：通过在普通家庭/手机网络上运行代理端点，让对外请求"看起来来自普通用户"而不是数据中心。常见搭配：residential proxy network（住宅代理网络）、residential IP、mobile residential proxy。理解这个词对反爬虫、风控、广告反作弊工程师都是基础词汇。

**arms race** — "It is an arms race at this level too."（出处：LWN scraper 文章原文）
"军备竞赛"——双方不断升级对抗工具、谁也无法终结对方的循环。常见搭配：arms race between X and Y、AI arms race、cybersecurity arms race。商业/科技报道常用它来描述攻防双方互相升级模型的局面。

**cold start** — "Time to import Hono, register two routes, and exit."（Ant 项目基准说明上下文）
"冷启动"——程序从零到完成一次基本工作的时间，没占任何先前缓存或预热。常见搭配：cold start time、lambda cold start、cold start latency。在 serverless / edge runtime 讨论里是核心指标。

**reuseport / so_reuseport** — "Every process in the fleet binds the same port with `so_reuseport` enabled."（出处：ClickHouse PgBouncer 文章原文）
Linux socket 选项 `SO_REUSEPORT`，让多个进程绑定同一 TCP/UDP 端口、由内核做 load balancing。在多核扩展单线程网络服务时是常见手段，常见搭配：`SO_REUSEPORT`、reuseport load balancing。

**strict table** — "Prefer strict tables in SQLite."（出处：Evan Hahn SQLite 文章标题）
SQLite 3.37+ 的 STRICT 表语法，强制每列按声明的数据类型存储（而不是 SQLite 默认的"任何列任何类型"）。常见搭配：`CREATE TABLE ... STRICT;`、strict type checking。不熟 SQLite 内部行为的人基本不会注意到它，但它是个能直接替你挡脏数据的好特性。