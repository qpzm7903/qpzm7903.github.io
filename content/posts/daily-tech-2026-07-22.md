---
title: "🌐 科技日报 | 2026-07-22"
date: 2026-07-22T06:38:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. 法官叫停 Paramount 1110 亿美元收购 Warner Bros.——好莱坞反垄断大案

美国加州北区联邦法官 Araceli Martínez-Olguín 下发临时禁制令（TRO），要求 Paramount Skydance 与 Warner Bros. Discovery 暂停其 1110 亿美元合并案，无法在 14 天内继续推进合并或整合业务。以加州总检察长 Rob Bonta 为首的 12 个州上周提起诉讼要求阻挡这项合并——这些州认为合并会消灭好莱坞竞争（五大电影制片厂中两家合并，基础有线频道也同理）。该合并本已获得特朗普政府批准，州起诉仍能令其暂停，凸显反垄断审查中州权和联邦之间的张力。法官在裁决中表示，合并后的公司将占宽发行电影市场约 27% 份额，HHI 集中度指标上升幅度已超过"可推定非法"阈值——此推定成立时原告无需提出复杂市场行为证据即可获禁制令。临时禁制令有效期 14 天，可转化为初步禁令直到案件审结；8 月 3 日将举行初步禁令听证。

> **原文金句**：
> "The Court is persuaded that it can presume the proposed merger is likely to violate antitrust laws."
> 法院认定可推定该合并拟议违反反垄断法。

