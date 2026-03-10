---
title: "一键打通本地 Agent 到远端 K8s Arthas MCP：脚本化接入实战"
date: 2026-03-10T14:12:00+08:00
draft: false
tags: ["Arthas", "MCP", "Kubernetes", "Java", "脚本化", "SSH", "port-forward", "排障"]
categories: ["Java 性能分析", "Kubernetes", "实战指南"]
description: "上一篇讲清楚了为什么要用 SSH + kubectl port-forward 把远端 Arthas MCP 安全带到本地。这一篇继续往前走：把它做成一键脚本，讲清楚参数设计、执行流程、典型命令、常见故障和压测中的使用姿势。"
---

上一篇我已经把核心结论讲清楚了：

> **远端 K8s 里的 Arthas MCP，不应该直接暴露给本地 Agent，而应该通过 SSH + kubectl port-forward，在本地制造一个安全、稳定、看起来像本地的 MCP 地址。**

但光有这个结论还不够。

因为只要你真的开始用，就会立刻遇到一堆工程层问题：

- 每次都手工敲一堆命令，太容易出错
- Pod 名称会变
- 压测前要快速切换实例
- 链路断了之后，很难判断是 SSH 问题、kubectl 问题，还是 Arthas 根本没起来
- 本地 Agent 需要的不只是“知道原理”，而是一个稳定可复用的本地 MCP 地址

所以这一篇不再讲抽象架构，而是专注一件事：

> **如何把本地 Agent → 远端 K8s Pod 内 Arthas MCP 的接入流程，做成一键脚本，并真正用于压测实战。**

本文配套脚本：

```text
~/.openclaw/workspace/scripts/connect-arthas-mcp.sh
```

---

## 一、脚本到底解决了什么问题

先看没有脚本时，你通常要做哪些事。

### 手工方式

1. 登录远端 master / bastion
2. 找到目标 namespace 和 Pod
3. 执行 `kubectl port-forward pod/<pod> 8563:8563`
4. 在本地再执行 `ssh -L 18563:127.0.0.1:8563 user@host`
5. 手工 `curl` 检查 `/mcp`
6. 再复制一段 MCP 配置到本地客户端

这套流程最大的问题不是“步骤多”，而是：

- **步骤分散**：K8s、SSH、本地端口、认证都散在不同地方
- **容易错位**：很容易连错 Pod，或者连上了一个已经不再承接流量的实例
- **不利于复用**：同一个动作，压测前、排障时、复现问题时都要重复做

所以脚本的目标不是“省几个字符”，而是把一条诊断链路固化成一个可执行单元。

---

## 二、脚本做了哪四件事

`connect-arthas-mcp.sh` 主要做四件事：

### 1. 选择目标 Pod

脚本支持两种模式：

- 直接指定 `--pod`
- 通过 `--selector` 自动选择一个 Running Pod

这一步的意义是把“实例选择”显式化。

在压测分析里，这是很关键的。因为你如果连错 Pod，后续所有分析都可能是伪结论。

### 2. 在远端执行 `kubectl port-forward`

脚本会先 SSH 到你指定的远端主机，然后在远端执行：

```bash
kubectl -n <namespace> port-forward pod/<pod-name> <remote-port>:<container-port>
```

默认映射是：

```text
18563 -> 8563
```

也就是远端主机的 `127.0.0.1:18563` 作为临时桥接端口，对接 Pod 内 Arthas 的 `8563`。

### 3. 在本地建立 SSH 隧道

接着脚本会在本地启动：

```bash
ssh -L <local-port>:127.0.0.1:<remote-port> user@host
```

这一步之后，本地就有了一个可访问的地址：

```text
http://127.0.0.1:<local-port>/mcp
```

### 4. 输出可直接复制的 MCP 配置片段

脚本不是只负责“打通链路”，还会把最终可用的 MCP 配置直接打印出来。

这一步很重要，因为它让“接入链路”和“客户端配置”在同一个动作里闭环了。

---

## 三、脚本参数设计：为什么这么定

下面是脚本里最核心的参数。

### 必填参数

```bash
--host <master-ip>
--user <ssh-user>
--namespace <ns>
```

这三个参数决定了：

- 去哪台主机执行远端命令
- 用谁的身份 SSH 上去
- 操作哪个 K8s namespace

### Pod 选择参数

二选一：

```bash
--pod <pod-name>
--selector <label-selector>
```

我的建议是：

- **排障 / 精确分析**：优先 `--pod`
- **临时接入 / 快速验证**：可以先用 `--selector`

因为 `--selector` 取到的是第一个 Running Pod，它适合快速起步，但不一定就是你压测真正命中的那个实例。

