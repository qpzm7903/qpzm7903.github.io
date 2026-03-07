# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Hugo 静态博客，使用 PaperMod 主题，部署在 `https://qpzm7903.github.io/`。内容以中文科技日报为主。

## 常用命令

```bash
# 本地开发预览（含草稿）
hugo server -D

# 构建生产版本
hugo --minify

# 新建文章
hugo new posts/YYYY-MM-DD-title.md
```

## 部署

推送到 `master` 分支后，`.github/workflows/hugo.yaml` 自动触发：
1. 用 `peaceiris/actions-hugo` 构建
2. 用 `actions/upload-pages-artifact` + `actions/deploy-pages` 发布

GitHub Pages 配置为 **Actions 模式**（`build_type: workflow`），不从分支读取，必须通过 `actions/deploy-pages` 触发。

## 架构

```
hugo.yaml              # 站点配置（baseURL、菜单、主题参数）
content/
  posts/               # 文章，Markdown 格式
  archives/_index.md   # 归档页
themes/papermod/       # git submodule，不要直接修改
layouts/partials/
  extend_head.html     # 注入自定义 CSS 和强制展开 TOC 的 JS
assets/css/
  custom.css           # TOC 样式覆盖（右侧悬浮、始终展开）
```

PaperMod 主题通过 `layouts/partials/extend_head.html` 和 `assets/css/custom.css` 扩展，避免直接修改 `themes/papermod/`。

## 文章 Front Matter

```yaml
---
title: "文章标题"
date: 2026-03-07T09:00:00+08:00
draft: false
tags: ["AI", "科技"]
categories: ["日报"]
---
```

`draft: true` 的文章不会被构建到生产版本，本地用 `hugo server -D` 可预览。
