---
title: "🌐 科技日报 | 2026-07-15"
date: 2026-07-15T07:49:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. 微软 Secure Boot 被破解了 13 年——11 个被遗忘的 UEFI shim 从未撤销，新手黑客就能绕过

安全公司 ESET 发现了 11 个固件镜像（shim），有些可以追溯到 2013 年——已知有漏洞但仍被微软签名且从未撤销。这意味着过去 14 年中，Secure Boot 有 13 年处于"可被轻松绕过"的状态。这不是什么精巧高级的零日漏洞：ESET 研究员 Martin Smolár 明确说"不需要新漏洞，不需要复杂的利用原语——只需要一份旧的、仍被信任的、但未被撤销的 shim 二进制文件，加上对 UEFI shim 的基本理解就够了。"

关键信息：

- **shim 是什么**：为了让 Secure Boot 同时支持 Linux，社区发明了"shim"——微软用另一枚 UEFI 证书签名的二级信任锚。shim 内嵌的证书授权后续所有引导加载器和工具软件。shim 有漏洞时微软应撤销它，但这 11 个 shim 被遗忘了。有些存在了超过十年。
- **影响范围**：Windows 和 Linux 设备都受影响。攻击者只要有短暂的物理访问（甚至在关机状态下），就能安装 bootkit 恶意固件——在操作系统加载早期运行、重装系统和更换硬盘都不会消除。
- **微软终于行动了**：在 ESET 把问题提交给 CERT 和微软后，微软在上个月的月度补丁中撤销了这些 shim。但微软至今没有解释这一失察是如何发生的。可能的原因：Secure Boot 的撤销机制（dbx 数据库仅 32KB，无法逐一列出所有组件哈希）极其复杂，微软已转向 SBAT 和 SVN 版本号撤销——但显然遗漏了这些老 shim。
- **对谁重要**：任何依赖 Secure Boot 保护的 Windows 或 Linux 用户。安装了 6 月补丁的 Windows 用户已不再受影响；Linux 用户应检查 Linux Vendor Firmware Service（fwupd.org）或咨询发行商。Windows 11 Secured-core PC 在默认状态下可能不受影响。

> 原文金句：「What makes these old shims dangerous is not a novel vulnerability... It's that no new vulnerability is needed to bypass UEFI Secure Boot. An attacker needs no complicated exploitation primitives—only a copy of an old, still-trusted, but un-revoked shim binary and a basic understanding of how UEFI shims work.」

"让这些旧 shim 危险的不是什么新漏洞……绕过 UEFI Secure Boot 根本不需要新漏洞。攻击者不需要复杂的利用技法——只需要一份旧的、仍被信任的、但未被撤销的 shim 二进制文件，加上对 UEFI shim 如何工作的基本理解。"