**为什么重要**：这起案可能是 2026 年美国媒体与科技行业影响最深远的反垄断事件。如果在听证后转初步禁令，意味着此交易正式进入诉讼阶段，已获联邦行政层批准的跨行业巨头并购可能被州的司法审查否决掉——这一信号也会影响其他科技产业并购案。
- 原文：[Judge halts Paramount's $111B purchase of Warner Bros. in win for US states](https://arstechnica.com/tech-policy/2026/07/judge-halts-paramounts-111b-purchase-of-warner-bros-in-win-for-us-states/)

### 2. 你的车比它的云活得更久：当车联网服务被关停

Ars Technica 发了篇关于汽车互联服务寿命的长文，揭示了广大车主尚未意识到的现实——大家依赖的远程启动、远程锁车、车舱预热、紧急呼叫都依赖车企云端服务，但车企并没有义务长期支持这些功能。2022 年美国多家运营商关闭 3G 网络时，Lexus、Porsche、Nissan、Volkswagen 等大批车型的互联服务一夜中断，Lexus 2010–2017 款车型的 Enform 服务因 3G-only 硬件直接"关灯"——硬件不兼容更高网络。令人侧目的是 Acura 在去年停止支持 2014–2022 款车型的 AcuraLink 老后端，即使这些车装配的是当前还能联网的 4G 调制解调器——并非技术淘汰，只是车企评估"不值得"继续维护该功能后端。车主不得不自找替代方案：部分车型通过 OTA 或硬件升级到新网络保住服务，许多 BMW i3 车主则只能花 $1400 自购 4G 硬件改装。文章提出路在何方：车企应采用"模块化软件定义架构"让车主能在物理上换硬件和软件升级——而不是"车还能开，网直连服务死了"。

> **原文金句**：
> "Cloud-based vehicle connectivity is growing. While only about half of the vehicles on the road today utilize the technology, industry experts predict that 90–95 percent of new vehicles will be Internet-connected by 2030."
> 车载云端互联正在增长——当前约半数上路车辆使用该技术，行业专家预计 2030 年前 90–95% 的新车将联网。

**为什么重要**：2020 年后生产的大量集成了云端服务功能的二手车主们可能在 5–7 年后经历"功能消失"——这不是偶发故障，是产品设计上内建的"联网寿命到点"。汽车行业与科技行业在这里的分歧值得关注：软件和云服务的产品生命周期是 5–10 年，而汽车的物理寿命是 15–20 年以上。
- 原文：[When your vehicle outlives its cloud: What happens next?](https://arstechnica.com/cars/2026/07/when-your-vehicle-outlives-its-cloud-what-happens-next/)

## 📰 快讯

- **FreeInk：开源阅读器全栈项目**：开源电子阅读器综合项目，覆盖固件、SDK 和开源硬件设计（de-link 项目，公开 KiCad 原理图，物料清单～$60 自制 ESP32-S3 阅读器）。固件 CrossPoint Reader 已支持 EPUB 2/3、Calibre Wi-Fi 传输、KOReader 同步、TLS 1.3、10+ 种界面语言，已适配 Xteink X3/X4、M5Paper 等 8+ 种商用开发板。HN 上 297 分热帖。[项目主页](https://freeink.org/)

- **欧盟法院判 VPN 是合法技术工具**：欧洲法院在一桩涉及 Anne Frank 日记版权侵权的案例中指出 VPN 是"合法技术工具"，版权方不能用版权名义禁止使用 VPN 访问数字作品——此判决被广泛认为是版权保护界限的里程碑。[原文](https://www.techradar.com/vpn/vpn-privacy-security/vpns-are-lawful-technical-tools-says-eu-court-in-landmark-anne-frank-copyright-ruling)

- **Apple 法院胜诉，不扫描 iCloud 涉 CSAM 不算违规**：法院裁定 Apple 没有法律义务扫描用户 iCloud 中的 CSAM 内容——但法官在书面意见里明确"不悦地"写的，鼓励立法层面解决平台内容问题。HN 上 292 分热帖。[原文](https://blog.ericgoldman.org/archives/2026/07/apple-defeats-liability-for-not-scanning-icloud-for-csam-but-the-judge-was-not-pleased-amy-v-apple.htm)

- **Tesla Robotaxi 拓展 Florida**：Tesla Robotaxi 服务计划扩展到奥兰多和坦帕，这是该公司在财报周期内的扩展动作之一。[原文](https://www.theverge.com/transportation/2026/07/tesla-robotaxis-orlando-tampa-florida-earnings)

- **Apple 传闻推 Upgrade 租赁到拥有计划**：Apple 传闻将针对 iPhone、Mac 和 iPad 推出"升级计划"——一台设备支付一段时间的租赁费用后归属用户。[原文](https://www.theverge.com/tech/968750/apple-upgrade-program)

- **Twitch 出家长控制：禁止未成年人开播**：Twitch 推出家长控制功能，允许家长阻止青少年开播以及接收 DM。[原文](https://www.theverge.com/tech/968480/twitch-parental-controls-block-streaming-live-dms)

- **美军士兵被推送的 App 含中俄代码**：研究发现一些针对美军士兵的应用程序（如军旅健身、岁月计算类）包含嵌入式的中国和俄罗斯第三方代码，涉及位置数据采集与后端通信。[原文](https://arstechnica.com/security/2026/07/apps-targeted-at-us-troops-contain-chinese-and-russian-code/)

## 📖 今日英语

1. **antitrust**（反垄断的）：出自司法 ruling *"can presume the proposed merger is likely to violate antitrust laws"*。指禁止企业通过合并或市场行为破坏市场竞争的法律领域。常见搭配：*antitrust lawsuit, antitrust violations, antitrust regulators*。

2. **concentration**（集中度）：出自反垄断判决中提到的 *"undue market concentration"*。经济学和反垄断常用，指少数企业在某市场上份额过高——通过 HHI 指数量化。

3. **obsolescence**（过时 / 废弃）：出自 Ars Technica 车联网文章 *"time ultimately kills cloud-based vehicle services... obsolescence challenges"*。名词，指产品或技术因不兼容新环境或支持结束而被淘汰的过程。常见短语 *planned obsolescence*（计划性淘汰）。

4. **perpetual-license**（永久许可）：出自 Ars Technica *"TreeSize won't renew perpetual-license support unless users subscribe"*。指用户购买的"一次性付款、永久可用"的软件授权，与"订阅式许可"（subscription license）相对。软件行业商业模式正从永久许可向订阅迁移——TreeSize 这一动作正是典型代表。

5. **landmark**（里程碑式的）：出自"landmark copyright ruling"——版权里程碑判决。修饰法律判例，表示判决对未来同类案有重大先例效应，一个里程碑事件会改变行业方向。也用于"landmark achievement"等正向表达。