### 端口参数

```bash
--container-port 8563
--remote-port 18563
--local-port 18563
```

它们分别表示：

- Pod 内 Arthas HTTP 端口
- 远端主机上的临时桥接端口
- 本地最终暴露给 Agent 的端口

默认我把远端和本地都设成 `18563`，是为了减少心智负担。你一眼就能知道：

```text
127.0.0.1:18563/mcp
```

就是最终入口。

### 认证参数

```bash
--bearer-token <token>
```

这个参数只用于：

- 脚本输出验证用 `curl`
- 输出客户端 MCP 配置片段

它**不会替你去修改远端 Arthas 配置**。这点刻意设计成这样，是为了把“连接”与“远端服务配置”分层。

### 连接参数

```bash
--ssh-port <port>
--identity-file <path>
--sshpass <password>
```

这里我建议：

- 正式使用优先 `--identity-file`
- `--sshpass` 仅在临时环境或自动化试验时用

原因很简单：命令行带密码天然有留痕风险。

### 调试参数

```bash
--dry-run
--no-check
```

这两个参数是给排障准备的。

- `--dry-run`：先看脚本到底要执行什么
- `--no-check`：跳过连通性验证，适合你想先粗暴打通再说的场景

---

## 四、最常用的三种命令

### 场景 1：快速验证，先随便连一个 Running Pod

```bash
bash ~/.openclaw/workspace/scripts/connect-arthas-mcp.sh \
  --host 10.0.0.12 \
  --user ops \
  --namespace perf \
  --selector 'app=my-java-service' \
  --bearer-token 'your-secure-password'
```

适合：

- 先确认远端链路是不是通的
- 先验证 Arthas MCP 是否正常响应
- 还没到精确定位实例的时候

### 场景 2：明确指定 Pod，做精确分析

```bash
bash ~/.openclaw/workspace/scripts/connect-arthas-mcp.sh \
  --host 10.0.0.12 \
  --user ops \
  --namespace perf \
  --pod myapp-7f6b5d8f5d-abcde \
  --bearer-token 'your-secure-password'
```

适合：

- 你已经知道压测命中的就是这个实例
- 你要对这个 Pod 做长时间分析
- 你不想让 selector 带来随机性

### 场景 3：先不执行，只看命令是否合理

```bash
bash ~/.openclaw/workspace/scripts/connect-arthas-mcp.sh \
  --host 10.0.0.12 \
  --user ops \
  --namespace perf \
  --selector 'app=my-java-service' \
  --dry-run
```

适合：

- 第一次在新环境里接入
- 你怀疑 context / namespace / pod 选择可能有问题
- 你想先审一下脚本到底会干什么

---

## 五、脚本执行后的标准输出长什么样

如果链路打通，脚本会输出类似内容：

```text
================ 连接已建立 ================
目标主机:        10.0.0.12
命名空间:        perf
目标 Pod:        myapp-7f6b5d8f5d-abcde
容器 Arthas 端口: 8563
远端转发端口:     18563
本地监听端口:     18563
本地 MCP 地址:    http://127.0.0.1:18563/mcp
===========================================
```

然后它会继续打印：

1. 一条建议的 `curl`
2. 一段可复制的 MCP 配置片段
3. 一份建议的诊断顺序

这就意味着，当脚本执行结束时，你已经同时得到了三样东西：

- 一个能访问的本地 MCP 地址
- 一条验证命令
- 一段能粘进 Agent 的配置

这就是“工程闭环”。

---

## 六、接入后，Agent 配置应该是什么样子

如果本地地址是：

```text
http://127.0.0.1:18563/mcp
```

你的客户端配置通常就是：

```json
{
  "mcpServers": {
    "arthas-mcp": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:18563/mcp",
      "headers": {
        "Authorization": "Bearer your-secure-password"
      }
    }
  }
}
```

这一步我想强调一个设计原则：

> **让 Agent 面向 localhost，而不是面向集群拓扑。**

只要你保持这个原则，后面无论你是：

- 换 SSH host
- 换 namespace
- 换 Pod
- 换连接方式

本地 Agent 的心智模型都不会被污染。

---

## 七、压测时应该怎么用这条链路

很多人打通链路之后，马上就会陷入另一个误区：

> 既然 Agent 能调 Arthas 了，那就让它多调一些。

这不对。

在压测场景里，接入链路只是前提，真正决定分析质量的是诊断节奏。

### 建议顺序

#### 第 1 层：低侵入巡检

先让 Agent 做：

- `dashboard`
- `thread`
- `memory`
- `jvm`

这一层的目标是建立“系统态势感知”。

#### 第 2 层：方法级统计

