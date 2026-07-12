---
title: "🌐 科技日报 | 2026-07-13"
date: 2026-07-13T06:45:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. Chrome 148 起 `Math.tanh` 能泄露操作系统：anti-bot 系统的新指纹信号

Scrapfly 的工程师在 HN 上以 125 分 / 49 评论引发关注——这是过去一两年"反爬虫 vs 反反爬虫"里非常有意思的一个新切面。核心发现：

一个 `Math.tanh(0.8)` 调用在 Linux Chrome 上返回 `0.6640367702678491`，在 macOS Chrome 上返回 `0.664036770267849`（少一位），在 Windows Chrome 上返回 `0.6640367702678489`——同一个浏览器、同一个版本、同样的硬件架构会随操作系统给出的 libm 实现不同得到**不同最低位**的值。一行 `Math.tanh` 调用 + 一张平台对规则表 = 一份不可伪造的 OS 指纹。

为什么会变？直到 Chrome 147，V8 用自带的 `fdlibm` 端口（相同结果在所有平台），Chrome 148 commit `c1486295ae5` 改成了 `std::tanh`——读操作系统的 `libm`。Linux 用 glibc、macOS 用 Apple 的 `libsystem_m`、Windows 用 UCRT，三家在不能正确舍入的函数上有各自的 trade-off。`Math.tanh` 是 V8 直接调 `std::tanh` 的一个，所以独独这一个 `Math.*` 函数泄露 OS；其它的 `Math.exp`、`Math.sin`、`Math.cos` 仍走 V8 自带实现，故意伪造 OS 反而会暴露不一致。

**为什么重要**：

这对 Web/anti-bot 工程师是一个直接影响生产的发现：User-Agent 声称用 macOS 但 `Math.tanh(0.8)` 返回 Linux 的 bit pattern = 自动矛盾。论文里说的 "一个 tanh 调用 + 一张 OS 对照表 = 一份操作系统签名"——用起来极轻量，检测器根本不需要等 canvas fingerprint、WebGL fingerprint 那些传统、同时间明显更贵的信号。对做 browser spoofing、datacenter proxy、scraper 的工程师，这是一条新的"反向约束"：你必须让被驱动的浏览器调用宿主 OS 的 `libm`，而伪造 libm 远比伪造 User-Agent 难。

