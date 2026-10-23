---
title: "从 macOS 远程连接 Ubuntu 桌面：Tailscale + GNOME Remote Desktop + 代理分流"
date: 2026-10-23T21:53:15+08:00
draft: false
tags: ["Tailscale", "RDP", "Ubuntu", "macOS", "Clash", "远程桌面", "网络"]
categories: ["技术"]
---

# 从 macOS 远程连接 Ubuntu 桌面（Tailscale + GNOME Remote Desktop + 代理分流）

> 实战总结。场景：Ubuntu 机器放在家里（**无公网 IP、无端口映射、且对外网络受限必须走代理**），人带着 MacBook 在外面，要随时连上那台 Ubuntu 的图形桌面。
> 最终方案：**Tailscale 组网 + GNOME Remote Desktop 系统级（无头）模式 + mihomo 系统服务**，已在多轮重启后验证。

本文所有命令都在 Ubuntu 侧以 `sudo` 执行，除特别注明。
文中 `<MAC_TAILNET_IP>`、`<UBUNTU_TAILNET_IP>`、`<你的局域网网段>`、`<用户名>`、`<密码>` 等占位符，请替换成你自己的实际值。

---

## 0. 最终架构

```
   [ MacBook 在外网 ]                          [ 家里 Ubuntu ]
     Tailscale 客户端                             tailscaled (systemd)
   <MAC_TAILNET_IP>  ─────── WireGuard ──────►  <UBUNTU_TAILNET_IP>
          │               直连 P2P 20~80ms              │
          │     （打洞失败时自动回落 DERP 中继）          │
          │                                            │
   RDP 客户端 ────────── TCP 3389 ────────────────────►│
   (Windows App / sdl-freerdp)                 gnome-remote-desktop
          │                                     （system 模式）
          │                                            │
          │                                  创建独立 Wayland 会话
          │                                （Remote Login，无需本地登录）

        Ubuntu 出网：所有流量 → mihomo 系统服务 (TUN utun1024) → 代理节点 → 互联网
        tailscaled 特例：控制面走 mihomo、数据面走真实 WAN（见 §2）
```

关键设计取舍：
- **代理内核与会话解耦**：mihomo 作为 systemd 系统服务常驻，不依赖"有没有人登录桌面"
- **不开 GDM 自动登录**：否则本地会话会占用用户名，Remote Login 直接拒绝（详见 §4 坑 5）

---

## 1. 安装并登录 Tailscale

```bash
# 官方源（Ubuntu 24.04/26.04 通用，把 resolute 换成你的 codename 或 noble）
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/resolute.noarmor.gpg \
  | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/resolute.tailscale-keyring.list \
  | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt update && sudo apt install -y tailscale

# 关键：不要接管 DNS（DNS 交给代理内核，避免和 fake-ip 打架）
sudo tailscale up --accept-dns=false --operator=$USER
# 浏览器打开输出的 URL 完成授权
```

验证：

```bash
tailscale status          # 应看到 Running、自己的 100.x IP、其他节点
tailscale ping <对端IP>    # 显示 "via <IP:port>" 是直连，"via DERP(xxx)" 是中继
```

> `--accept-dns=false` 的效果：`CorpDNS: false`，`/etc/resolv.conf` 不被接管。
> `--operator=$USER` 让你之后不用 sudo 也能跑 `tailscale status/up`。

---

## 2. ⭐ 核心坑：受限网络下 tailscaled 卡死在 "fetch control key"

### 现象

```
$ sudo tailscale up
# 卡住几十秒到无限，日志：
health(warnable=login-state): error: ... fetch control key:
Get "https://controlplane.tailscale.com/key?v=148": context canceled
```

而同一台机器上 `curl https://controlplane.tailscale.com/key` 却是 200。**连 TCP 连接都不会发出**（`ss -tnp | grep tailscaled` 全空）。

### 原因

tailscaled 会给自己发出的控制面/数据面流量打上 `fwmark 0x80000`，并插入自己的 ip rule **故意绕过**自己的隧道：

```
5210: from all fwmark 0x80000/0xff0000 lookup main   ← 它的流量走物理网卡直连
```

如果你的机器**本身不能直连外网（被墙/只有代理能用）**，这条规则会让控制面流量直接撞墙 → 永远认证不上。
同时 clash/mihomo 的 TUN 规则优先级在 9000+，抢不过 5210。

### 解决：按协议分流，把 tailscale 流量"部分"导入代理

新建 `/etc/systemd/system/tailscale-clash-route.service`（mihomo 的 TUN 路由表 id 默认是 **2022**）：

