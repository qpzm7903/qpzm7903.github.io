#!/bin/bash
# 发布日报到博客并推送

cd ~/OpenClaw-Blog

# 获取今天的日期
TODAY=$(date +%Y-%m-%d)
SOURCE_FILE=~/.openclaw/workspace/AI-Share/daily-news-${TODAY}.md
TARGET_FILE=content/posts/daily-news-${TODAY}.md

# 检查源文件是否存在
if [ ! -f "$SOURCE_FILE" ]; then
    echo "错误：找不到日报文件 $SOURCE_FILE"
    exit 1
fi

# 复制文件
cp "$SOURCE_FILE" "$TARGET_FILE"
echo "✅ 已复制日报到博客"

# 检查是否需要添加 front matter
if ! grep -q "^---" "$TARGET_FILE"; then
    # 添加 front matter
    TEMP_FILE=$(mktemp)
    cat > "$TEMP_FILE" << 'EOF'
---
title: "📰 科技热点日报"
date: DATE_PLACEHOLDERT00:00:00+08:00
draft: false
tags: ["AI", "科技", "日报"]
categories: ["日报"]
---

EOF
    sed "s/DATE_PLACEHOLDER/$TODAY/" "$TEMP_FILE" > "${TEMP_FILE}.tmp"
    cat "${TEMP_FILE}.tmp" "$TARGET_FILE" > "${TARGET_FILE}.new"
    mv "${TARGET_FILE}.new" "$TARGET_FILE"
    rm -f "$TEMP_FILE" "${TEMP_FILE}.tmp"
    echo "✅ 已添加 front matter"
fi

# 构建
hugo --minify
echo "✅ Hugo 构建完成"

# 提交并推送
git add -A
git commit -m "发布日报 ${TODAY}"
git push
echo "✅ 已推送到 GitHub"

echo ""
echo "📱 博客地址：https://qpzm7903.github.io/"