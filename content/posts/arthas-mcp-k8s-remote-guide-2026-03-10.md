---
title: "Arthas MCP + 远端 K8s 实战：让本地 Agent 在压测时直接分析 Java 服务"
date: 2026-03-10T14:05:00+08:00
draft: false
tags: ["Arthas", "MCP", "Kubernetes", "Java", "性能测试", "诊断", "Agent", "SSH"]
categories: ["Java 性能分析", "Kubernetes", "实战指南"]
description: "Arthas 官方推出 MCP Server 后，AI Agent 已经可以直接调用 Java 诊断能力。本文结合远端 Kubernetes 场景，系统讲清楚如何通过 SSH + kubectl port-forward 安全接入 Arthas MCP，并给出一键连接脚本与压测诊断建议。"
---

Arthas 最近放出了 **MCP Server** 能力。这个变化的意义，不只是“Arthas 多了一个新入口”，而是：

> **Java 诊断能力，第一次可以被本地 Agent 以标准工具协议直接调用。**

以前我们做性能测试，常见流程是这样的：

- 压测工具把流量打上去
- 我们盯着监控看 CPU、RT、GC
- 发现异常后，再 SSH 到机器里 attach Arthas
- 手工跑 `thread`、`dashboard`、`trace`、`watch`
- 最后把零散信息拼成结论

这个流程不是不能用，但它有两个问题：

1. **慢**：压测窗口很短，手工分析经常跟不上问题出现的节奏
2. **碎**：数据、判断和命令是割裂的，很难形成可复用流程

Arthas MCP 把这件事往前推进了一步：**AI Agent 可以直接把 Arthas 当工具调用。**

于是问题就变成了：

> 如果我的 Java 服务跑在远端 K8s 集群里，本地 Agent 怎么安全地连上远端 Arthas MCP，并在压测时参与分析？

这篇文章我想把这件事讲透，重点回答四个问题：

1. Arthas MCP 到底解决了什么问题
2. 远端 K8s 场景下，链路应该怎么设计
3. 最推荐的接入方式是什么
4. 我如何把这件事做成一键脚本，并真正用于压测分析

---

## 一、Arthas MCP 到底是什么

根据 Arthas 官方文档，**Arthas MCP Server** 是 Arthas 的实验性模块，实现了基于 **MCP（Model Context Protocol）** 的服务端能力，通过 **HTTP / Netty + JSON-RPC 2.0** 对外暴露工具接口。

这句话如果翻译成人话，其实就是：

- Arthas 不再只是一个命令行诊断工具
- 它开始变成一个 **可被 Agent 直接调用的工具服务**
- 支持 MCP 的客户端，可以像调别的工具一样去调 Arthas

官方文档里最关键的配置很简单：

```properties
arthas.mcpEndpoint=/mcp
arthas.httpPort=8563
```

如果配置了密码：

```properties
arthas.password=your-secure-password
```

客户端就需要带上 Bearer Token：

```http
Authorization: Bearer your-secure-password
```

也就是说，默认情况下，一个开启了 Arthas MCP 的服务端点通常长这样：

```text
http://127.0.0.1:8563/mcp
```

如果你的 Agent 支持 `streamableHttp` 类型的 MCP Server，那么它理论上就可以把这个地址注册进去，然后直接调用 Arthas 提供的诊断工具。

---

## 二、Arthas MCP 能让 Agent 分析什么

Arthas 官方给 MCP 暴露了 **26 个诊断工具**。从压测角度看，最有价值的不是“命令变多了”，而是这些命令被结构化了。

典型工具可以分成三层。

### 1. JVM 与运行时总览

- `dashboard`
- `thread`
- `memory`
- `jvm`
- `sysprop`
- `vmoption`

这一层解决的是“系统层感知”。

你要先回答：

- 现在是 CPU 高、GC 高、线程池打满，还是锁竞争？
- 是全局性抖动，还是个别线程/接口出问题？

### 2. 类和类加载分析

- `sc`
- `sm`
- `jad`
- `classloader`
- `dump`

这一层解决的是“运行时结构到底是什么”。

