# 需要提交到 GitHub 的文件清单

## ✅ 网站核心文件（必须提交）

这些是网站运行必需的文件：

1. `app.py` - FastAPI 应用
2. `Dockerfile` - Docker 配置
3. `requirements.txt` - Python 依赖
4. `index.html` - 主页面
5. `styles.css` - 样式文件
6. `app.js` - JavaScript 逻辑
7. `website_metrics.json` - 指标数据
8. `detailed_explanations.json` - 详细说明数据
9. `README.md` - 项目说明
10. `.gitignore` - Git 忽略配置
11. `deploy.py` - 部署脚本（安全，使用环境变量）

## ❌ 不要提交的文件

这些文件已在 `.gitignore` 中，不会被提交：

- `.env` - 包含 API token
- `conversations.json` - 原始数据（太大）
- `messages.csv`, `edges.csv` - 数据文件（太大）
- 各种包含 token 的部署脚本
- 分析和生成脚本（仅本地使用）
- 输出文件（analysis_output/, 各种 .md 文档）

## 🚀 快速提交命令

```bash
# 只添加核心文件
git add app.py Dockerfile requirements.txt index.html styles.css app.js
git add website_metrics.json detailed_explanations.json
git add README.md .gitignore deploy.py DEPLOYMENT.md

# 提交
git commit -m "Add AI Usage Analytics Dashboard"

# 推送到 GitHub
git push origin main
```