```ini
[Unit]
Description=Route Tailscale fwmark traffic through Clash TUN (table 2022)
After=network-pre.target
Before=tailscaled.service

[Service]
Type=oneshot
RemainAfterExit=yes
# DNS(udp/53) 必须走代理内核，保证控制面域名解析正常（fake-ip）
ExecStart=-/sbin/ip rule add fwmark 0x80000/0xff0000 ipproto udp dport 53 table 2022 pref 5010
# WireGuard/DERP/STUN 的 UDP：走真实 WAN 直连，才能 P2P 打洞
ExecStart=-/sbin/ip rule add fwmark 0x80000/0xff0000 ipproto udp table main pref 5020
# 局域网目标直连（同网段互连握手）
ExecStart=-/sbin/ip rule add fwmark 0x80000/0xff0000 to <你的局域网网段>/24 lookup main pref 5050
# 其余（主要是控制面 TCP 443）走代理
ExecStart=-/sbin/ip rule add fwmark 0x80000/0xff0000 table 2022 pref 5100

ExecStop=-/sbin/ip rule del fwmark 0x80000/0xff0000 ipproto udp dport 53 table 2022 pref 5010
ExecStop=-/sbin/ip rule del fwmark 0x80000/0xff0000 ipproto udp table main pref 5020
ExecStop=-/sbin/ip rule del fwmark 0x80000/0xff0000 to <你的局域网网段>/24 lookup main pref 5050
ExecStop=-/sbin/ip rule del fwmark 0x80000/0xff0000 table 2022 pref 5100

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now tailscale-clash-route.service   # Before=tailscaled 保证开机顺序
sudo systemctl restart tailscaled
```

**分流口诀：控制面走代理，数据面走直连。** 效果：

| 场景 | 结果 |
|---|---|
| 之前 | 全程 DERP 中继，400~900ms，SSH 敲字明显拖 |
| 之后 | 直连 P2P，**18~85ms**，scp 12Mbit/s |

> - 用 `ip rule show` 确认新规则优先级（5050/5010/5020/5100）**小于** 5210。
> - 把 `<你的局域网网段>` 换成你家的实际网段（例如 `192.168.1.0`）；网段不同就改这条规则。
> - 若之后 UDP 被运营商封掉，会**自动回落 DERP 中继**（仍可连，只是慢），无需干预。
> - 直连刚建立/路由器 NAT 端口变化时，会有几十秒的短暂中断，属正常。

---

## 3. 代理内核改成系统服务（mihomo / Clash Verge 派生的配置）

**为什么必须改**：Clash Verge 是 GUI 应用，只能活在图形会话里。若靠"自动登录 + 自启动"来保代理，那么：
- 开机就有一个本地会话占用用户名 → 远程桌面 Remote Login 被拒（§4 坑 5）
- 你退出远程桌面 → 代理跟着断

做法：把 Clash Verge 生成好的配置交给系统级 mihomo 服务，GUI 只在需要改配置时打开。

```bash
SRC=$HOME/.local/share/io.github.clash-verge-rev.clash-verge-rev
sudo mkdir -p /etc/mihomo
sudo cp "$SRC/clash-verge.yaml" /etc/mihomo/config.yaml       # GUI 生成的"增强后"配置
sudo cp -r "$SRC/rule-providers" /etc/mihomo/                  # 规则库缓存（避免开机无网拉取失败）
for f in Country.mmdb ASN.mmdb geoip.dat geosite.dat; do sudo cp "$SRC/$f" /etc/mihomo/; done
sudo chown -R root:root /etc/mihomo && sudo chmod 600 /etc/mihomo/config.yaml

# 先校验再跑
sudo /usr/bin/verge-mihomo -t -d /etc/mihomo -f /etc/mihomo/config.yaml
```

`/etc/systemd/system/mihomo.service`：

```ini
[Unit]
Description=Mihomo core (config generated by Clash Verge)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/verge-mihomo -d /etc/mihomo -f /etc/mihomo/config.yaml
Restart=always
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl disable --now clash-verge-service      # 别和系统内核抢 TUN/端口
sudo systemctl enable --now mihomo.service

# 验证（无任何桌面会话也应正常）
ss -ltn | grep 7897 ; ip -br link show | grep utun1024
curl -s https://api.ipify.org                          # 应为代理节点 IP
```

配套两个小工具（可选但强烈建议）：

