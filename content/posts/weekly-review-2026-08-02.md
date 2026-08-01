---
title: "🧭 周报 | 2026-08-02"
date: 2026-08-02T06:37:19+08:00
draft: false
tags: ["周报", "趋势"]
categories: ["周报"]
---

> 本期覆盖 2026 年 7 月 27 日—8 月 2 日。周报只回读本周已发布日报；8 月 2 日股票市场休市未发，因此趋势依据本周 7 篇 AI 日报、7 篇论文日报、7 篇科技日报和 5 篇股票日报整理。

## 🧭 本周主线

### 1. 模型竞争进入“能力、价格与成功任务成本”同时定价

本周模型层最明显的变化不是单一冠军，而是能力和价格开始被放进同一张表。OpenAI 先解释 GPT-5.6 如何在前沿能力与推理效率之间取舍，随后宣布 Luna 价格大幅下降、Sol 用更高单价换取约 2.5 倍速度；同周还向学术研究者提供覆盖 10 万人的前沿模型访问（[7/30 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-30/)、[7/31 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-31/)）。DeepSeek 则把 V4-Flash 正式版推入公测，在不改变架构和规模的前提下重做后训练，原生兼容 Responses API 与 Codex（[8/1 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-08-01/)）。

开放权重也从“承诺开放”进入可下载和可核验阶段。Kimi K3 的完整模型权重与模型卡上线 Hugging Face，2.8T 总参数、每 token 激活 104B 参数、百万 token 上下文和 MXFP4/MXFP8 训练配置都有了可检查载体（[7/28 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-28/)）。与此同时，OpenAI 的企业文章反复强调 `cost of a successful outcome`，把重试、人工监督、错误和等待时间都算入成本，而不是只比较百万 token 单价（[8/1 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-08-01/)）。

放在近一个月看，上期周报提出“模型 + harness 的每项任务成本”会取代单纯 benchmark，本周定价和产品都开始围绕这件事落地。后续选型不会只问谁分数最高，而会同时比较速度档、协议兼容、长上下文成本、失败恢复和可验证结果；便宜模型若需要更多重试，也未必真的便宜。

### 2. Agent harness 从外围框架变成状态、预算、审计与恢复的系统工程

Kimi Code 的 Agent Core v2 用按作用域状态容器、按 Profile 激活工具和步骤上限后的目标续跑，把“长任务能否继续、不同角色能看见什么工具、状态如何观测”变成内核能力（[7/27 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-27/)）。Gemini 托管 Agent 随后加入工具调用前后钩子、总 token 预算上限和定时触发器；MCP 2026-07-28 规范则把核心改为无状态请求/响应，并为多轮往返、缓存和发行方校验补齐协议基础（[7/29 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-29/)）。

论文侧同步出现了“让中间状态成为产品”的设计。JarvisHub 把参考资料、草稿、失败尝试、版本关系和人类反馈保存在可演化画布中；CodeNib 为编程 Agent 抽出可复用的仓库索引服务；Qwen-UI-Agent 又把手机、桌面、网页和 CLI 统一到一个动作空间并支持百步流程（[7/29 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-07-29/)、[7/31 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-07-31/)、[8/1 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-08-01/)）。工具版本则持续修复 MCP 重连、压缩膨胀、历史重放、数据库恢复和消息持久投递。

放在近一个月看，harness 已不再是“给模型套个循环”的轻量胶水，而是类似操作系统和工作流引擎的基础设施：必须管理身份、状态、预算、工具面、日志、重试、分支和崩溃恢复。模型能力逐渐商品化后，真正难复制的可能正是这些长期运行的工程约束。

### 3. AI 安全从“模型会不会作恶”下沉到密钥、内核与可复验证据链