比如很多线上/压测环境里，实际加载的类、字节码版本、代理类情况，和你本地源码认知并不完全一致。

### 3. 方法级诊断

- `monitor`
- `stack`
- `trace`
- `watch`
- `tt`

这一层才是真正进入“性能问题定位”。

比如：

- 哪个接口真的慢
- 慢在方法内部哪一段
- 是数据库、RPC、锁还是业务逻辑
- 某些请求参数下才会触发异常耗时

所以 Arthas MCP 的价值，本质上不是“远程执行 Arthas”，而是：

> **让 Agent 具备了系统化的 Java 诊断能力。**

---

## 三、你的问题本质上不是命令问题，而是链路设计问题

你当前的前提是：

- Java 服务部署在远端 Kubernetes 集群
- 你手里有 master 节点 IP、用户密码、root 密码
- 你想让本地 Agent 连接远端 Arthas MCP
- 你计划在性能测试过程中做分析

这件事的难点，其实不在 Arthas 本身，而在**连接链路**。

因为对本地 Agent 来说，最理想的状态不是“它理解远端 K8s 拓扑”，而是：

> 它面前就有一个本地可访问的 MCP 地址。

从系统视角看，完整链路应该是这样：

```text
本地 Agent
  -> 本地 MCP 地址（localhost）
    -> SSH 隧道
      -> 可访问集群的远端主机（master / bastion）
        -> kubectl port-forward
          -> Pod 内 Arthas HTTP 端口
            -> /mcp
```

这意味着你真正要解决的是四件事：

1. Pod 里如何启用 Arthas MCP
2. 如何把 Pod 内 `/mcp` 安全带出来
3. 如何让本地 Agent 用“本地地址”接入它
4. 如何在压测时控制诊断扰动

---

## 四、远端 K8s 场景下，三种可行方案

### 方案 A：`kubectl port-forward` + SSH 隧道

这是我最推荐的方案，也是这篇文章真正要落地的方案。

结构很简单：

```text
本地 Agent
  -> http://127.0.0.1:18563/mcp
  -> ssh -L
  -> 远端 master / bastion
  -> kubectl port-forward pod/<pod-name> 18563:8563
  -> Pod 内 Arthas MCP
```

优点：

- 不需要把 Arthas 直接暴露到公网
- 对现有 K8s 改动最小
- 适合压测时临时打开、结束后关闭
- 安全边界清晰

缺点：

- Pod 重建后需要重新连接
- 多副本场景下要明确分析的是哪个实例

但对于“本地 Agent + 远端 K8s + 压测分析”这个问题，它依然是最稳的。

---

### 方案 B：内网 Service + 堡垒机 / VPN

如果你们已经有成熟内网网络，可以在集群内给 Arthas HTTP 端口暴露一个仅内网可达的 Service，然后让本地走 VPN、堡垒机或者代理访问。

这种方案更适合：

- 环境比较固定
- 需要较长期保留诊断入口
- 团队已经有平台能力

但它的复杂度在于：

- 多副本下路由到哪个实例
- 如何做权限和网络隔离
- 如何避免把高权限诊断口过度暴露

所以它不是我当前最推荐的起手式。

---

### 方案 C：Arthas Tunnel 负责“远程接入”，MCP 负责“Agent 调用”

Arthas 本身还有 Tunnel 能力，用来远程管理多个 Agent。

它解决的是：

- 多机器
- 多实例
- 跨网络
- 集中接入

而 MCP 解决的是：

- Agent 怎么调用 Arthas

换句话说：

- **Tunnel** 更偏“实例发现和远程接入”
- **MCP** 更偏“工具协议和 Agent 集成”

长期来看，Tunnel + MCP 可以形成更强的平台化方案；但如果你现在只是想尽快在压测里用起来，**先把单实例链路跑通更重要**。

---

## 五、为什么我推荐方案 A

因为它符合一个很重要的工程原则：

> **对 Agent 隐藏环境复杂度，对人保留连接控制权。**

对本地 Agent 来说，它只需要知道：

```text
http://127.0.0.1:18563/mcp
```

至于这个地址背后到底是：

- SSH
- 跳板机
- master 节点
- kubectl
- Pod 内转发

