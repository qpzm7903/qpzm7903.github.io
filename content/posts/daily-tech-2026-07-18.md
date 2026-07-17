---
title: "🌐 科技日报 | 2026-07-18"
date: 2026-07-18T06:42:00+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

今天科技主线两条：一条是"工人 vs 人形机器人"延烧到制造业一线、首次因机器人停工整厂；另一条是 SQLite 在独立开发者站点继续"逆流"——一个 4 年跑满的 Mess with DNS 把它从 Postgres 切过、一个 11 年老站 Lobste.rs 这周也跟上。

## ⭐ 今日最值得关注

### 现代汽车蔚山厂因"部署 25,000 台 Atlas 人形机器人"罢工——业界首次因人形机器人停工

现代汽车位于韩国蔚山的汽车综合体本周部分罢工，工会 15 轮谈判破裂后，工人从 7/13 到 7/15 每个早晚班提前两小时下班，7/20–22 计划升级为四小时罢工。这是**业界首次因人形机器人部署停工停产**，被《华尔街日报》指出"汽车行业首例"。

罢工是围绕现代集团宣布的机器人路线图：旗下 Boston Dynamics 即将成为**全资子公司**（从 SoftBank 收购），同时公布将部署 **25,000 台 Atlas 人形机器人**到现代和起亚工厂——从 **2028 年开始，先在美国工厂落地**，乔治亚州萨凡纳外的 Metaplant America 是首发点，新一代 Atlas 身高 >6 英尺、可举 >100 磅。这台机器人单台估算 **$130,000**，2 年回本（三星证券估算）；若降至 $100,000，运营成本可低于美国联邦最低工资 $7.25/小时，比一名汽车工人的工资还低。

