# 部署指南

## 快速部署

### 方法 1: 使用部署脚本（推荐）

```bash
python3 deploy.py
```

脚本会自动：
1. 检查 git 仓库和远程 URL
2. 提示输入服务名称、分支、端口
3. 调用 AI Builders 部署 API
4. 显示部署状态和访问链接

### 方法 2: 使用 curl 直接调用

```bash
export AI_BUILDER_TOKEN=sk_126b30d3_e7e6c5293219d96a8ad79062639b0b9fbd20

curl -X POST "https://space.ai-builders.com/backend/v1/deployments" \
  -H "Authorization: Bearer $AI_BUILDER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "repo_url": "https://github.com/your-username/your-repo",
  "service_name": "ai-usage-analytics",
  "branch": "main",
  "port": 8000
}'
```

## 部署前准备

### 1. 确保代码已推送到 GitHub

```bash
# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Add AI Usage Analytics Dashboard"

# 添加远程仓库（替换为你的 GitHub 仓库）
git remote add origin https://github.com/your-username/your-repo.git

# 推送到 GitHub
git push -u origin main
```

### 2. 确保项目包含以下文件

- ✅ `app.py` - FastAPI 应用
- ✅ `Dockerfile` - Docker 配置
- ✅ `requirements.txt` - Python 依赖
- ✅ `index.html` - 主页面
- ✅ `styles.css` - 样式文件
- ✅ `app.js` - JavaScript 逻辑
- ✅ `website_metrics.json` - 数据文件
- ✅ `detailed_explanations.json` - 详细说明数据

### 3. 确保 .env 文件中有 API Token

```bash
AI_BUILDER_TOKEN=sk_126b30d3_e7e6c5293219d96a8ad79062639b0b9fbd20
```

## 部署步骤

### 步骤 1: 准备 GitHub 仓库

1. 在 GitHub 创建新仓库
2. 将代码推送到仓库

### 步骤 2: 运行部署

```bash
# 使用 Python 脚本
python3 deploy.py

# 或使用 bash 脚本
./deploy.sh
```

### 步骤 3: 等待部署完成

- 部署通常需要 5-10 分钟
- 访问 `https://your-service-name.ai-builders.space` 查看结果

## 验证部署

部署完成后，可以：

1. 访问网站：`https://your-service-name.ai-builders.space`
2. 检查健康状态：`https://your-service-name.ai-builders.space/health`
3. 查看部署状态（通过 API 或部署门户）

## 故障排除

### 部署失败

- 检查 Dockerfile 是否正确
- 确认所有依赖都在 requirements.txt 中
- 验证端口配置（默认为 8000）

### 网站无法访问

- 等待 5-10 分钟完成部署
- 检查部署状态是否为 HEALTHY
- 查看部署日志了解错误信息

### 静态文件加载失败

- 确认 index.html 中的路径使用 `/static/` 前缀
- 检查 app.js 中的 JSON 文件路径

