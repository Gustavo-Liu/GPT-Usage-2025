# 部署指令

## 仓库信息
- **GitHub URL**: https://github.com/Gustavo-Liu/GPT-Usage-2025.git
- **服务名称**: ai-usage-analytics
- **分支**: main
- **端口**: 8000

## 部署步骤

### 步骤 1: 确保代码已推送到 GitHub

```bash
cd "/Users/liuyingte/Json Explore"

# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: AI Usage Analytics Dashboard"

# 添加远程仓库
git remote add origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git
# 如果已存在，使用: git remote set-url origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git

# 设置分支
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 步骤 2: 执行部署

运行以下命令：

```bash
curl -X POST "https://space.ai-builders.com/backend/v1/deployments" \
  -H "Authorization: Bearer sk_612ffd16_2f4afacbc641f99b6122dc696e4715dfc2b3" \
  -H "Content-Type: application/json" \
  -d '{
  "repo_url": "https://github.com/Gustavo-Liu/GPT-Usage-2025.git",
  "service_name": "ai-usage-analytics",
  "branch": "main",
  "port": 8000
}'
```

或者使用 Python 脚本：

```bash
python3 deploy_now.py
```

## 部署完成后

访问以下 URL 查看网站：
```
https://ai-usage-analytics.ai-builders.space
```

预计等待时间：5-10 分钟