如果确认某个接口异常，再让 Agent 用：

- `monitor`

这一步主要看：

- 调用次数
- RT 变化趋势
- 异常比例

#### 第 3 层：链路剖开

只有在已经锁定目标方法后，再考虑：

- `trace`
- `stack`
- `watch`

而且一定要缩小范围。

#### 第 4 层：重武器后置

像下面这些，要尽量放后面：

- `tt`
- `heapdump`
- `dump`
- `vmtool`

因为它们更容易引入额外开销，或者产生额外副作用。

---

## 八、最常见的五类故障，怎么排

这一段我觉得是实战里最有价值的部分。

### 故障 1：脚本能 SSH 上去，但找不到 Pod

常见原因：

- namespace 写错
- selector 写错
- 目标 Pod 不在 Running 状态
- 远端 kubectl context 不对

处理思路：

```bash
kubectl -n <namespace> get pods
kubectl -n <namespace> get pods -l 'app=xxx'
```

如果是多集群环境，优先补上：

```bash
--context <context>
```

### 故障 2：Pod 找到了，但 `/mcp` 没响应

这通常不是脚本问题，而是 Arthas 侧没准备好。

重点检查：

- Pod 内是否真的启动了 Arthas
- `arthas.mcpEndpoint=/mcp` 是否配置了
- `arthas.httpPort` 是否真的是 8563
- Arthas 是否只开了 telnet 没开 http

建议先在 Pod 内验证：

```bash
curl http://127.0.0.1:8563/mcp
```

### 故障 3：远端 port-forward 起来了，但本地 curl 不通

这时重点看 SSH 隧道。

常见原因：

- SSH 隧道没建起来
- 本地端口被占用
- SSH 连接中途断开
- 本地映射端口和远端桥接端口不一致

一个好习惯是显式改端口，比如：

```bash
--local-port 28563 --remote-port 28563
```

这样你可以快速排除端口冲突问题。

### 故障 4：链路之前是通的，压测中途突然断了

大概率是 Pod 重建了。

因为 `kubectl port-forward` 是绑 Pod 的，不是绑 Deployment 的。

这也是为什么在正式压测里，你最好：

- 固定分析实例
- 压测期间避免滚动发布
- 必要时把重连动作脚本化

### 故障 5：链路通了，但分析结论明显不对

这种情况非常常见，且经常被误判为“Arthas 不准”。

其实更常见的原因是：

- 你连错了 Pod
- 你分析的不是压测真正命中的实例
- Service 后面多个副本，你只看了一个正常副本

所以压测分析里，最需要尊重的一条原则是：

> **先证明这个实例正在承接你关注的流量，再谈诊断结论。**

---

## 九、脚本现在够不够用？够，但还可以继续进化

当前这个脚本已经足够解决：

- 单实例接入
- 压测前临时打通链路
- Agent 侧快速注册 MCP
- 常见链路验证

但如果你后面要更重度使用，我建议它还可以继续往下演进。

### 下一步值得加的能力

1. **列出所有匹配 Pod，让人选择**
2. **支持自动重连**
3. **把远端 port-forward 与本地 SSH 隧道做成后台守护进程**
4. **输出不同客户端的 MCP 配置模板**
5. **压测前后一键启停**
6. **记录最近连接过的环境和参数**

也就是说，今天它还是一个“连接脚本”，再往下走，它就会逐渐变成一个“诊断接入工具”。

---

## 十、结论

如果说上一篇解决的是“为什么这样接”，那么这一篇解决的是：

> **怎么把它真正做成一个能用、敢用、能复用的脚本化入口。**

从工程视角看，这件事的真正价值不只是省命令，而是把下面这条链路变成标准化动作：

```text
本地 Agent
  -> localhost MCP
  -> SSH
  -> kubectl port-forward
  -> Pod 内 Arthas MCP
```

这样一来，你的压测分析流程就会明显变顺：

- 连接方式可复用
- 环境复杂度被封装
- Agent 可以面向稳定入口工作
- 排障路径更清晰

最后还是那句话：

> **Arthas MCP 让 Agent 有了执行诊断的手，脚本化接入则让这双手真正够得着远端 K8s 里的 Java 服务。**

两者缺一不可。

---

## 配套资源

- 上一篇：《Arthas MCP + 远端 K8s 实战：让本地 Agent 在压测时直接分析 Java 服务》
- 配套脚本：`~/.openclaw/workspace/scripts/connect-arthas-mcp.sh`
- 官方文档：
  - <https://arthas.aliyun.com/doc/mcp-server.html>
  - <https://arthas.aliyun.com/doc/tunnel.html>
  - <https://arthas.aliyun.com/doc/arthas-properties.html>