工会开出三条诉求：把计时换成**固定月薪**（避免自动化缩短工时直接砍工资）、把退休年龄从 60 提高到 65、加发工龄奖金。同期美国这边 UAW 在底特律宪法大会上警告"人形机器人和大规模自动化威胁工人就业和薪酬"，近期还批评通用在旗舰 EV 工厂裁员 1,300 后立刻装 50 套新机械臂。[原文：ars technica](https://arstechnica.com/ai/2026/07/fear-of-humanoid-robots-spurs-human-workers-to-strike-at-hyundai-auto-factory/)

为什么对你重要：这是 2026 年最值得跟踪的一个商业-劳工拐点。人形机器人从"PPT 和测评视频"走到工厂一线、第一次让工会把"机器人 vs 人"摆到谈判桌上。如果 Atlas 这种人形机在 2028 年 Metaplant 按计划落地、能真正替代部分工位，蓝领工人待遇谈判、最低工资立法都会被重新定价。

> 原文金句：
> Hyundai aims to deploy more than 25,000 Atlas robots across various Hyundai and Kia manufacturing plants. It plans to start with its US factories in 2028 ... Each Atlas robot costs an estimated $130,000 but may pay for itself within about two years of operations.
> （现代计划在现代、起亚各工厂部署超过 25,000 台 Atlas 机器人，2028 年从美国工厂起跑……每台 Atlas 造价约 13 万美元，两年就能回本。）

### "Frame"：一个用纯汇编写成、2 万行的 Linux X server——作者用电池当动力

HN 上一篇文章 [Frame](https://github.com/isene/frame) 拿到 124 分：作者 Kim Isene 把自己 Linux 桌面的 X server 从 X11（400 万行 C）换成了自己**用汇编**写的版本，只有约 20,000 行。X11 的替代堆栈（gdm + X11 + i3 + conky + wezterm + zsh）合计 5000 万行以上，作者完全自造的 CHasm 工具链合计约 100,000 行——**五十分之一**。[原帖](https://isene.org/2026/07/Frame.html)。

动机很特别：作者明确说**电池续航**是主要动力之一。"我不确定这台笔记本还有没有风扇——除了我之外。"闲置时测量 Xorg 的 CPU 消耗几乎是 frame 的 3 倍，窗口管理器 tile 和终端 glass 在三分钟里 **CPU use 0 毫秒**。

合理评价这条：这是一个绝不打算普适化的"一人栈"——作者在文末承认"为大众设计的软件让每个人沾一点边；这版只精确地服务一个人"。意义在于两点：一是把"二进制代码可读、易优化增长"推到一个清晰的极端（"no dependencies、no hot paths、no unnecessary wakeups"），是当前 ln 尚书崇尚的**库最小化运动**的汇编版；二是说**在 AI Coding 给力的当下**，作者提到自己直接用 Claude Code 来描述需求 → AI 教他写 frame，把"把硬件层、cursor painting、GPU handoff 等冷知识"按需学通。

> 原文金句：
> No dependencies, no libraries, no garbage collector. No hot paths, no unnecessary wakeups. When it is idle, it sits still. It shuts up unless spoken to. My kind of software.
> （没有依赖、没有库、没有垃圾回收。没有热点路径、没有无谓唤醒。空闲时它就安静地坐着，除非被叫到，否则一声不吭。我喜欢的软件。）

## 📰 快讯

- **Lobste.rs 也迁到 SQLite**：11 年老技术社区 [Lobsters 本周上线 SQLite 版本](https://lobste.rs/s/ko1ji1)。同期 [Julia Evans（jvns）专门写了一篇"运行 SQLite 学到的几件小事"](https://jvns.ca/blog/2026/07/17/learning-about-running-sqlite/)——核心提醒是**"即便配 SQLite 也要会运维"**：她用 Django + SQLite 做小项目，一条 FTS5 全文检索 5 秒不返回，最后发现是**没跑 `ANALYZE` 收集统计信息**让查询计划器瞎猜，跑完查询 5s → 0.05s。同时她在批量 `DELETE` 时撞到了 SQLite **单一 writer** 限制——其他 worker 5 秒拿不到写锁就崩溃，唯有小批量删。
- **苹果音乐涨价**：[Apple Music 调高订阅价](https://www.theverge.com/tech/967379/apple-music-price-increase)，The Verge 没给调幅，但位置和定价层级一致表明 Apple 站在 Spotify 涨价潮一侧跟 PLEX 牌价。[The Verge 报道](https://www.theverge.com/tech/967379/apple-music-price-increase)。
- **三星 Galaxy Z Fold 8 设计 leak**：[The Verge 曝光折叠系列新设计图](https://www.theverge.com/tech/967198/samsung-galaxy-z-fold-8-images-specs-leak)，_fold 8 突然加入"宽屏"意味着三星折叠线第一次正面跟 Pixel 9 Pro Fold 和国产品对话折叠生态的"主屏尺寸"标准跟齐。
- **Chip Motors 推可自动泊车低速 EV**：[The Verge 评测新闻](https://www.theverge.com/transportation/966498/chip-motors-low-speed-ev-remote-park-price) "qu亡的 Jeep 风格电动车"——主打能自己泊入位、低速街速 cc，是 GNU 以来最有意思的一类 LSV（low-speed vehicle）新创业路径。
- **谷歌投资的野火探测卫星发射**：[Ars Technica 报道](https://arstechnica.com/space/2026/07/google-backed-satellites-for-wildfire-detection-launch-as-smoke-chokes-us-canada/)——加拿大/美国 smoke 抽风之际，Google 系卫星首次搭载专用的红外/多光谱传感器做近实时野火检测，可提供分钟级早期告警。
- **旧金山要求 Apple/Google 下架 nudify 应用**：[SF 检察长下令](https://arstechnica.com/tech-policy/2026/07/apple-google-must-stop-profiting-off-ai-nudify-apps-san-francisco-ag-says/)——指出 Apple/Google 仍在从 "AI 脱衣" 类应用抽成，要求其下架。这是州/市级 AG 第一次具体点名 App Store 对 AI 生成色情的审核义务。
- **FCC 被指控向 Paramount 收昂贵礼物**：[Ars Technica](https://arstechnica.com/tech-policy/2026/07/fcc-took-pricey-gifts-from-paramount-as-the-company-needed-approval-for-deals/)——在 Paramount Skydance 合并审批期间，FCC 官员收受高价礼物。机构独立性争议延续到 2026。
- **SpaceX Starship 发射中止**：[因部分发动机未启动](https://arstechnica.com/space/2026/07/spacex-scrubs-starship-launch-after-some-of-its-engines-didnt-start/)——7/17 静态点火后中止，机组未受影响，发射窗口延期。
- **HP 印度被罚 14 亿卢比（约 1.65 亿美元）**：[ Ars Technica 报道](https://arstechnica.com/gadgets/2026/07/hp-fined-1-4-billion-rupees-for-cartelization-of-ink-cartridges-toner-pcs/)——印度竞争监管机构判 HP 因喷墨+激光打印机+PC "cartelization（串通定价）"违规。
- **T-Mobile 强制套餐迁移失误**：[部分用户免费号被取消](https://arstechnica.com/tech-policy/2026/07/t-mobile-bungled-forced-plan-migration-canceling-some-users-free-lines/)——运营错误风波续；老用户免费贴现线被吞。

## 📖 今日英语

- **hindsight**（事后瞻 / 后见之明）
  原句：出处 ⭐ Frame 一文以及今天的论文日报都出现——"hindsight" 是英文里形容 "事后看 / 原本以为" 一个**极常用、极克制**用词，"hindsight is 20/20" 是俚语，意思 "事后看当然清楚"。

- **idle**（空闲的 / 挂机的）
  原句：出处 ⭐ Frame 一文："When it is idle, it sits still. It shuts up unless spoken to." — idle 在软件工程里指进程没有任务时的状态。idle / hot path / busy loop 是常配对出现的术语。

- **string theory of running**（运行 SQL 的弦理论）
  原句：（玩笑关联，非文内原句）jvns 文章对 SQLite 的小注解 "SQLite 这次给我上了'数据库是复杂的'一课"—— 英语 tech blog 常用 "It was kind of fun to see how long it takes me to learn sort of basic things" 这种"自嘲句"开场，是一种谦和表述范式。

- **cartelization**（卡特尔化 / 串通定价）
  原句：出处 📰 HP 罚单报道："India fine over 'cartelization' of ink cartridges, toner, PCs" — 反垄断术语，"cartel" 指同业公司默契锁定价格或瓜分市场。"cartelize" 是动词形式，反trust 法里的核心指控之一。

- **dead man's switch**（人身安全/监控开关）
  原句：出处 📰 jvns SQLite 备份："I do usually try to monitor them with a dead man's switch." — 借指"无人续命就报警"的检测机制——原文是火车司机失能刹车装置，工程圈引申指**不定期心跳/上报来证明任务还活着**的兜底监控。