Hugging Face 入侵事件在本周继续产生技术复盘。Tailscale 明确指出，零信任网络无法拯救已从 secret store 泄露的长期 auth key：攻击者把可复用凭据带到外部，仍能被网络忠实识别为授权 CI 节点。其建议是让云或 CI 通过 workload identity federation 获取短期身份，而不是保存长期静态密钥（[8/1 科技日报](https://qpzm7903.github.io/posts/daily-tech-2026-08-01/)）。

形式化验证也暴露了自身实现边界。Lean 的嵌套归纳类型漏洞让一份 AI 辅助的 Collatz “反证”在没有 `sorry` 的情况下通过内核，并且恰好同时击中旧版外部检查器 nanoda 的另一处漏洞；团队在报告后一小时修复，并开始用多个独立内核和对抗样本持续比较（[8/2 科技日报](https://qpzm7903.github.io/posts/daily-tech-2026-08-02/)）。另一边，Anthropic 用 Claude 寻找 HAWK-256 与简化 AES 的算法结构弱点，OpenAI 的科学计算案例则再次强调：Agent 可以更快实现，但无法可靠判断科学结论是否成立（[7/29 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-29/)）。

放在近一个月看，安全边界正从单个提示词或工具调用下沉到完整证据链：凭据寿命、内核实现、独立检查器、可复现基准和人工责任缺一不可。未来“有形式化证明”也不能只看绿色勾号，还要问证明陈述、可信计算基、检查器版本和独立实现是否都对得上。

### 4. Physical AI 从单点模型走向“世界表示 + 数据 + 实时部署”

本周具身智能沿着三个层面推进。Gemini Robotics 2 从桌面抓取扩到全身控制和多机器人协作；NVIDIA Cosmos-H-Dreams 把手术机器人世界模型蒸馏到单张 RTX PRO 6000 上约 160 FPS 的闭环模拟；TurboVLA 则把机器人视觉—语言—动作模型压到不足 1GB 显存，并在 RTX 4090 上达到 32Hz（[7/31 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-31/)、[7/28 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-28/)、[7/31 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-07-31/)）。

论文还开始拆解“世界模型应该预测什么”。SANA-Video 2.0 用混合线性注意力降低视频生成成本；PhiZero 不直接把所有规律藏在像素预测里，而是先生成离散的“物理语言”再渲染视频；DistillAlign 则提醒视频蒸馏不能只追求高质量样本，还要保留教师分布的覆盖与多样性（[7/28 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-07-28/)、[8/2 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-08-02/)）。

放在近一个月看，physical AI 的竞争焦点逐渐从“能否生成一段未来视频”转为表示能否解释、部署能否实时、跨硬件能否运行、训练数据能否覆盖真实长流程。世界模型、机器人策略和视频模型正在共享更多中间表示，但最终价值仍取决于真实设备上的错误恢复与安全边界。

### 5. AI 资本开支开始接受现金流、利率与跨市场轮动的共同审判

本周市场先经历对成长资产的剧烈再定价。A 股创业板一度单日下跌 7.35%，美股半导体承压而道指上涨，显示风险并非简单“全市场下跌”，而是从拥挤的算力和成长交易向传统板块轮动（[7/29 股票日报](https://qpzm7903.github.io/posts/daily-stock-2026-07-29/)）。FOMC 随后维持利率不变，但三名票委主张加息；美国 PCE 环比下降、同比通胀仍高于目标，英国央行也在 3.75% 利率上出现三名加息支持者（[7/30 股票日报](https://qpzm7903.github.io/posts/daily-stock-2026-07-30/)、[7/31 股票日报](https://qpzm7903.github.io/posts/daily-stock-2026-07-31/)）。

财报又把情绪拉回业绩。微软季度营收达到 900 亿美元、Azure 增长 43%，苹果创下最强六月季度并实现 16% 营收增长，科技业绩推动美股明显反弹（[7/30 科技日报](https://qpzm7903.github.io/posts/daily-tech-2026-07-30/)、[7/31 科技日报](https://qpzm7903.github.io/posts/daily-tech-2026-07-31/)）。但油价和地缘风险反复、长端利率与融资成本仍会影响高资本开支公司的估值。

放在近一个月看，“AI 基建是否值得投”已经从单向扩张叙事变成多变量账本：收入增长、自由现金流、融资利率、芯片供应和仓位拥挤度会同时定价。强财报可以暂时修复风险偏好，却不能替代对资本回报周期的持续验证。

## 📈 值得持续盯的信号

- **OpenAI 十项数学结果能否经受领域级独立审阅**：Lean 证书提供机械验证，但下一步要看数学家是否确认问题陈述、假设和贡献边界，以及论文署名规则是否形成可复用惯例（[8/2 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-08-02/)）。
- **长上下文订阅与 API 计费边界是否继续分化**：oh-my-pi 17.2.3 因 Anthropic OAuth 订阅缺少 1M 上下文额度而撤下 beta 声明，说明“模型目录标称支持”与“当前凭据实际可用”之间仍需运行时门禁。
- **Agent 安全是否统一到短期身份 + 多检查器 + 全轨迹日志**：Tailscale、Lean 和本周多个工具修复指向同一方向。若云身份、证明检查与 Agent 平台开始共享可审计字段，事故复盘会从手工取证走向标准化。

## 📖 本周英语回顾

1. **task crossover** — 出处：[7/28 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-28/)：“We call the resulting pattern task crossover.” 释义：任务跨界；一个岗位借助 AI 承担传统上属于另一岗位的任务。
2. **runaway tasks** — 出处：[7/29 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-29/)：“To prevent runaway tasks, you can pass `max_total_tokens` ...” 释义：失控任务；指 Agent 循环持续消耗时间或预算却不收敛。
3. **scientifically valid** — 出处：[7/29 AI 日报](https://qpzm7903.github.io/posts/daily-ai-2026-07-29/)：“Agents ... could not reliably judge whether their work was scientifically valid.” 释义：在科学上成立；比“代码可运行”多一层方法与结论有效性。
4. **workload identity federation** — 出处：[8/1 科技日报](https://qpzm7903.github.io/posts/daily-tech-2026-08-01/)：“We built workload identity federation for cases like this.” 释义：工作负载身份联合；让程序按运行环境换取短期凭据，避免静态密钥。
5. **recursive self-improvement** — 出处：[8/2 论文日报](https://qpzm7903.github.io/posts/daily-papers-2026-08-02/)：“Recursive self-improvement (RSI) requires AI systems that improve the process of building AI.” 释义：递归自我改进；系统不仅完成任务，还改进构建和优化系统的过程。
