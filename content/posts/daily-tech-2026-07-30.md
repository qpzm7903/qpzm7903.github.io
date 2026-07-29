---
title: "科技日报 2026-07-30"
date: 2026-07-30T06:39:03+08:00
draft: false
tags: ["科技", "软件", "硬件", "日报"]
categories: ["日报"]
summary: "微软 FY26 收官季度云业务继续扩张；Google Play 年龄信号 API 将全球开放；Swift 团队解释语言的安全、性能与互操作设计；Keychron 回顾定制键盘开放生态。"
---

## 今日要闻

### 1. 微软 FY26 Q4：Azure 增长 39%，资本开支继续抬升

微软公布截至 2026 年 6 月 30 日的第四财季：营收 764 亿美元、同比增长 18%，营业利润 349 亿美元、增长 23%。Microsoft Cloud 营收 514 亿美元、增长 26%，Azure 与其他云服务收入增长 39%。

公司同时披露年度营收 2,817 亿美元、年度营业利润 1,285 亿美元。季度资本开支约 300 亿美元，主要投向云和 AI 基础设施；这说明需求仍强，也意味着折旧、供电和数据中心利用率会继续影响后续利润结构。

[微软官方 FY26 Q4 业绩材料](https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q4/press-release-webcast)

### 2. Google Play Age Signals API 将向全球开发者开放

Google 宣布把 Play Age Signals API 扩展到全球所有 Play 开发者。该接口让家长通过 Family Link 选择是否把孩子的年龄段（例如 16—17 岁）分享给使用该 API 的应用；年龄段默认不共享，家长可随时修改或关闭。成年用户也可在应用请求时自行分享年龄。

Google 计划 8 月中旬先扩展到澳大利亚和加拿大，随后在今年晚些时候覆盖全球用户。开发者获得的是用于调整内容、功能和安全设置的年龄信号，而不是统一强制的“一刀切”规则。

[Android Developers 官方博客](https://android-developers.googleblog.com/2026/07/google-play-age-signals-api-safer-experiences.html)

### 3. Swift 团队解释：一门“伟大语言”如何平衡安全、性能与互操作

Swift 官方博客回顾语言设计目标：默认内存安全、值语义、可预测性能与渐进式互操作必须同时成立，而不是用运行时开销换取所有安全保证。文章强调所有权、借用、并发隔离等特性正逐步把更多错误前移到编译期，同时保留与 C、C++、Objective-C 生态协作的现实路径。

这篇文章不是版本发布，而是一份设计原则说明。它帮助开发者理解 Swift 近年的语言演进为何围绕数据竞争安全、非拷贝类型和跨语言互操作展开，也解释了“易学”和“系统级性能”之间并非只能二选一。

[Swift 官方博客](https://www.swift.org/blog/Swift-is-a-great-language/)

### 4. Keychron 回顾定制机械键盘：开放固件把硬件变成平台

Keychron 的长文梳理定制机械键盘从小众套件走向大众产品的路径。除了热插拔轴体、可替换键帽、铝制外壳和布局选择，真正改变生态的是 QMK / VIA 一类开放固件：用户可以重映射按键、配置层、宏和旋钮，而不必被单一厂商软件锁定。

对硬件行业而言，这种模式把一次性消费品变成可长期维护的平台。设计竞争也从“堆轴体和灯效”转向结构、声学、固件兼容和社区配件，降低了小团队做差异化产品的门槛。

[Keychron 原文](https://www.keychron.com/blogs/news/the-rise-of-the-custom-mechanical-keyboard-experience)

## 概念速查

- **[大语言模型（LLM）](/concepts/large-language-model/)**：微软财报中的云与基础设施投入为何持续增长，可从模型训练和推理的算力需求理解。
- **[Transformer](/concepts/transformer/)**：现代生成式模型的主流基础架构，也是云厂商扩建 AI 集群的重要需求来源。

## 编辑备注

已剔除 AI 模型发布、AI 功能测评和消费导购；微软条目聚焦云业务与基础设施，Google、Swift、Keychron 均回溯到主体官方页面。所列 URL 未在最近日报中出现。
