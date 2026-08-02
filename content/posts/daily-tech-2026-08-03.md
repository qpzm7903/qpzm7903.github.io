---
title: "🌐 科技日报 | 2026-08-03"
date: 2026-08-03T06:38:52+08:00
draft: false
tags: ["科技", "日报"]
categories: ["科技日报"]
---

## ⭐ 今日最值得关注

### 1. Bor 0.8.0：Linux 桌面策略管理补齐邮件、浏览器与防火墙

开源 Linux 桌面策略管理系统 Bor 发布 0.8.0，新增 Thunderbird、Microsoft Edge for Business 和 Firewalld zone 三类策略。Thunderbird 与 Edge 的受管配置会按绑定策略合并写入，最后一条策略移除时恢复或清理文件；Flatpak 安装也在检测范围内，外部篡改会被 watcher 发现并还原。

Firewalld 策略可管理服务、端口、转发端口、rich rule、伪装、接口、来源和 zone target。Agent 先把 XML 写入 `/etc/firewalld/zones/`，再用 `firewall-cmd --check-config` 校验并重新加载，避免直接把无效配置推进系统。Polkit 规则则新增 `action.lookup()` 变量条件，例如只允许挂载可移动磁盘。

这一版也重做了 Web UI：页面拥有真实 URL，节点与合规列表改成服务端分页、过滤和排序，并为删除操作加输入确认。安全修补包括把 Agent 身份严格绑定到 mTLS 客户端证书、迁移旧 TOTP 密钥加密、阻断软件源重定向 SSRF、避免审计 CSV 公式注入，以及不再把初始管理员密码写进日志。升级时 Agent 也必须到 0.8.0，否则会忽略新策略类型。

**原文金句：** “Agent identity is now strictly bound to the mTLS client certificate, and MFA/RBAC enforcement paths were hardened on the server.”
**中文：** Agent 身份现在严格绑定到 mTLS 客户端证书，服务端的 MFA 与 RBAC 执行路径也得到加固。

[Bor 官方发布说明：Bor v0.8.0 released](https://getbor.dev/blog/2026-08-02-bor-v080-release/)

### 2. Kakehashi 让部分 macOS ARM64 命令行程序跑在 Linux ARM64 用户态

Kakehashi 是一个刚创建十天左右的实验项目：它在 Linux aarch64 用户态加载 Darwin Mach-O，映射自带的精简 `libSystem`，再翻译 BSD 系统调用；没有 JIT，也不是 CPU 指令模拟器。当前 README 声称已实际运行 clang 探针、Darwin 版 7-Zip 和 curl，并支持线程、HTTP/HTTPS 与把 guest 的 `/Volumes/linux/` 桥接到宿主文件系统。

它的目标不是替代完整 macOS。官方明确把 POST、代理、HTTP/3 全路径、Apple Security.framework、Git/Xcode 命令行工具、GUI 和代码签名列为尚未交付；眼下更接近“让纯命令行 Darwin 二进制进入便宜的 Linux ARM64 CI”。

性能也有清楚边界：在约 8,000 个文件、240MiB 的 7-Zip 测试里，Kakehashi 用约 118 秒，原生 Linux 7zz 约 22.5 秒，相差约 5.2 倍；少文件、重压缩任务差距可缩到约 1.1—1.2 倍。项目认为，即使任务慢 5 倍，Linux ARM64 托管 runner 每分钟 0.005 美元相对 macOS 0.062 美元仍可能更便宜，但 GUI、签名、公证和 Xcode UI 测试仍应留在 macOS。仓库创建于 7 月 24 日，8 月 2 日仍有代码更新；这是早期工程，不应按成熟兼容层理解。

**原文金句：** “The product goal for CI is not "as fast as native macOS," but run Darwin CLI/tools on cheap Linux aarch64 runners instead of scarce, expensive macOS capacity.”
**中文：** 这个 CI 产品目标不是“和原生 macOS 一样快”，而是在便宜的 Linux aarch64 runner 上运行 Darwin 命令行工具，替代稀缺且昂贵的 macOS 资源。

[Kakehashi 官方仓库](https://github.com/wie-project/kakehashi)

## 📰 快讯

### Meshdiff 把 3D 模型版本差异留在浏览器本地计算

[Meshdiff](https://meshdiff.com/) 今日在 HN 获得 166 points。当前 0.0.1 页面允许分别载入 STL、3MF 或 OBJ 两个版本并计算差异，解析和 diff 全在浏览器本地完成，文件不会上传；团队协作、版本历史、评论锚点和报告导出都被明确列为路线图，尚不是已交付功能。

## 📖 今日英语

1. **finer-grained RBAC（更细粒度的 RBAC）**
   原句（Bor 0.8.0）：“Bor v0.8.0 is out. This release adds three new policy types — Thunderbird, Microsoft Edge for Business, and Firewalld zones — alongside a full web UI overhaul, finer-grained RBAC, and a dedicated security hardening pass.”
   权限系统中表示把一个宽泛管理权限拆成多个具体动作权限。
2. **tamper-protected（防篡改保护的）**
   原句（Bor 0.8.0）：“Like all other managed files, the zone files are tamper-protected.”
   常用于配置、日志和固件，表示未授权修改会被阻止、发现或恢复。
3. **no JIT（无即时编译）**
   原句（Kakehashi）：“Userspace macOS ARM64 → Linux aarch64 translation layer (CLI-first, no JIT).”
   `JIT` 是 just-in-time compilation；这里说明执行路径不靠运行时动态翻译 CPU 指令。
4. **syscall boundary（系统调用边界）**
   原句（Kakehashi）：“The tax is the syscall boundary (TLS switch, alt stack, NEON save/restore, Rust dispatch) × how chatty the guest is — not an instruction emulator.”
   用户态程序进入内核服务的边界；调用越频繁，兼容层额外开销越明显。
