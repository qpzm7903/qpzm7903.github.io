---
title: "🌐 科技日报 | 2026-07-16"
date: 2026-07-16T06:42:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. Stripe 联手 Advent 向 PayPal 提出 530 亿美元收购要约，PayPal 反应冷淡

支付行业或迎来近年来规模最大的一笔并购交易。7 月 15 日据路透援引知情人士，支付独角兽 Stripe 已联手私募巨头 Advent International，向纽约上市支付公司 PayPal 提出总价约 530 亿美元收购要约——每股 60.50 美元、较 PayPal 前一交易日收盘价溢价约 28%，已获约 500 亿美元银行融资承诺。

但 PayPal 尚未就报价启动实质性谈判。原因有三：

- **价格不够吸引**：报价虽较最新股价有 28% 溢价，但仍低于 PayPal 一年前约 70 美元的股价；2021 年历史高点算下来已缩水逾八成。
- **战略转型正紧**：PayPal 正推进战略调整、改善盈利能力，管理层认为公司仍有较大价值释放空间。
- **逆向并购逻辑**：Stripe 想补齐消费者支付版图的缺口——多年来在企业支付市场领先，但在消费端缺乏全球平台。若完成收购，Stripe 将一举获得 PayPal 的 4 亿活跃账户和 Venmo 等成熟消费支付品牌。

更具象征意义的是这是典型\"新势力收购老巨头\"——成立更晚、至今仍保持非上市身份的 Stripe（1590 亿美元估值）试图收购拥有二十多年历史的支付老兵。但 PayPal 方冷淡的态度让这笔 530 亿美元的交易距离真正落地仍存在较大不确定性。

> 原文金句：现成的报道为"反向收购"（reverse takeover）叙事，路透原文措辞简洁："Stripe and Advent have made a joint offer to acquire PayPal – sources"。

\"Stripe 和 Advent 已联合提出收购 PayPal 的要约——消息人士。\"

