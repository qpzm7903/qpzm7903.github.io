---
title: "🌐 科技日报 | 2026-07-29"
date: 2026-07-29T06:36:58+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 欧盟公民倡议要求：年龄验证不能变成永久在线身份层

英文原标题：[Stop Killing The Internet: No Digital ID & No Age Verification](https://citizens-initiative.europa.eu/initiatives/details/2026/000011_en)

欧盟委员会登记页面显示，一项新的欧洲公民倡议要求为数字身份和在线年龄验证划出更严格的隐私边界。组织者并非反对保护未成年人，而是要求访问合法内容时，身份和年龄确认必须保持自愿、必要、成比例且有法律依据。技术方案应优先支持匿名或假名式年龄证明，只披露“是否达到年龄门槛”，而不交出姓名、完整生日和可跨站关联的身份。倡议还要求数据最小化、选择性披露、开放标准、可公开审计的密码协议、独立安全与基本权利审计，并禁止依赖方跨服务追踪。没有数字钱包的人必须获得功能等价的替代方式，技术细则也应接受议会审查。这是已获登记的倡议目标，不等于欧盟已经通过新法；后续仍需募集支持并进入相应程序。它把争论焦点从“要不要验证年龄”推进到“能否验证一个属性而不建立覆盖整个网络的实名层”。

> **原文金句**：“Europe can protect minors without building a permanent online ID layer.”
>
> 中文：欧洲可以在不建立永久在线身份层的情况下保护未成年人。

### Zig 把真实应用的增量重编译压到几十毫秒

英文原标题：[Inside Zig's Incremental Compilation](https://mlugg.co.uk/posts/incremental-compilation-internals/)

Zig 核心团队成员 Matthew Lugg 详细拆解了编译器如何只重做受一次代码修改影响的部分。演示中的像素编辑器首次构建约 5 秒，随后修改只需 50—70 毫秒；一次性能追踪更录得 37 毫秒，其中语义分析、代码生成和链接合计约 1.6 毫秒。前端会缓存每个源文件的 ZIR，并把类型、常量值和函数体拆成分析单元，通过依赖图和源代码哈希找出真正失效的节点。代码生成只为变化函数重新产生机器中间表示；与编译器紧密集成的增量链接器则直接在输出二进制中调整对应区域，并追踪需要重做的重定位。当前主要剩余成本反而是遍历引用图，文章认为这里还有明显优化空间。现实限制也写得很清楚：0.16.0 缺少部分关键链接能力，完整体验更适合 master 分支或未来 0.17.0，目前重点目标还是 x86_64 Linux，且可能存在误报甚至错误编译。它已经从概念验证走到核心团队日用，但还没有到“所有项目默认安全开启”的阶段。

> **原文金句**：“Today, using Zig’s incremental compilation, you can make changes to real, complex applications in a matter of milliseconds.”
>
> 中文：今天，借助 Zig 的增量编译，你可以在数毫秒内完成对真实复杂应用的修改构建。

## 📰 快讯

- **[Apple 宣布结束 iPhone Upgrade Program](https://www.apple.com/shop/iphone/iphone-upgrade-program)**：现有成员可继续支付剩余月供，但旧计划将停止；下一部 iPhone 可改用新的 Apple Upgrade 租赁、运营商优惠、Apple 融资或一次性购买。官方页面没有给出旧计划用户会被自动迁移的承诺，因此具体资格仍需在账户中检查。
- **[SBCL 2.6.7 发布](https://sbcl.org/all-news.html?2.6.7)**：新版加入可从普通 Lisp 定义文档字符串中交互浏览手册的 SB-MANUAL 模块，并支持 `DOCUMENTATION` 的声明文档类型。平台侧新增 ARM64 的 SB-SIMD 与 x86-64 AVX-512 支持，还修复 ARM64 的 `SAP-REF-N` 错误编译和多项类型系统问题。
- **[W3C 回顾 WOFF 1.0，并把下一站指向增量字体传输](https://www.w3.org/blog/2026/woff-1-0-a-milestone-on-w3cs-journey-of-fonts-on-the-web/)**：WOFF 通过无 DRM、可压缩且可测试互操作的折中，让 Web 字体使用率从 2011 年接近零增长到 2020 年约 80%；WOFF2 后来再把文件缩小最高约 40%。当前的 Incremental Font Transfer 目标是只下载页面需要的字体字节，尤其改善中日韩等大字符集语言的首屏延迟。
## 📖 今日英语

- **privacy-preserving** — 欧盟公民倡议原句：“Digital identity and age-assurance systems ... remain voluntary, privacy-preserving and non-discriminatory.” 释义：保护隐私的。为什么值得记：密码学、身份系统和数据治理文件中常与 `data minimisation` 连用。
- **selective disclosure** — 欧盟公民倡议原句：“The legislation should require anonymous or pseudonymous proof-of-age, data minimisation, selective disclosure...” 释义：选择性披露，只证明必要属性而不交出全部身份。为什么值得记：数字凭证和零知识证明讨论中的核心短语。
- **incremental compilation** — Zig 原句：“This feature allows the compiler to detect which individual functions and declarations have changed since a project was last built.” 释义：增量编译。为什么值得记：构建系统语境中强调只处理变化及其依赖，而非全量重来。
- **battle-tested** — Zig 原句：“Both of these optimizations have been enabled by default in Zig for years—they are battle-tested.” 释义：经过长期实战检验的。为什么值得记：比 `tested` 更强调真实生产或复杂负载下的验证。
