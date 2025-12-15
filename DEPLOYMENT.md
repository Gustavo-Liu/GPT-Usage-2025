# 部署说明

## 网站核心文件（需要上传到 GitHub）

以下文件需要提交到 GitHub 仓库：

```
✅ app.py                    # FastAPI 应用
✅ Dockerfile                # Docker 配置
✅ requirements.txt          # Python 依赖
✅ index.html               # 主页面
✅ styles.css               # 样式文件
✅ app.js                   # JavaScript 逻辑
✅ website_metrics.json     # 指标数据
✅ detailed_explanations.json  # 详细说明数据
✅ README.md                # 项目说明
✅ .gitignore               # Git 忽略文件
✅ deploy.py                # 部署脚本（使用环境变量）
```

## 部署前准备

### 1. 设置环境变量

在 `.env` 文件中设置（本地文件，不上传）：
```
AI_BUILDER_TOKEN=your_token_here
```

### 2. 推送代码到 GitHub

```bash
cd "/Users/liuyingte/Json Explore"

# 初始化 git（如果还没有）
git init

# 只添加网站核心文件
git add app.py Dockerfile requirements.txt index.html styles.css app.js
git add website_metrics.json detailed_explanations.json
git add README.md .gitignore deploy.py

# 提交
git commit -m "Add AI Usage Analytics Dashboard"

# 设置远程仓库
git remote add origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git
git branch -M main

# 推送（确保仓库是 Public）
git push -u origin main
```

### 3. 执行部署

```bash
# 使用 Python 脚本（从 .env 读取 token）
python3 deploy.py

# 或使用 bash 脚本（需要设置环境变量）
export AI_BUILDER_TOKEN=your_token
./deploy.sh
```

## 部署配置

- **仓库 URL**: https://github.com/Gustavo-Liu/GPT-Usage-2025.git
- **服务名称**: ai-usage-analytics
- **分支**: main
- **端口**: 8000

## 部署后访问

等待 5-10 分钟后访问：
```
https://ai-usage-analytics.ai-builders.space
```

## ⚠️ 重要提示

- **不要**提交包含 API token 的文件到 Git
- `.env` 文件已在 `.gitignore` 中
- 部署脚本使用环境变量读取 token
- 确保 GitHub 仓库是 **Public**