这些都属于连接层，不该污染 Agent 侧配置。

这件事的好处非常直接：

- Agent 配置更干净
- 切换环境更方便
- 连接方式以后可以替换，但 Agent 不需要跟着改

这其实就是“把系统边界画清楚”。

---

## 六、真正落地前，你需要先把服务端准备好

在 Pod 内或 Java 进程侧，你至少需要保证 Arthas 开启了 MCP。

一个最小配置如下：

```properties
arthas.mcpEndpoint=/mcp
arthas.httpPort=8563
arthas.password=replace-with-strong-password
arthas.disabledCommands=stop,dump
```

这里我建议特别注意两点。

### 1. 一定要开密码

Arthas MCP 本质上是高权限诊断入口，不应该裸奔。

### 2. 压测环境建议禁掉高风险命令

例如：

```properties
arthas.disabledCommands=stop,dump
```

如果你的目标只是压测分析，而不是线上热修、类字节码导出、强干预操作，就没必要把所有能力都开放出去。

先在 Pod 内验证：

```bash
curl -H "Authorization: Bearer replace-with-strong-password" \
  http://127.0.0.1:8563/mcp
```

只有这一步通了，后面的转发才有意义。

---

## 七、把这件事做成一键脚本

光讲方案没有意义，真正能落地的是脚本。

我这里写了一个脚本：

```text
scripts/connect-arthas-mcp.sh
```

它做四件事：

1. 通过 SSH 登录到远端 master / bastion
2. 在远端执行 `kubectl port-forward`
3. 在本地建立 `ssh -L` 隧道
4. 输出本地 MCP 地址和可直接复制的 MCP 配置片段

### 脚本特点

- 支持直接指定 `--pod`
- 支持通过 `--selector` 自动选择一个 Running Pod
- 支持 `--context`
- 支持自定义本地端口 / 远端端口
- 支持输出 Bearer Token 版 MCP 配置片段
- 支持 `--dry-run` 先看命令，不真正执行
- 退出时自动清理远端 `kubectl port-forward`

### 帮助命令

```bash
bash ~/.openclaw/workspace/scripts/connect-arthas-mcp.sh --help
```

### 示例 1：通过 selector 选 Pod

```bash
bash ~/.openclaw/workspace/scripts/connect-arthas-mcp.sh \
  --host 10.0.0.12 \
  --user ops \
  --namespace perf \
  --selector 'app=my-java-service' \
  --bearer-token 'your-secure-password'
```

### 示例 2：直接指定 Pod

```bash
bash ~/.openclaw/workspace/scripts/connect-arthas-mcp.sh \
  --host 10.0.0.12 \
  --user ops \
  --namespace perf \
  --pod myapp-7f6b5d8f5d-abcde \
  --local-port 28563 \
  --remote-port 28563 \
  --identity-file ~/.ssh/id_rsa \
  --bearer-token 'your-secure-password'
```

如果一切正常，脚本会输出类似结果：

```text
本地 MCP 地址: http://127.0.0.1:18563/mcp
```

同时会给出可直接复制的配置片段。

---

## 八、本地 Agent 怎么注册这个 MCP

如果你的客户端支持 `streamableHttp`，配置通常像这样：

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

这一步的关键不是配置语法，而是一个观念：

> **Agent 不应该直接理解 K8s，它只应该看到一个稳定的、本地可访问的 MCP 地址。**

这样才能把环境复杂度留在连接层，把诊断逻辑留给 Agent。

---

## 九、压测时如何正确使用 Arthas MCP

很多人一提压测分析，第一反应就是：

- 直接 `trace`
- 不行再 `watch`
- 还不够就 `tt`

这其实很容易把诊断本身变成额外扰动。

真正更合理的做法是“逐级加码”。

### 第一层：低侵入总览

先看：

1. `dashboard`
2. `thread`
3. `memory`
4. `jvm`

目标是快速判断问题属于哪一类：

- CPU 型
- 线程型
- GC 型
- 锁竞争型
- I/O 型

### 第二层：方法级统计

当你已经知道哪个接口异常，再上：

- `monitor`

因为它更适合看趋势，侵入性比直接大规模 `trace` 小得多。

