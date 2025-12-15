# AI 使用习惯分析网站

这是一个展示 AI 使用习惯分析结果的交互式网站，基于 800 个对话、13,146 条消息的深度分析。

## 🚀 快速部署

### 1. 推送代码到 GitHub

**重要**: 部署前必须先推送代码到 GitHub！

```bash
cd "/Users/liuyingte/Json Explore"

# 初始化 git
git init

# 添加文件
git add app.py Dockerfile requirements.txt index.html styles.css app.js website_metrics.json detailed_explanations.json .gitignore README.md

# 提交
git commit -m "Add AI Usage Analytics Dashboard"

# 添加远程仓库
git remote add origin https://github.com/Gustavo-Liu/GPT-Usage-2025.git

# 设置主分支并推送
git branch -M main
git push -u origin main
```

### 2. 部署到 AI Builders

代码推送成功后，运行：

```bash
python3 deploy_now.py
```

或使用一键修复脚本（自动推送+部署）：

```bash
python3 fix_and_deploy.py
```

## 📁 项目结构

```
.
├── app.py                    # FastAPI 应用
├── Dockerfile                # Docker 配置
├── requirements.txt          # Python 依赖
├── index.html               # 主页面
├── styles.css               # 样式文件
├── app.js                   # JavaScript 逻辑
├── website_metrics.json     # 指标数据
├── detailed_explanations.json  # 详细说明数据
└── deploy_now.py            # 部署脚本
```

## 🌐 部署后访问

部署完成后（5-10 分钟），访问：
```
https://ai-usage-analytics.ai-builders.space
```

## 📊 网站功能

- 核心指标展示（对话数、消息数、使用天数等）
- 5 个交互式可视化图表
- 详细的指标说明和解释
- 用户画像分析
- 关键发现与洞察

## 🔧 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行本地服务器
python3 -m http.server 8000
# 或
python3 app.py
```

## 📝 故障排除

如果部署失败，请确保：
1. ✅ 代码已推送到 GitHub
2. ✅ GitHub 仓库是 Public
3. ✅ main 分支有代码提交
4. ✅ 所有必要文件都在仓库中

更多信息请查看 `FIX_DEPLOYMENT.md`
