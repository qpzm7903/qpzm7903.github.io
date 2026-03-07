# 科技热点日报

基于 [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主题的静态博客，聚焦中文科技热点资讯。

在线访问：<https://qpzm7903.github.io/>

## 快速开始

### 前置要求

- [Hugo Extended](https://gohugo.io/installation/)（推荐最新版本）
- Git

### 克隆项目

```bash
git clone --recurse-submodules https://github.com/qpzm7903/qpzm7903.github.io.git
cd qpzm7903.github.io
```

> 如果已经 clone 但忘记拉取子模块，执行：`git submodule update --init --recursive`

### 本地开发

```bash
# 启动本地服务器（含草稿预览）
hugo server -D
```

访问 http://localhost:1313 即可预览。

### 新建文章

```bash
hugo new posts/YYYY-MM-DD-title.md
```

文章 Front Matter 示例：

```yaml
---
title: "文章标题"
date: 2026-03-07T09:00:00+08:00
draft: false
tags: ["AI", "科技"]
categories: ["日报"]
---
```

将 `draft` 设为 `true` 可将文章标记为草稿，生产构建时不会包含。

### 发布文章

编辑完成后，提交并推送即可触发自动部署：

```bash
git add content/posts/你的文章.md
git commit -m "post: 文章标题"
git push
```

### 构建（可选，本地验证用）

```bash
hugo --minify
```

输出目录为 `public/`（已加入 `.gitignore`，不提交到仓库）。

## 部署

推送到 `master` 分支后，GitHub Actions 自动完成构建和部署：

1. `peaceiris/actions-hugo` 安装 Hugo Extended 并构建
2. `actions/deploy-pages` 发布到 GitHub Pages

GitHub Pages 配置为 **Actions 模式**，不从分支直接读取静态文件。

## 项目结构

```
hugo.yaml                  # 站点配置
content/
  posts/                   # 文章（Markdown）
  archives/_index.md       # 归档页
layouts/partials/
  extend_head.html         # 自定义 CSS/JS 注入
assets/css/
  custom.css               # 样式覆盖（TOC 右侧悬浮等）
themes/papermod/           # PaperMod 主题（git submodule，勿直接修改）
.github/workflows/
  hugo.yaml                # CI/CD 工作流
```

## 自定义扩展

通过 `layouts/partials/extend_head.html` 和 `assets/css/custom.css` 扩展主题，避免直接修改 `themes/papermod/` 目录，以便主题升级。

## 许可证

内容版权归作者所有。Hugo 框架和 PaperMod 主题遵循各自的开源许可证。