```bash
# /usr/local/bin/clash-sync —— 把 GUI 改好的配置同步到系统内核
#!/bin/bash
set -e
SRC=/home/<user>/.local/share/io.github.clash-verge-rev.clash-verge-rev
DST=/etc/mihomo
install -m 600 "$SRC/clash-verge.yaml" "$DST/config.yaml"
for f in Country.mmdb ASN.mmdb geoip.dat geosite.dat; do [ -f "$SRC/$f" ] && install -m 644 "$SRC/$f" "$DST/$f"; done
[ -d "$SRC/rule-providers" ] && cp -f "$SRC/rule-providers/"* "$DST/rule-providers/" 2>/dev/null || true
/usr/bin/verge-mihomo -t -d "$DST" -f "$DST/config.yaml" >/tmp/clash-sync-test.log 2>&1 \
  && systemctl restart mihomo.service && echo "✅ 已同步" \
  || { echo "❌ 配置校验失败，未应用"; exit 1; }

# ~/bin/clash-gui —— 需要 GUI 改配置时：停内核 → 开 GUI → 关掉后自动同步
#!/bin/bash
systemctl is-active --quiet mihomo.service && { sudo systemctl stop mihomo.service; S=1; }
/usr/bin/clash-verge
[ "$S" = 1 ] && sudo /usr/local/bin/clash-sync
```

免密码（可选）：`/etc/sudoers.d/clash-sync`

```
<user> ALL=(root) NOPASSWD: /usr/local/bin/clash-sync, /usr/bin/systemctl stop mihomo.service, /usr/bin/systemctl start mihomo.service, /usr/bin/systemctl restart mihomo.service
```

---

## 4. 开启远程桌面：GNOME Remote Desktop 系统级（无头）模式

Ubuntu Desktop 预装了 `gnome-remote-desktop`（26.04 是 50.x），直接用它，**不要装 xrdp**。

### 4.1 生成证书 + 配置 + 启用

```bash
sudo mkdir -p /etc/gnome-remote-desktop
sudo openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 \
  -subj "/C=CN/ST=Local/L=Local/O=Self/CN=$(hostname)" \
  -keyout /etc/gnome-remote-desktop/tls.key \
  -out    /etc/gnome-remote-desktop/tls.crt

# ★ 属主必须是 gnome-remote-desktop 用户，否则服务 active 但 3389 不监听
sudo chown gnome-remote-desktop:gnome-remote-desktop /etc/gnome-remote-desktop/tls.key /etc/gnome-remote-desktop/tls.crt
sudo chmod 600 /etc/gnome-remote-desktop/tls.key

sudo grdctl --system rdp set-tls-cert /etc/gnome-remote-desktop/tls.crt
sudo grdctl --system rdp set-tls-key  /etc/gnome-remote-desktop/tls.key
sudo grdctl --system rdp set-credentials <用户名> <密码>     # RDP 层凭据（明文存 /etc/gnome-remote-desktop/grd.conf）
sudo grdctl --system rdp disable-view-only                  # 允许键鼠控制，不是只读
sudo grdctl --system rdp enable
sudo systemctl enable --now gnome-remote-desktop.service

sudo grdctl --system status --show-credentials
ss -ltn | grep 3389
```

> **系统模式 vs 用户模式**
> | | `grdctl --system`（本文用） | `grdctl`（用户模式） |
> |---|---|---|
> | 配置位置 | `/etc/gnome-remote-desktop/` | `~/.config/gnome-remote-desktop/` + **GNOME 钥匙环** |
> | 需要登录桌面 | 不需要 | 需要 |
> | 会话 | 新建独立无头会话 | 共享当前桌面 |
> | 凭据存储 | GKeyFile，无坑 | 钥匙环锁定就写不进去（自动登录场景必踩） |

### 4.2 五个实战坑（按出现概率排序）

**坑 1｜服务 active 但不监听 3389**
```bash
sudo journalctl -u gnome-remote-desktop -n 20 --no-pager | grep -i tls
# "RDP TLS certificate and key not yet configured properly"
```
原因：`tls.key` 是 `root:root 600`，而服务以 `User=gnome-remote-desktop` 运行读不到。
解决：`chown gnome-remote-desktop:` 后 `systemctl restart gnome-remote-desktop`。

**坑 2｜用户模式 `Cannot create an item in a locked collection`**
原因：`grdctl rdp set-credentials` 要把密码写进 GNOME 钥匙环，而 GDM 自动登录 → login keyring 处于锁定态（无密码可解）。
解决：改用**系统模式**（本文方案），凭据存 GKeyFile，完全绕开钥匙环。

