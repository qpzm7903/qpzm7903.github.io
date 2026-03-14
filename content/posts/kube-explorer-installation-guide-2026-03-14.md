---
title: "kube-explorer：轻量级 Kubernetes Dashboard 替代方案"
date: 2026-03-14T12:00:00+08:00
draft: false
tags: ["Kubernetes", "Dashboard", "kube-explorer", "Docker Desktop"]
categories: ["工具推荐"]
description: "官方 Kubernetes Dashboard 在新版本 K8s 上存在兼容性问题，kube-explorer 是一个轻量、无依赖的替代方案，支持本地运行和集群部署。"
---

Kubernetes 官方 Dashboard 在 K8s 1.32 版本上存在兼容性问题（如 CronJob 页面 404）。如果你只需要一个简单的 Web UI 来管理本地 K8s 集群，kube-explorer 是一个轻量、无依赖的替代方案。

---

## 为什么选择 kube-explorer

| 特性 | kube-explorer | 官方 Dashboard |
|------|---------------|----------------|
| 依赖 | 单二进制，无依赖 | 需部署多个组件 |
| K8s 兼容性 | 广泛兼容 | 新版本存在兼容问题 |
| 安装方式 | 本地运行 / 集群部署 | 仅集群部署 |
| 认证 | 自动读取 kubeconfig | 需要 Token |

---

## 方式一：本地运行

适合 Docker Desktop / kind / minikube 等本地 K8s 环境。

### 下载并安装

```bash
# macOS (ARM64)
curl -sL -o ~/bin/kube-explorer "https://github.com/cnrancher/kube-explorer/releases/download/v0.3.0/kube-explorer-darwin-arm64"
chmod +x ~/bin/kube-explorer

# macOS (Intel)
curl -sL -o ~/bin/kube-explorer "https://github.com/cnrancher/kube-explorer/releases/download/v0.3.0/kube-explorer-darwin-amd64"
chmod +x ~/bin/kube-explorer

# Linux (amd64)
curl -sL -o /usr/local/bin/kube-explorer "https://github.com/cnrancher/kube-explorer/releases/download/v0.3.0/kube-explorer-linux-amd64"
chmod +x /usr/local/bin/kube-explorer
```

### 启动服务

```bash
kube-explorer --http-listen-port=9090 --https-listen-port=0
```

访问 http://localhost:9090 即可使用。

---

## 方式二：部署到 K8s 集群

适合生产环境，服务随集群自动启动，无需本地进程。

### 一键部署

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: kube-explorer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kube-explorer
  namespace: kube-explorer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kube-explorer
  template:
    metadata:
      labels:
        app: kube-explorer
    spec:
      serviceAccountName: kube-explorer
      containers:
      - name: kube-explorer
        image: cnrancher/kube-explorer:v0.3.0
        args:
        - --http-listen-port=9090
        - --https-listen-port=0
        ports:
        - containerPort: 9090
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: kube-explorer
  namespace: kube-explorer
spec:
  type: NodePort
  ports:
  - port: 9090
    targetPort: 9090
    nodePort: 30090
  selector:
    app: kube-explorer
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-explorer
  namespace: kube-explorer
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kube-explorer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kube-explorer
  namespace: kube-explorer
EOF
```

### 访问方式

```bash
# Docker Desktop / 本地集群
http://localhost:30090

# 远程集群（通过 kubectl port-forward）
kubectl port-forward -n kube-explorer svc/kube-explorer 9090:9090
# 然后访问 http://localhost:9090
```

---

## 验证部署状态

```bash
# 查看 Pod 状态
kubectl get pods -n kube-explorer

# 查看服务
kubectl get svc -n kube-explorer

# 查看日志
kubectl logs -n kube-explorer deployment/kube-explorer
```

---

## 卸载

```bash
kubectl delete namespace kube-explorer
kubectl delete clusterrolebinding kube-explorer
```

---

## 其他 Dashboard 替代方案

如果 kube-explorer 不满足需求，可以考虑：

| 项目 | Stars | 特点 |
|------|-------|------|
| **Headlamp** | 6k | CNCF 官方项目，插件系统，桌面应用 |
| **Kubewall** | 1.9k | AI 集成，单二进制部署 |
| **Kite** | 2.4k | AI 助手，OAuth，RBAC，中文支持 |
| **k9s** | 25k+ | 终端 UI，快捷键操作 |

---

*参考链接：*
- <https://github.com/cnrancher/kube-explorer>