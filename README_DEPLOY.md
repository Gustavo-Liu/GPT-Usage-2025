# 部署说明

## 准备部署

项目已准备好部署，包含：
- ✅ `app.py` - FastAPI 应用
- ✅ `Dockerfile` - Docker 配置  
- ✅ `requirements.txt` - Python 依赖
- ✅ 所有网站文件（HTML, CSS, JS, JSON）

## 部署步骤

### 1. 确保代码已推送到 GitHub

```bash
# 如果还没有 git 仓库
git init
git add .
git commit -m "AI Usage Analytics Dashboard"

# 添加远程仓库（替换为你的 GitHub 仓库 URL）
git remote add origin https://github.com/your-username/your-repo.git

# 推送到 GitHub
git push -u origin main
```

### 2. 使用部署脚本

```bash
python3 quick_deploy.py
```

脚本会提示输入：
- GitHub 仓库 URL
- 服务名称（默认：ai-usage-analytics）
- 分支（默认：main）
- 端口（默认：8000）

### 3. 或直接使用 curl

```bash
curl -X POST "https://space.ai-builders.com/backend/v1/deployments" \
  -H "Authorization: Bearer sk_612ffd16_2f4afacbc641f99b6122dc696e4715dfc2b3" \
  -H "Content-Type: application/json" \
  -d '{
  "repo_url": "https://github.com/your-username/your-repo",
  "service_name": "ai-usage-analytics",
  "branch": "main",
  "port": 8000
}'
```

### 4. 等待部署完成

部署通常需要 5-10 分钟。完成后访问：
```
https://your-service-name.ai-builders.space
```

## 重要提示

1. **GitHub 仓库必须是公开的**（Public）
2. **确保所有必要文件都在仓库中**（app.py, Dockerfile, 网站文件等）
3. **不要提交敏感文件**（.env 已在 .gitignore 中）
4. **确保 main 分支包含最新代码**

## 验证部署

部署后可以通过以下方式验证：

1. **健康检查**：
   ```
   curl https://your-service-name.ai-builders.space/health
   ```

2. **访问网站**：
   打开浏览器访问部署 URL

3. **查看部署状态**（如果 API 返回了部署信息）