**坑 3｜客户端提示 `Session Already Running`** ⭐ 最致命
```
Remote login is not possible because a local session is already running for <user>.
To login remotely, you must log out from the local session or Force stop it.
```
原因：GNOME Remote Login **不允许同一用户同时存在本地会话**。为了"开机自启代理"而开的 GDM 自动登录正好制造了这个本地会话。
解决（二选一）：
- 关掉自动登录（本文选择，配合 §3 的系统级 mihomo，代理不再依赖桌面）
  ```bash
  # /etc/gdm3/custom.conf
  [daemon]
  AutomaticLoginEnable=false
  ```
  然后 `sudo loginctl terminate-session <seat0 上的会话号>` 立即生效
- 或每次点 Force Stop（会杀掉本地会话里的程序，代理会断，不推荐）

> ⚠️ 用脚本改 `custom.conf` 时注意：`echo pw | sudo -S ... python3 - <<'PY'` 会让 sudo 把 heredoc 当密码吃掉，**编辑静默失败**。直接写文件再 `cp` 更稳，改完一定 `grep` 确认。

**坑 4｜macOS 版 Windows App 报 "The Credentials Did Not Work"**
原因：系统模式的连接是**两段式**——先 NLA 认证，然后服务器发**重定向（RDSTLS）**让客户端带 routing token 重连。服务端日志能看到：
```
Incoming connection without routing token → NLA 通过 → Sending server redirection
Incoming connection with routing token → nla_recv() error: -1 → client authentication failure
```
macOS 版 Windows App 在第二段失败（不动 RDSTLS），**密码没错也会一直弹凭据框**。
解决：换支持 RDSTLS 的客户端（FreeRDP），或信任证书后再试（见 §5）。

**坑 5｜客户端一直弹证书警告**
自签名证书 + CredSSP，微软系客户端会拦。macOS 上把证书加信任：
```bash
scp root@ubuntu:/etc/gnome-remote-desktop/tls.crt ./ubuntu-rdp.crt   # 或从 /var/lib 下取
security add-trusted-cert -r trustRoot -k ~/Library/Keychains/login.keychain-db ./ubuntu-rdp.crt
security verify-cert -c ./ubuntu-rdp.crt -p ssl -L    # 应输出 "certificate verification successful"
```

---

## 5. macOS 客户端选型（重要）

| 客户端 | RDSTLS（系统模式必需） | 有无窗口 | 结论 |
|---|---|---|---|
| **Windows App**（原 Microsoft Remote Desktop，App Store 免费） | ❌ macOS 版实测不支持 | ✅ | 只适合连 Windows；连 GNOME Remote Login 会卡在第二段认证 |
| `sfreerdp`（brew freerdp） | ✅ | ❌ **该二进制没链接 SDL/X11** | 连得上但**永远看不到窗口**，别用 |
| **`sdl-freerdp`**（brew freerdp） | ✅ | ✅ 链接了 `libSDL3.0.dylib` | ✅ **能用**（本文推荐） |
| `xfreerdp`（brew freerdp） | ✅ | ✅ 但需要 XQuartz | 可用，需 `brew install --cask xquartz` |

### 判定 `sfreerdp` 是不是"无窗口版"

```bash
otool -L /opt/homebrew/Cellar/freerdp/*/bin/sdl-freerdp | grep SDL   # 有输出才行
nm -u /opt/homebrew/Cellar/freerdp/*/bin/sfreerdp | grep -c SDL      # 0 = 无窗口
```

### 推荐用法（macOS）

```bash
brew install freerdp        # 装完得到 sdl-freerdp（带窗口）和 sfreerdp（无窗口，别用）
```

```bash
# ~/bin/rdp-ubuntu
#!/bin/bash
exec /opt/homebrew/bin/sdl-freerdp \
  /v:<UBUNTU_TAILNET_IP> /u:<用户名> /p:<密码> /cert:ignore \
  /dynamic-resolution +clipboard "$@"
```

常用参数：`/f` 全屏（`Ctrl+Alt+Enter` 切换）、`/cert:ignore` 忽略自签名证书、`+clipboard` 剪贴板互通。
连上后是 GDM 登录界面 → 输入**系统账号密码** → 进入独立桌面会话。

> 想双击启动，可以包成 `.app`（`Contents/MacOS/<可执行脚本>` + `Info.plist` 里写 `CFBundleExecutable`），
> **并注意**：从无图形权限的后台 shell（如某些 agent/守护进程环境）里 `open` 这类 GUI 程序不会有可见窗口，
> `screencapture` 也会报 `could not create image from display` —— 必须由用户在自己的 Terminal / Finder 里启动。

