#!/bin/bash
# 推送代码到 GitHub 并重新部署

set -e

echo "=========================================="
echo "🚀 推送代码并部署"
echo "=========================================="

cd "/Users/liuyingte/Json Explore"

# 检查 git 是否初始化
if [ ! -d ".git" ]; then
    echo "初始化 git 仓库..."
    git init
fi

# 添加文件
echo ""
echo "📦 添加文件到 git..."
git add app.py Dockerfile requirements.txt index.html styles.css app.js website_metrics.json detailed_explanations.json .gitignore DEPLOY.md README.md 2>/dev/null || true
git add -A

# 提交
echo ""
echo "💾 提交更改..."
git commit -m "Add AI Usage Analytics Dashboard - FastAPI app with static files" || echo "没有新更改或已提交"

# 设置远程仓库
echo ""
echo "🔗 设置远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git

# 设置主分支
echo ""
echo "🌿 设置主分支..."
git branch -M main 2>/dev/null || true

# 推送
echo ""
echo "⬆️  推送到 GitHub..."
git push -u origin main --force || {
    echo "❌ 推送失败，可能需要设置 GitHub 认证"
    echo "请手动执行: git push -u origin main"
    exit 1
}

echo ""
echo "✅ 代码已推送到 GitHub!"
echo ""
echo "⏳ 等待 10 秒后开始部署..."
sleep 10

# 部署
echo ""
echo "🚀 开始部署..."
python3 deploy_now.py

