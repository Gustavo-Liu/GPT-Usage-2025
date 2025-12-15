#!/bin/bash
# 部署脚本 - 使用 AI Builders 部署 API

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}准备部署 AI 使用习惯分析网站...${NC}"

# 检查环境变量
if [ -z "$AI_BUILDER_TOKEN" ]; then
    echo -e "${RED}错误: 未找到 AI_BUILDER_TOKEN 环境变量${NC}"
    echo "请设置: export AI_BUILDER_TOKEN=your_token"
    exit 1
fi

# 检查是否在 git 仓库中
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}警告: 当前目录不是 git 仓库${NC}"
    echo "部署需要将代码推送到 GitHub 仓库"
    read -p "是否要初始化 git 仓库? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit: AI Usage Analytics Dashboard"
        echo -e "${YELLOW}请先推送到 GitHub，然后提供仓库 URL${NC}"
        exit 1
    else
        exit 1
    fi
fi

# 获取 GitHub 仓库 URL
REPO_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REPO_URL" ]; then
    echo -e "${YELLOW}未找到 git remote origin${NC}"
    read -p "请输入 GitHub 仓库 URL: " REPO_URL
fi

# 默认配置
SERVICE_NAME="${SERVICE_NAME:-ai-usage-analytics}"
BRANCH="${BRANCH:-main}"
PORT="${PORT:-8000}"

echo -e "${GREEN}部署配置:${NC}"
echo "  仓库 URL: $REPO_URL"
echo "  服务名称: $SERVICE_NAME"
echo "  分支: $BRANCH"
echo "  端口: $PORT"
echo ""

read -p "确认部署? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消部署"
    exit 0
fi

# 调用部署 API
echo -e "${YELLOW}正在部署...${NC}"

RESPONSE=$(curl -s -X POST "https://space.ai-builders.com/backend/v1/deployments" \
  -H "Authorization: Bearer $AI_BUILDER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
  \"repo_url\": \"$REPO_URL\",
  \"service_name\": \"$SERVICE_NAME\",
  \"branch\": \"$BRANCH\",
  \"port\": $PORT
}")

echo -e "${GREEN}部署响应:${NC}"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"

echo ""
echo -e "${GREEN}部署已提交！${NC}"
echo "请等待 5-10 分钟完成部署"
echo "部署完成后访问: https://${SERVICE_NAME}.ai-builders.space"

