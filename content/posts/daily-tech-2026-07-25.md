---
title: "🌐 科技日报 | 2026-07-25"
date: 2026-07-25T06:57:27+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. 安防摄像头把 GitHub 管理员 token 打包进登录页面

安全研究者 hhh 对 Hanwha Wisenet XNP-9300RW 摄像头固件做逆向分析后发现，一枚 GitHub token 被重复写进约 30 个前端文件，并拥有该公司 GitHub 组织数百个仓库的管理员权限。研究者在 [完整披露](https://hhh.hn/hanwha-github-token/) 中说明，摄像头前端使用 Vite 构建，构建配置疑似把整个 `process.env` 注入前端变量，导致 CI 环境里的 `GITHUB_NPM_TOKEN` 和其他内部配置一起进入产品固件及管理界面。

研究者随后批量抓取约 500 份 Hanwha 摄像头固件，其中 62% 能用同一套方法解包；三份固件包含 GitHub token，且都是同一枚。披露邮件发出后，Hanwha 在 12 小时内回复并吊销 token。事件没有证据表明仓库已被滥用，但暴露了一个典型供应链风险：秘密并非只会被误提交到源码，也会在构建系统“把环境变量全量序列化”时进入最终产品，甚至由每台设备的 Web UI 发给访问者。

对工程团队而言，修复不能止于轮换这一枚 token。CI 应默认最小权限、按任务注入单个 secret，并在构建产物而不只是源码上运行 secret scanner；前端构建尤其需要禁止 `process.env` 全量透传。硬件固件一旦出厂，错误凭据会在大量离线设备里长期留存，撤销后虽然不能再访问仓库，却仍会暴露内部命名、地址和构建拓扑。

> 原文金句：“I checked what repos the token had access to, and it had admin privileges to hundreds of repositories in their github organization.”
> 中文对照：“我检查了这枚 token 能访问哪些仓库，发现它对该组织数百个 GitHub 仓库拥有管理员权限。”

### 2. 宇树 AS2-W 轮足机器狗：6 米/秒、33 公里空载续航

宇树发布 [Unitree AS2-W](https://www.unitree.com/As2-W/) 轮足四足机器人，把轮式移动的速度与腿式越障结合起来。整机含电池约 25 千克，最高速度约 6 米/秒；官方实验室数据称空载连续行走超过 3 小时、里程超过 33 公里，持续负载约 16 千克时仍可运行 2 小时以上。它能适应碎石、楼梯和斜坡，最大越障高度标为 0.4—0.8 米、坡度约 45°，防护等级 IP54。

硬件包括 95 N·m 工业级关节、7 英寸车轮、64—128 线激光雷达，以及可选 150 TOPS 扩展计算模块；ISS 3.0 侧向跟随系统提供厘米级定位和稳定跟随。开放 SDK 与 API 支持二次开发，可用于巡检、安防、户外运输和具身智能研究。相比纯腿机器人，轮足结构在平地用轮子换取速度和续航，遇到台阶再调用腿部自由度，是当前户外移动机器人最实际的折中路线之一。

需要注意，页面同时说明部分展示能力仍在开发测试中，参数来自实验室条件，实际表现随载重、地形与配置变化；这是一款民用机器人，官方明确要求不要进行危险改装。

> 原文金句：“Combining the high-speed of wheels with the obstacle-overcoming capability of legs, it automatically adapts to stairs, gravel, and steep slopes.”
> 中文对照：“它结合轮子的高速与腿部的越障能力，可自动适应楼梯、碎石和陡坡。”

## 📰 快讯

- **Firefox 153 把 Containers 变成原生功能**：Mozilla 宣布 [Firefox Containers Preview](https://blog.mozilla.org/en/firefox/firefox-containers-preview/)，可在同一浏览器窗口把工作、购物、个人和网银账号放进不同容器，分别隔离 cookie 与广告追踪。过去近十年这项能力主要由 Multi-Account Containers 扩展提供；现在可直接右击标签页或长按“新标签”按钮创建容器。预览版尚未覆盖扩展的全部功能，两者可并行使用。

## 📖 今日英语

- **admin privileges** — “admin privileges to hundreds of repositories”（Hanwha 固件披露）。释义：管理员权限。为什么值得记：安全事故说明里必须区分 read、write 与 admin，权限级别决定潜在影响范围。
- **build time** — “the entirety of the CI job's environment is being written to these files at build time”（Hanwha 固件披露）。释义：构建时。为什么值得记：很多 secret 泄漏不发生在运行时，而是在打包阶段被固化进产物。
- **obstacle-overcoming capability** — “the obstacle-overcoming capability of legs”（Unitree AS2-W）。释义：越障能力。为什么值得记：机器人与车辆规格中常用来描述通过台阶、沟壑和复杂地形的能力。
- **first-party feature** — “making Containers a native, first-party feature in Firefox 153”（Mozilla）。释义：第一方原生功能，由产品开发者直接维护而非第三方扩展提供。为什么值得记：功能进入 first-party 通常意味着更稳定的维护、默认可见性和更深系统集成。
