# AI 使用习惯分析网站

这是一个展示 AI 使用习惯分析结果的交互式网站，基于 800 个对话、13,146 条消息的深度分析。

## 📁 项目结构

### 网站核心文件
- `app.py` - FastAPI 应用（提供静态网站服务）
- `Dockerfile` - Docker 配置
- `requirements.txt` - Python 依赖
- `index.html` - 主页面
- `styles.css` - 样式文件
- `app.js` - JavaScript 逻辑和图表渲染
- `website_metrics.json` - 指标数据
- `detailed_explanations.json` - 详细说明数据

### 数据分析脚本（本地使用，不部署）
- `json_to_dataset.py` - JSON 转数据集
- `calculate_website_metrics.py` - 计算网站指标
- `analyze_usage_patterns.py` - 分析使用模式

## 🚀 部署

### 前提条件

1. **代码已推送到 GitHub**（仓库必须是 Public）
2. **设置环境变量**：在 `.env` 文件中配置 `AI_BUILDER_TOKEN`

### 部署步骤

```bash
# 1. 确保代码已推送
git add .
git commit -m "Add AI Usage Analytics Dashboard"
git push origin main

# 2. 运行部署脚本（使用环境变量中的 token）
python3 deploy.py
```

### 部署后访问

等待 5-10 分钟后，访问：
```
https://ai-usage-analytics.ai-builders.space
```

## 🔧 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 FastAPI 应用
python3 app.py

# 或使用 Python HTTP 服务器（仅前端）
python3 -m http.server 8000
```

## 📊 网站功能

- 核心指标展示（总对话数、消息数、使用天数等）
- 5 个交互式可视化图表
- 详细的指标说明和解释
- 用户画像分析
- 关键发现与洞察

## 🔒 安全提示

- ⚠️ **不要**将包含 API token 的文件提交到 Git
- ✅ `.env` 文件已在 `.gitignore` 中
- ✅ 部署脚本使用环境变量读取 token

## 📝 数据更新

如果需要更新数据：

```bash
# 重新生成指标
python3 calculate_website_metrics.py

# 重新生成对话总结（需要 API token）
python3 generate_conversation_summaries.py
```