- 路透原文：[Stripe and Advent offer to buy PayPal for more than $53 billion](https://www.reuters.com/business/finance/stripe-advent-offer-buy-paypal-more-than-53-billion-sources-say-2026-07-15/)
- 华尔街见闻详细解读：[530亿美元、28%溢价：Stripe联手Advent"反向收购"PayPal](https://wallstreetcn.com/articles/3777011)
- HN 讨论（292 分）：[https://news.ycombinator.com/item?id=48915953](https://news.ycombinator.com/item?id=48915953)

### 2. 838 家便利店集体逃离 VMware：Broadcom 的\"不确定性\"把客户推向 StorMagic

美国便利店连锁 Sheetz 宣布将把全美 838 家门店从 VMware vSphere 全面迁移到 StorMagic SvHCI——每店 11~14 台虚拟机，总计约 11,000 台。至今已迁完 600+ 家、平均每月 200 家，预计 4 个月后全部完成。

为什么走：

- **Broadcom 改许可模式**：取消 VMware 永久许可、改推大型 bundle 的订阅制——很多用户在 Broadcom 收购 VMware 后收到成本暴增通知。
- \"Broadcom created too much uncertainty\"——Sheetz 基础架构主管 Scott Robertson 的原话。
- **被留住的新东家**：Sheetz 2019 年起在 VMware 旁同时用 StorMagic 的虚拟 SAN，对产品熟、迁移路径短（不需换硬件、可远程迁不让技术人员出差店）。
- **行业大势**：Allstate、T-Mobile、Tesco 等大企业都在最近公布 VMware 迁移计划——Gartner 预计到 2028 年 35% 的 VMware 工作负载会迁移到其他平台。

为什么这件事不只是 \"一家零售连锁换虚拟化软件\"：VMware 在企业虚拟化市场近 28 年几乎等同于行业标准，Broadcom 改订阅后的用户逃亡潮是近年最大规模的一次 IT 基础设施再分配。StorMagic 之前主营 SMB 市场，这次抢到了 Sheetz 这种分布广泛的零售巨头，说明替代厂商正在从小客户向企业级跃迁。

> 原文金句：「In reality, we have always focused heavily on two distinct markets: SMB/mid-market datacenters and the 'edge' environments of large, highly distributed enterprises, like Sheetz.」

\"事实上一向有两个聚焦市场：SMB/中型数据中心，和大型高度分布式企业的'边缘'环境（像 Sheetz）。\"

- 原文：[Sheetz moves 838 stores off VMware: Broadcom created "too much uncertainty"](https://arstechnica.com/information-technology/2026/07/sheetz-moves-838-stores-off-vmware-broadcom-created-too-much-uncertainty/)

---

## 📰 快讯

### Windows 0-day 同日曝光：研究员 HiveLegacy 直击用户配置文件服务提权漏洞

就在微软发布本月创纪录的 570 个安全补丁的同一天，匿名研究员 NightmareEclypse 公开了又一个 Windows 0-day——代号 HiveLegacy，是一个权限提升漏洞，针对 Windows User Profile Service，让低权限用户可以篡改管理员用户的 classes registry hive（关联文件类型与打开应用的注册表键）。多位独立研究员确认 PoC 可用。这是 NightmareEclypse 公开的第 9 个 Windows 0-day，动机是对微软 bug 报告处理流程的不满。

- 原文：[Windows 0-day drops the same day Microsoft releases record number of patches](https://arstechnica.com/security/2026/07/windows-0-day-drops-the-same-day-microsoft-releases-record-number-of-patches/)

### 第三方应用商店下周登陆 Google Play：Epic 和解协议被撤回，法院完整反垄断救济生效

Epic Games 与 Google 之间的和解协议被撤回，意味着法院对 Google 的完整反垄断救济措施即将生效——Google Play 下周起将允许第三方应用商店。这是 Epic 诉 Google 反垄断案的关键落地，安卓应用分发生态将不再由 Google Play 单一垄断。

- 原文：[Third-party app stores coming to Google Play next week as Epic settlement withdrawn](https://arstechnica.com/gadgets/2026/07/third-party-app-stores-coming-to-google-play-next-week-as-epic-settlement-withdrawn/)

### Firefox 跑在 WebAssembly 里：puter.com 在浏览器里虚拟出完整的浏览器内核

Show HN 项目：在浏览器里用 WebAssembly 跑完整 Firefox 内核——这不是嵌套截图，是真的一个 browser-in-browser。开发者可在任何现代浏览器中加载这个 Firefox WASM 实例，用于测试跨浏览器兼容性、隔离环境运行不受信任网页，或纯粹为了好玩。HN 61 分。

- 原文：[Show HN: Firefox in WebAssembly](https://developer.puter.com/labs/firefox-wasm/)

### 大款觉能在浏览器里跑：Firefox WASM 只是开始，你还能跑 Linux、Windows 98

同一项目方（puter.com）此前演示在浏览器里跑 Linux 桌面和 Windows 98——这些演示共享同一思路：用 WASM 封装完整 OS / 应用 runtime，在浏览器的沙箱里跑，不依赖本地安装、不依赖云。

### HN 高热帖：「睡眠规律比睡眠时长更影响死亡率」（629 分）

学术研究——睡眠规律性（每天睡大致同一时间的稳定性）是死亡率风险比单纯睡眠时长更强的预测因子。这看似非科技新闻，但 HN 对此帖的热烈讨论（320 条评论）大量涉及量化自我 / 穿戴健康设备的讨论，与可穿戴生物传感器趋势有交集。原文发表在《Sleep》期刊 2023 年第 47 卷第 1 期。

- 原文：[Sleep regularity is a stronger predictor of mortality risk than sleep duration](https://academic.oup.com/sleep/article/47/1/zsad253/7280269)
- HN 讨论（629 分）：[https://news.ycombinator.com/item?id=48919363](https://news.ycombinator.com/item?id=48919363)

---

## 📖 今日英语

**perpetual license** — "Broadcom's changes, which include eliminating **perpetual licenses** in favor of subscriptions to large bundles, forced the retail chain's hand."（出处：Ars Technica Sheetz/VMware 报道）

\"永久许可\"——一次付费后可永久使用的软件授权模式，与"订阅"（subscription）相对。Broadcom 收购 VMware 后砍掉 perpetual license、改推 bundle 订阅，把 Sheetz 这种多年老客户逼走。这是企业软件行业近年最经典的一桩"许可模式转换逼用户出走"案例。常见搭配：perpetual license、perpetual vs subscription、buy perpetual、end-of-life perpetual license。

**reverse takeover / reverse acquisition** — "这是一场典型的'新势力收购老巨头'。"（出处：华尔街见闻对 Stripe/PayPal 报道的解读）

\"反向收购\"——在 M&A 语境中可指多种形态：通常意义上的"小公司收购大公司"，或在借壳上市（reverse merger）中私人公司收购已上市公司从而获得上市地位。这里指前者——成立更晚、未上市的 Stripe 试图收购上市多年、用户规模庞大的 PayPal。常见搭配：reverse takeover、reverse merger、backdoor listing。

**premium** — "报价为每股 60.50 美元，较 PayPal 前一交易日收盘价溢价约 28%。"（出处：华尔街见闻同上报道）

\"溢价\"——收购报价超出被收购方市场价的幅度。28% 溢价意味着报价比当前股价高 28%——这是在被收购方董事会尚未同意时的友好示意价格。如果对方管理层不配合，收购方可能不得不提价或转向恶意要约。常见搭配：offer at a premium、premium over closing price、28% premium。

**edge** — "A distributed enterprise with hundreds or thousands of retail, grocery, or branch locations actually faces similar IT challenges at each site as a local SMB."（出处：StorMagic 高管在 Sheetz 报道中的陈述）

\"边缘\"——在企业 IT 语境中，指分布广泛的远端小型部署点（零售门店、加油站、分行等），区别于集中的数据中心。边缘计算（edge computing）把算力下推到物理位置近用户处。Sheetz 这样的便利店连锁每店都需要小规模 IT 基础设施，是典型的 edge 场景。StorMagic 之前擅长 edge，这次正是靠 edge 场景赢得零售巨头。常见搭配：edge computing、edge location、edge vs datacenter。

**proof-of-concept (PoC)** — "multiple researchers say works... the proof-of-concept code included in the report was stripped down to prevent attackers from using it maliciously."（出处：Ars Technica HiveLegacy Windows 0-day 报道）

\"概念验证代码\"——安全研究中指能证明漏洞可被利用的最小代码示例。研究员公开 PoC 前通常会去掉关键利用步骤（"stripped down"），以防被恶意利用。但即便 stripped 也足以让攻击者推断漏洞细节。Windows 0-day 同日补丁发布的场景下，PoC 公开意味着企业必须马上打补丁、没有缓冲。常见搭配：release a PoC、stripped PoC、exploit PoC。