---

## 6. 一键自检清单（重启后跑一遍）

```bash
# Ubuntu 侧
systemctl is-active mihomo.service tailscale-clash-route.service tailscaled gnome-remote-desktop
ss -ltn | grep -E ':(7897|3389)'          # 都应有监听
ip -br link show | grep utun1024          # TUN 存在
curl -s https://api.ipify.org             # = 代理出口 IP
tailscale status | head -3                # Running
loginctl list-sessions | awk 'NR>1 && $3=="seat0" && $5=="user"'   # 应为空（无本地用户会话）

# macOS 侧
tailscale ping <ubuntu tailnet IP>        # 期望 "via <公网IP>:41641" 直连，几十 ms
nc -z -w 3 <ubuntu tailnet IP> 3389 && echo RDP-ok
```

---

## 7. 日常运维命令速查

| 需求 | 命令 |
|---|---|
| 看 remote desktop 日志 | `sudo journalctl -u gnome-remote-desktop -f` |
| 改 RDP 账号密码 | `sudo grdctl --system rdp set-credentials <u> <p>` |
| 让桌面可键鼠控制 | `sudo grdctl --system rdp disable-view-only` |
| 重启 RDP 服务 | `sudo systemctl restart gnome-remote-desktop` |
| 看代理是否在跑 | `systemctl status mihomo` / `curl -s https://api.ipify.org` |
| 改代理配置（GUI） | 远程桌面里跑 `~/bin/clash-gui` |
| 只同步配置 | `sudo /usr/local/bin/clash-sync` |
| 看 tailscale 走什么路径 | `tailscale ping <peer>`（看 `via ...` 是直连还是 DERP） |
| 看本机路由分流 | `ip rule show`（注意 5xxx 规则要早于 9xxx） |
| 查会话冲突 | `loginctl list-sessions` |

---

## 8. 一页速查表：症状 → 原因 → 解决

| 症状 | 原因 | 解决 |
|---|---|---|
| `tailscale up` 卡死、`fetch control key ... context canceled` | tailscaled 的 `fwmark 0x80000 → main` 让控制面直连被墙网络 | §2 的 `tailscale-clash-route.service` 分流 |
| tailscale 全走 DERP，几百 ms | WireGuard UDP 被代理掉了，无法打洞 | 让 UDP 走 `main` 表直连（§2） |
| 服务 active 但 3389 不监听 | `tls.key` 不是 `gnome-remote-desktop` 属主 | `chown` 后重启服务 |
| `Cannot create an item in a locked collection` | 用户模式 + 自动登录 → 钥匙环锁定 | 改系统模式 `grdctl --system` |
| `Session Already Running` | 有本地桌面会话占着该用户 | 关闭 GDM 自动登录 + 结束本地会话 |
| Windows App 反复要凭据 | macOS 版不支持 GNOME 的 RDSTLS 重定向 | 换 `sdl-freerdp` |
| `sfreerdp` 连上但没窗口 | 该二进制未链接 SDL/X11 | 改用 `sdl-freerdp` |
| 证书警告刷屏 | 自签名证书 | macOS 上加信任，或 `/cert:ignore` |
| 断开远程桌面后代理就没了 | 代理跑在图形会话里 | 改成 systemd 系统级 mihomo（§3） |

---

## 9. 安全提醒

- RDP 的 3389 默认监听 `*:3389`。既然只用 Tailscale 访问，建议限制只在 `tailscale0` 上可达：
  ```bash
  sudo iptables -A INPUT -i tailscale0 -p tcp --dport 3389 -j ACCEPT
  sudo iptables -A INPUT -p tcp --dport 3389 -j DROP     # 其余来源丢弃（注意先放行已建立连接）
  ```
  或用 `ufw` 规则绑定接口。
- 自签名证书的指纹记录在 `sudo grdctl --system status` 里，首次连接核对一下更稳妥。
- RDP 层凭据明文存在 `/etc/gnome-remote-desktop/grd.conf`（root 600），别和系统登录密码搞混。

---

## 10. 环境版本（本次实测）

| 组件 | 版本 |
|---|---|
| Ubuntu | 26.04.1 LTS，GNOME Shell 50.1（Wayland），x86_64 |
| gnome-remote-desktop | 50.2 |
| tailscale | 1.104.2 |
| mihomo (verge-mihomo) | v1.19.32（gvisor） |
| macOS | 27.0.1 (arm64) |
| FreeRDP | 3.32.2（brew） |
