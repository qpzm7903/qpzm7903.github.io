---
title: "🌐 科技日报 | 2026-07-19"
date: 2026-07-19T06:41:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

周末科技主线两条：一条是"显示器通过 Windows Update 悄悄装 McAfee 推广弹窗"——把硬件外设强装软件这条隐蔽供应链摆到了桌面，HN 一天 925 分；另一条是开发者社区本周集中冒出的几条小信号——Google 把自己的 Noto 3D emoji 全套开源、Gleam 语言入驻 Tangled、Elixir 官网新设计、ACM 期刊《Bikeshed》专栏作者 PHK 写收官篇。

## ⭐ 今日最值得关注

### LG 显示器通过 Windows Update 静默装软件，连推 McAfee 订阅弹窗 31 次 / 32 次开机

本周 HN 反响最大的一篇硬件新闻报道——[VideoCardz 跟 Gamers Nexus 联合调查](https://videocardz.com/newz/lg-monitors-silently-install-software-through-windows-update-without-user-consent) 揭示：**部分 LG 显示器在通过 DisplayPort / HDMI 接上 Windows PC 时，无需用户同意就会通过 Windows Update 自装一款叫 "LG Monitor App Installer" 的软件**，装上后会反复弹 McAfee 杀毒软件 30 天试用订阅窗口。Gamers Nexus 在他们 LG UltraGear 34GX900A-B 上一口气测了 32 次开机，**31 次弹的是 McAfee 试用、1 次弹的是 LG 自家工具**。

它背后的机制是 **Windows Update 的"设备元数据"通道**——Windows 检测到外设后，会从 Microsoft 服务器拉取设备关联的"扩展组件"和"软件包"自动安装，**不弹出任何同意提示**。Windows 可靠性监视器显示 LG Monitor App Installer 延迟约 1 分钟就被装上。Microsoft Store 列出该应用申请的权限是"互联网访问 + 全系统资源"。

更扰人的是这种行为**不限于新显示器**：Gamers Nexus 也在一台 3 年前买的 LG UltraFine 32UN880-B 上测出同样行为。用户投诉可追溯到 2024 年，但近期投诉数明显增多——表明 LG 扩大了适用型号。Dell 也用同样的通道给 Alienware 显示器自动装 Alienware Command Center。

绕开方法：组策略里启用 **`Computer Configuration → Administrative Templates → System → Device Installation → Prevent automatic download of applications associated with device metadata`** 就能挡——代价是真正有用的官方应用也得手动拉。

这是"外设从 Windows Update 自带供应链"问题上【925 分】在 HN 上拉到本周最高分的原因——它第一次把一个外设厂商把显示器当成"装弹窗口"的具体厂家、具体型号、具体弹窗频次、具体绕过办法全列清。下面这句是 Gamers Nexus 视频标题也被原文引用。

> 原文金句：
> Windows Update first installed LG extension and software component packages. Windows Reliability Monitor showed that LG Monitor App Installer appeared one minute later. The installation did not display a consent prompt or require the user to approve the download.
> （Windows Update 先装 LG 扩展和软件组件包。Windows 可靠性监视器显示 LG Monitor App Installer 在一分钟后被装上——安装过程没有显示任何同意提示，也不需要用户批准下载。）

### Google 把 Noto 3D emoji 全套开源——世界表情日放了一组"沉浸 VR 可以直接用"的资产

[The Verge 报道](https://www.theverge.com/design/967606/google-open-source-3d-emoji) + [Google 博客](https://blog.google/products-and-platforms/platforms/android/noto-3d-emoji/)：作为 7/17 世界表情日（[World Emoji Day](https://worldemojiday.com/)）的一部分，Google 宣布 **Noto Emoji 3D 全套开源**——5 月首次随着 Android 推出，本周把整套 3D 模型放给所有人。

这批 emoji 不少设计问题在 2D 时代不存在——3D 之后"笑脸是一个球体、一个面具、还是一片扁平盘？"都得在建模里给出答案才不会从不同视角看着崩。Google 设计团队在博客里专门讲他们怎么处理的。Google 在文章里点了一个很乐观的使用场景："anyone can use these emoji in immersive VR worlds / 创作者可以用在自己的 VR 场景里"——让 The Verge 作者吐槽"用一堆 emoji 去拼沉浸 VR 世界到底能拼出什么我先想象不出来"。

为什么对你重要：这是少有的大型科技公司把视觉原创资产主动推给公共池——Noto Emoji 系列本来就是 Google 主推的跨平台字体覆盖项目（无表情 = Noto Emoji 兜底），现在 3D 版再开成资产，意味着开发者做 demo / 教学材料 / 商业应用都可以免费用一套经过设计团队评审的 3D emoji，不再要自己建或上 Adobe Stock。配合 [Noto 3D 五月首次发布](https://blog.google/products-and-platforms/platforms/android/noto-3d-emoji/) 当时业界普遍 😬 的反应，这次开源是 Google 做出"反正也流行不起来当个艺术项目算了"的姿态。

## 📰 快讯

- **Elixir 官网改版**：[elixir-lang.org](https://elixir-lang.org/) 推出新设计，HN [142 分](https://news.ycombinator.com/item?id=48958813)。社区反应分化——有些觉得更现代更易读，有些觉得失去了"老派 Erlang 系"的克制感。这种"项目主页改版"在 BEAM 圈一向被讨论很久——因为 Elixir 的"文档 = 教程"立场比一般 PL 强。

- **Gleam 入驻 Tangled**：[tangled.org/gleam.run/gleam](https://tangled.org/gleam.run/gleam) 在 HN [174 分](https://news.ycombinator.com/item?id=48958534)。[Gleam](https://gleam.run/) 是跑在 BEAM 上的现代静态类型函数式语言；[Tangled](https://tangled.org/) 是分布式代码托管平台。Gleam 主仓迁入 Tangled 意味着 BEAM 新语言社区也开始找 GitHub 之外的托管方案——和本月早些时候"ACM / Linux Foundation 倡议联邦代码托管"的大背景同向。

- **PHK《Bikeshed》专栏收官**：[acmqueue: Goodbye, and Thanks for All the Bikesheds](https://queue.acm.org/detail.cfm?id=3818307) 164 分。FreeBSD 核心开发者 [Poul-Henning Kamp](https://en.wikipedia.org/wiki/Poul-Henning_Kamp) 近 20 年前开始写的《Bikeshed》专栏正式停笔，最后一篇谈他对开源软件远景的两个判断——LLM-辅助 code review 和年龄验证是当下 FOSS 里两个最烫手的话题；他认为 LLM code review 影响被严重夸大，"我们看到 LLM 找到的 bug 大爆炸只发生在前几周——之前所有静态分析工具都是一样的模式"。PHK 借收官把自己摆出"未来若被打脸就让我上榜"的位置。

- **Zilog Z80 50 周年**：[goliath32 blog](https://goliath32.com/blog/z80.html) 271 分。Z80 处理器 1976 年 7 月正式发布，到今年 50 年——文章从工业历史、GameBoy 里的衍生架构 Sharp LR35902、[Zilog 自己两年前才停产](https://www.zilog.com/) 原始 Z80、到当前工业应用仍常见的 [eZ80](https://www.zilog.com/) 讲了一条完整工业史。8 位处理器黄金时代的极简 AI 编程课。

- **Regressive JPEGs：渐进式 JPEG 各频段扫一张一图讲清**：[maurycyz.com](https://maurycyz.com/projects/bad_jpeg/) 640 分。一篇挺漂亮的图像工程科普——把一张 JPEG 的 9 个 scan（DC + AC bin 0-5 + 全精度）一次次拆开给你看每个 scan 在补什么数据，让"分频率输入 = 渐进式 JPEG 原理"一次看懂。作者 Maurycy 是常写 codec 短文的工程师。

- **Fubo 涨价 15 美元**：[Ars Technica](https://arstechnica.com/gadgets/2026/07/fubo-hikes-prices-by-15-after-restoring-some-nbcu-channels-lost-in-november/)——美国流媒体 live TV 平台 Fubo 在去年 11 月因与 NBCUniversal 谈判破裂下架一批 NBCU 频道、近期恢复部分频道后**立刻涨月费 15 美元**，是流媒体 live TV 继 YouTube TV / Hulu + Live TV 后今年第二次跟涨。

- **FCC 被指控在 Paramount 合并审批期间收名贵礼物**：[Ars Technica](https://arstechnica.com/tech-policy/2026/07/fcc-took-pricey-gifts-from-paramount-as-the-company-needed-approval-for-deals/)——FCC 在审批 Paramount 与 Skydance 合并期间，相关官员收受了 Paramount 的高价礼物。监管机构独立性问题延续到 2026 年。

## 📖 今日英语

- **device metadata（设备元数据）**
  原句：出处 ⭐ VideoCardz 文章里提到的组策略项 "Prevent automatic download of applications associated with device metadata"——Windows 通过一个外设的元数据识别它需要装什么配套软件。"device metadata" 在 Windows 内部指的是一组藏在注册表和 WSUS 的厂商提供元数据（设备图标、品牌名、配对应用）。

- **consent prompt（同意提示 / 许可弹窗）**
  原句：出处 ⭐ "The installation did not display a consent prompt or require the user to approve the download"——consent prompt 在欧美 privacy / 合规章程里是高频术语，GDPR 和 CCPA 都要求"明示同意"前必须有一个 consent prompt 出现。无 consent prompt = 默示同意（implied consent），在很多司法案例里不被认。

- **pass the eye test（经受粗看考验 / 看上去 OK）**
  原句：出处 ⭐ Phillip Kerger 凸优化文章 "producing things that pass the eye test for being correct while being utter nonsense"——英文常用短语，指"乍看下能糊弄过去"。在科技英语里也常作 "it passes the smell test"（"smell test" 来自"闻一下察觉味道不对"，和 eye test 意思几乎一样）。

- **so loud / quiet**（行业动静的大小）
  原句：出处 📰 PHK《Bikeshed》收官篇 "the LLM-assisted code reviews are causing a lot of headlines because this comes out of one of those economic bubbles that seem to automatically inflate as soon as most people have forgotten how utterly stupid and predictable the previous bubble was"——"causing a lot of headlines" 是英文里指"被媒体炒作得很响"的固定搭配，常带贬义。"stupid and predictable" 是技术圈老炮写收官文的常见语气。

- **monopoly on attention（独占注意力的渠道）**
  原句：出处 📰 PHK 专栏 "FOSS 在远未来预测里值得关注的两件事" 一段——指媒体平台把读者注意力锁住。这个词在科技评论里越来越常出现，配合 attention economy（注意力经济）使用。