### 第三层：热点链路剖开

锁定到具体类/方法后，再用：

- `trace`
- `stack`
- `watch`

但一定要控制范围：

- 限定类名
- 限定方法名
- 限定条件
- 限定次数

### 第四层：谨慎使用高干预工具

例如：

- `tt`
- `heapdump`
- `vmtool`
- `dump`

这些工具不是不能用，而是更适合在：

- 问题复现后做补充分析
- 非峰值时段做深入采样
- 有明确目标时短时使用

一句话：

> **Arthas 在压测里应该像手术刀，不应该像电锯。**

---

## 十、K8s 场景下几个特别容易踩的坑

### 1. 分析错 Pod

这大概是最常见的坑。

你压的是 Service，但你连的是某个随机 Pod。结果你看到一切正常，只是因为真正出问题的不是这个实例。

所以压测分析里，最重要的不是“有没有数据”，而是：

> **数据是不是来自真正被压中的那台实例。**

### 2. Pod 重建导致链路失效

`kubectl port-forward` 是绑定 Pod 的。Pod 一重建，转发就断了。

这也是为什么脚本化很重要，因为你迟早要面对重连。

### 3. 把 Arthas 直接暴露到公网

这很危险，不建议。

Arthas MCP 是高权限诊断口，应该：

- 只监听内网
- 通过 SSH / VPN / 堡垒机访问
- 开启密码
- 必要时禁掉部分高风险命令

### 4. 诊断本身污染压测结果

如果你在高并发阶段大规模跑 `trace`、`watch`、`tt`，那么你最终拿到的性能数据，很可能已经掺进了诊断开销。

所以一个成熟流程应该是：

- 压测前：做轻量基线检查
- 压测中：低侵入观察 + 短时深入分析
- 压测后：对问题实例做更重的补充诊断

---

## 十一、我建议的落地路径

如果你现在马上要用，我建议按三个阶段推进。

### 阶段 1：先打通单实例

目标很简单：

- 让本地 Agent 成功连接远端某个 Pod 的 Arthas MCP
- 能稳定执行 `dashboard`、`thread`、`monitor`

### 阶段 2：把连接流程脚本化

也就是本文里的 `connect-arthas-mcp.sh`。

这样压测前只需要执行一次脚本，就能拿到一个本地 MCP 地址。

### 阶段 3：多实例 / 多环境时再考虑 Tunnel

当你的需求变成：

- 多服务
- 多环境
- 多 Pod
- 多压测任务并发

再考虑引入 Arthas Tunnel 做统一管理。

顺序不要反。**先解决连接，再解决平台化。**

---

## 十二、结论

如果一句话总结这篇文章：

> **远端 K8s 里的 Arthas MCP，不应该直接暴露给本地 Agent，而应该通过 SSH + kubectl port-forward，在本地制造一个安全、稳定、看起来像本地的 MCP 地址。**

这是当前最实用、最容易控制风险、也最适合压测场景的方案。

而真正让它具备工程价值的，不是某条命令，而是下面这套完整思路：

- 用 Arthas MCP 把 Java 诊断能力工具化
- 用 SSH + port-forward 把远端复杂度封装掉
- 用脚本把连接流程固化
- 用分层诊断的方法减少压测扰动

Arthas MCP 让 Agent 第一次真正有机会成为“诊断执行者”，而不只是“诊断建议者”。

如果这套链路跑顺了，你的压测分析方式会发生一个很明显的变化：

- 以前是人盯图、敲命令、拼结论
- 以后会逐渐变成：**人定义目标，Agent 帮你执行诊断链路并汇总证据**

这才是它真正有意思的地方。

---

## 附：脚本路径

本文配套脚本：

```text
~/.openclaw/workspace/scripts/connect-arthas-mcp.sh
```

---

## 参考资料

- Arthas MCP Server 官方文档：<https://arthas.aliyun.com/doc/mcp-server.html>
- Arthas Tunnel 官方文档：<https://arthas.aliyun.com/doc/tunnel.html>
- Arthas Properties 官方文档：<https://arthas.aliyun.com/doc/arthas-properties.html>