- 原文：[Microsoft's Secure Boot has been broken for a decade and no one noticed until now](https://arstechnica.com/security/2026/07/microsoft-secure-boot-has-been-broken-for-most-of-its-existence/)
- ESET 研究：[Forgotten UEFI shims undermining Secure Boot](https://www.welivesecurity.com/en/eset-research/forgotten-uefi-shims-undermining-secure-boot/)

### 2. Boston Dynamics 让 Spot 机器狗送货：一条传送带加 $74,500 的四足机器人能找到你家前门吗？

Boston Dynamics 正在测试让四足机器人 Spot 执行最后一英里配送——从货车卸包裹并自主放到客户家门口。一个新增的传送带配件让 Spot 能背多件包裹、用短传送带卸货。

核心看点：

- **为什么不用车轮或无人机**：已有轮式机器人或空中无人机尝试配送，但人类仍是从卡车到家门口最"全能"的送货者——因为楼梯、不平的通道各种障碍。Spot 擅长攀爬不平地面和跨越复杂障碍（已在搜救和庞贝古城巡查中验证），这些能力恰好适合"从马路到家门口"的非结构化郊区环境。
- **成本问题**：Spot 单台约 $74,500，要替代人类快递员的效率需要相当大的单量才能回本。Boston Dynamics 表示"已在与主要物流公司洽谈测试 Spot 作为最后一英里配送方案"，但目前只是从演示推进到试点。
- **商业逻辑**：不是让 Spot 取代快递员全程，而是让司机留在车上操作，Spot 专门跑家门口这一段——这是劳动密集度最高、最容易被自动化优化的环节。

> 原文金句：「Can a $74,500 Spot robot find your front door?」

"一台 74,500 美元的 Spot 机器狗能找到你家的前门吗？"

- 原文：[Boston Dynamics tries using 'robot dogs' for deliveries](https://www.theverge.com/tech/965378/boston-dynamics-spot-robot-dog-delivery-assistant)

---

## 📰 快讯

### 谷歌图片搜索 25 周年改版：兴趣驱动的画廊 + 更多 AI 参与

谷歌庆祝图片搜索 25 周年（起源可追溯到 2000 年 Jennifer Lopez 在格莱美上的那条绿色 Versace 礼服——人们搜它的图片不想读文章只想看照片）。新版将在搜索前就展示基于个人兴趣（浏览和搜索历史）自动更新的图片画廊，并进一步融入 AI 元素。目前 images.google.com 极简（仅有搜索栏），改版后体验更接近个性化推荐。

- 原文：[Google revamps image search for its 25th anniversary with more images and more AI](https://arstechnica.com/google/2026/07/google-revamps-image-search-for-its-25th-anniversary-with-more-images-and-more-ai)

### Windows 11 大补丁：允许无限期暂停更新

微软发布 7 月 Patch Tuesday 大补丁，其中包含一项新功能：用户可无限期暂停更新。此前 Windows 11 只允许暂停 5 周。此外补丁还修复了开始菜单崩溃、改善文件资源管理器性能，并整合了前一版被回滚的更改。这是微软"重建用户信任"系列的延续。

- 原文：[Windows 11's big patch Tuesday allows you to hold off on updates for longer](https://www.theverge.com/tech/965643/microsoft-windows-11-july-2026-patch-tuesday-updates)

### 可穿戴生物传感器新方向：导电墨水"电子纹身"直接画在皮肤上

研究人员开发出将导电墨水直接画在皮肤上、干燥后变成可工作电极的技术。彩色自定义设计的"电子纹身"可用作可穿戴生物传感器——监测心率、肌电图、脑电图等生理信号，比传统贴片更舒适、更个性化。墨水含有生物相容性导电聚合物，干燥后可保持功能数小时。

- 原文：[These painted e-tattoos could be the future of wearable biosensors](https://arstechnica.com/science/2026/07/these-painted-e-tattoos-could-be-the-future-of-wearable-biosensors/)

### Plex 服务大规模中断：用户无法流媒体播放

Plex 周二遭遇大范围服务问题，用户反映无法远程播放电影和电视剧。自建 Plex 服务器（在用户本地或 NAS 上运行）的流媒体功能受影响——本地网络播放仍正常，但 Plex Relay/Plex Cloud 路由不可用。Plex 团队确认正在修复。

- 原文：[Plex problems prevented users from streaming movies and shows](https://www.theverge.com/tech/965518/plex-tv-down-outage-issues)

### HN 高热帖：「你的 App 其实可以只是一个网页」（682 分）

开发者 Dan Q. 发文指出大量 Electron 应用和独立 app 完全可以用普通网页实现——他做了一个工具把你能想到的"本应是网页"的 app 直接打回网页版。HN 上 682 分引发热烈讨论，核心争论点：渐进式 Web App（PWA）是否真的已足够强大到替代 Electron，还是原生桌面应用仍有 PWA 无法覆盖的能力。

- 原文：[Your 'app' could have been a webpage (so I fixed it for you)](https://danq.me/2026/07/09/your-app-could-have-been-a-webpage/)

---

## 📖 今日英语

**shim** — "The images are known as shims, which were invented to extend Secure Boot to Linux devices and utility software."（出处：Ars Technica Secure Boot 报道）

"垫片 / shim 程序"——在系统软件中，指插入两个不兼容接口之间的薄层适配代码，让原来的组件能协同工作。Secure Boot 本为 Windows 设计，Linux 通过 shim 获得兼容支持。这个词在嵌入式、驱动开发、UEFI 模块中高频出现。常见搭配：install a shim、compatibility shim、UEFI shim。比喻义也常见：a shim between two APIs。

**revocation** — "Microsoft finally revoked them in its regular monthly patch release, after ESET brought them to CERT's and Microsoft's attention."（出处：同上）

"撤销 / 废止"——在安全语境中指签名机构宣布某个证书、二进制或密钥不再被信任，系统应拒绝让它运行。与"签发"（signing/issuing）相对。今天故事的荒诞之处正是——微软签发了 shim 却忘了 revoke 漏洞版本，让它们继续被信任了十年。常见搭配：certificate revocation、revocation list、revoke a key。

**last-mile delivery** — "Boston Dynamics says it's 'already in talks with major logistics companies about testing Spot for a last-mile delivery solution'."（出处：The Verge Boston Dynamics 报道）

"最后一英里配送"——物流行业核心术语，指货物从最后一个分拣中心到最终收件人手中这一段。是整个配送链中成本最高、效率最低、最难自动化的环节——因为路径复杂、收件人分散、需应对楼梯/门铃/签收等非结构化场景。Spot 机器狗的试水正是针对这一段。常见搭配：last-mile logistics、last-mile solution、solve the last-mile problem。

**unstructured environment** — "Spot's unique ability to clamber over uneven terrain and navigate complicated obstacles could make it well suited for navigating the 'unstructured environments of suburban neighborhoods.'"（出处：同上）

"非结构化环境"——机器人学术语，指没有明确标记、规则不固定、环境动态变化的空间。与之相对的是"结构化环境"（如工厂流水线，路径和障碍都预先设定）。郊区住宅区是典型的非结构化环境——每户的台阶、草坪、栅栏、宠物都不同。Spot 之所以选用于配送，正因为它的四足行走在非结构化环境中优于轮式机器人。常见搭配：navigate unstructured environments、unstructured vs structured、unstructured terrain。

**palette** — "The new Google image search will use your 'unique interests' to create an always-updated gallery."（出处：Ars Technica Google Images 25 周年报道）

"调色板 / 选择范围"——在产品语境中，palette 不只是画家用的调色板，更常指"提供给用户的选择范围"或"可用选项的组合"。Google Images 改版后根据你的兴趣画像为你构建一个"不断更新的图片画廊"，本质上是在从全网图片里为你定制一个 palette。常见搭配：color palette、product palette、palette of options。