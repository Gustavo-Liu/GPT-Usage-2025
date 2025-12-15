# 修复部署问题

## 问题
部署失败：`Failed to get the SHA of the commit` - 说明 GitHub 仓库的 main 分支是空的。

## 解决方案

### 步骤 1: 推送代码到 GitHub

在终端执行以下命令：

```bash
cd "/Users/liuyingte/Json Explore"

# 初始化 git（如果还没有）
git init

# 添加所有必要文件
git add app.py Dockerfile requirements.txt index.html styles.css app.js website_metrics.json detailed_explanations.json .gitignore

# 提交
git commit -m "Add AI Usage Analytics Dashboard"

# 设置远程仓库
git remote add origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git
# 如果已存在，使用: git remote set-url origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git

# 设置主分支
git branch -M main

# 推送到 GitHub（可能需要 GitHub 认证）
git push -u origin main
```

**如果推送时需要认证**，可以使用以下方法：

1. **使用 GitHub CLI**:
   ```bash
   gh auth login
   git push -u origin main
   ```

2. **使用 Personal Access Token**:
   - 在 GitHub 设置中创建 Personal Access Token
   - 推送时使用 token 作为密码

3. **使用 SSH**:
   ```bash
   git remote set-url origin git@github.com:Gustavo-Liu/GPT-Usage-2025.git
   git push -u origin main
   ```

### 步骤 2: 验证代码已推送

访问 https://github.com/Gustavo-Liu/GPT-Usage-2025 确认文件已存在。

### 步骤 3: 重新部署

代码推送成功后，运行：

```bash
python3 deploy_now.py
```

或使用 curl:

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

## 一键修复脚本

也可以运行我创建的修复脚本：

```bash
python3 fix_and_deploy.py
```

这个脚本会自动执行上述所有步骤。