- 原文：[Your Browser Does Math Differently on Every OS, and Anti-Bot Systems Read the Bits](https://scrapfly.dev/posts/browser-math-os-fingerprint/)

### 2. 爱尔兰数据中心现在"喝掉"全国 23% 的电：一个微型国家级 AI 基建的极端案例

The Register 报道了爱尔兰中央统计局（CSO）的最新数据：2025 年爱尔兰数据中心耗电 7,663 GWh，比 2024 年增长 10%，占全国计量用电的 **23%**——超过城市家庭用电（18%），是农村家庭用电（9%）的两倍多。值得注意的是，这个增长发生在都柏林地区对新建数据中心电网接入的"有效禁令"延续几乎整个 2025 年期间——禁令直到 2025 年 12 月才解除。

为什么 AI 时代这项数据会让工程师需要关注：

- 一个国家不到 550 万人口却容纳了 80 多个数据中心——爱尔兰因为低企业税 + 英语 + 直连北美光缆成了 hyperscaler 在欧洲的桥头堡，所以"AI 基建需求 × 电力基础设施供给"冲突在这里先演了一遍。
- 关键的后续约束已落地：新规要求**任何超过 10 MW 的数据中心电网接入必须自带发电或电池系统，按命令向国家电网倒送电**——一个数据中心不再仅仅是电力消费者，要成为备用电力提供方。微软、Digital Realty 等在都柏林已开始试点"grid-interactive"数据中心——这给"AI 公司到处找电"的全球趋势做了一个微缩模板。

[The Verge 的同题报道](https://www.theverge.com/column/963346/ai-data-centers-fight) 也在周末被广泛讨论——"反对 AI 数据中心的战斗才刚开始"，预兆这种地政经冲突会从爱尔兰散到其他 hyperscaler 站点所在国家。

- 原文：[Irish datacenters now guzzle 23% of the country's electricity](https://www.theregister.com/on-prem/2026/07/11/irish-datacenters-now-guzzle-23-of-the-countrys-electricity/5270013)
- 相关：[The fight against AI data centers is just beginning](https://www.theverge.com/column/963346/ai-data-centers-fight)

---

## 📰 快讯

### Ghostel.el：把 libghostty 嵌进 Emacs 的终端模拟器

HN 254 分 / 47 评论的项目，作者给 Emacs 写了一个用 [Ghostty](https://ghostty.org/) 的 C 库 libghostty 做后端的终端模拟器。Ghostty 自己是一个独立高性能终端，但作者认为 Emacs 用户希望能"在 Emacs 里拥有一个真终端"而不是用 shell-mode 模拟。Ghostel 用 native module 桥接 libghostty，支持多种 [输入模式](https://dakra.github.io/ghostel/#input-modes)（semi-char、char、Emacs、copy 等），有完整的 shell 集成、scrollback 搜索、鼠标选择。如果你的工作流需要在 Emacs 里同窗口跑真 shell 命令而不是 ansi-term，这个 1 人项目值得试。

- 原文：[Ghostel.el: Terminal emulator powered by libghostty](https://dakra.github.io/ghostel/)

### 三星电子将龙仁首座芯片厂投产提前至 2029 年，比原计划提前 1~2 年

据华尔街见闻报道，三星决定将韩国龙仁半导体集群首座工厂的投产时间从原计划提前到 2029 年——比原计划早 1~2 年。该厂区是三星史上最大单笔投资的核心部分，承担下一代存储与逻辑芯片产能。提前投产的背景是 AI 内存需求（HBM）供不应求、SK 海力士刚创下史上最大海外赴美 IPO，以及台积电 2nm 与封装上的领先格局。对供应链读者，这是一个三星"加速多年布局的项目到实际产能对接时间"的关键节点——意味着 2029 起 HBM 与先进逻辑产能全球供应格局可能出现大幅供应方变化。

- 来源：[华尔街见闻](https://wallstreetcn.com/articles/3776715)

### 全球市场步入"动荡之夏"：美联储变局 + 日元危机 + 财报季大考

华尔街见闻周末综述了过去 24h 的宏观格局：伊朗关闭霍尔木兹海峡后美军对伊发动新一轮袭击，布什尔、阿萨卢耶等地传爆炸声；下周（7 月 14~18 日）重磅日程紧凑：**中国 Q2 GDP、美国 CPI、美联储主席沃什半年度听证会、WAIC 大会、台积电财报**。并预告了"动荡之夏"的三大考题：美联储变局、日元危机、财报季大考。对 ens 仍在消化 SK 海力士 IPO + 算力恐慌的市场，这是一份把握未来一周节奏的关键时间表。

- 来源：[华尔街见闻](https://wallstreetcn.com/articles/3776710) ｜ [全球市场动荡之夏综述](https://wallstreetcn.com/articles/3776706)

---

## 📖 今日英语

**fingerprint** — "Fingerprinting is usually about canvas, WebGL, fonts, audio. There is a quieter signal, and it lives in the last bits of a number."（出处：Scrapfly 文章原文）
"指纹"——浏览器 / 在线追踪语境里指一组能唯一标识你设备的特征。浏览器指纹不靠 cookie，只靠设备在执行时的物理特性。常见搭配：browser fingerprint、device fingerprint、canvas fingerprint。反爬虫和 anti-bot 工程师的核心专业词汇。

**ULP** — "three implementations, three sets of bits: Linux (glibc), macOS (Apple libsystem_m), Windows (UCRT) ... split just often enough to classify the OS. ... usually by one unit in the last place (1 ULP)."（出处：Scrapfly 文章原文）
"Unit in the Last Place / 最低位差异" ——浮点数精度术语，指两个相邻浮点数之间的距离。一个 ULP 的差异就是"最低位差 1"，这是浮点计算能达到的最小精度差。是本项目整个发现的技术基础——不同 OS 的 libm 实现在 1 个 ULP 范围内会选不同方向舍入。常见搭配：1 ULP、2 ULP spread、ULP tolerance。

**moratorium** — "The Commission for Regulation of Utilities (CRU) put an effective moratorium on connecting new server farms to the electricity grid."（出处：The Register 爱尔兰数据中心文章原文）
"暂停 / 禁令"——政府或监管机构对某事发出的临时禁令，通常用于争取时间评估风险。爱尔兰对新建数据中心电网接入的 moratorium 就是一个典型例子。常见搭配：moratorium on、declare a moratorium、lift the moratorium。

**guzzle** — "Irish datacenters now guzzle 23% of the country's electricity."（出处：The Register 文章标题）
"大口吞食 / 大量消耗"——动词，比 consume 更具口语色彩、更有"什么都很能消耗"的意味。媒体标题里常用，用来形容资源消耗夸张的设施。常见搭配：guzzle electricity/fuel、gas guzzler（油老虎）。非正式用词，但表达力强。

**pre** / **post market** — "hasPrePostMarketData": false（出处：Yahoo Finance 指数 API 返回结构）
"盘前 / 盘后交易时段"——美股正式交易时间 9:30–16:00 ET 之外的延伸交易时段：盘前 4:00–9:30、盘后 16:00–20:00。财报和重大消息通常在盘后发布以避免交易时间直接冲击。常见搭配：pre-market trading、post-market move、after-hours。财经新闻高频词汇。