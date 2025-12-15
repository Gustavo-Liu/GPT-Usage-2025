# AI 使用习惯分析网站

这是一个展示 AI 使用习惯分析结果的交互式网站。

## 📁 文件结构

```
.
├── index.html              # 主页面
├── styles.css              # 样式文件
├── app.js                  # JavaScript 逻辑和图表渲染
├── website_metrics.json    # 数据文件
└── README_WEBSITE.md       # 本文件
```

## 🚀 快速开始

### 方法 1: 使用 Python 本地服务器（推荐）

```bash
# Python 3
python3 -m http.server 8000

# 或 Python 2
python -m SimpleHTTPServer 8000
```

然后在浏览器中访问: http://localhost:8000

### 方法 2: 使用 Node.js http-server

```bash
# 安装 http-server (如果还没有)
npm install -g http-server

# 启动服务器
http-server -p 8000
```

### 方法 3: 直接打开（可能有限制）

由于浏览器的安全策略，直接双击 `index.html` 可能无法加载 JSON 数据。建议使用上述方法。

## 📊 网站功能

### 核心指标展示
- 总对话数、总消息数、使用天数
- 工具使用率、平均对话长度、技术深度指数

### 可视化图表
1. **对话类型分布** - 饼图展示不同类型对话的占比
2. **技术能力使用** - 柱状图展示代码、图片、工具、多模态的使用情况
3. **活跃时段分析** - 折线图展示 24 小时使用分布
4. **交互模式分布** - 饼图展示协作型、指导型、问答型的比例
5. **个性化能力雷达图** - 多维度能力展示

### 深度分析
- 用户画像分析
- 关键发现与洞察
- 个性化特点标签
- 专业领域画像

## 🎨 技术栈

- **HTML5** - 页面结构
- **CSS3** - 现代化样式（渐变、动画、响应式）
- **JavaScript** - 数据加载和交互
- **Chart.js** - 图表可视化库

## 📱 响应式设计

网站支持移动端、平板和桌面端，自适应不同屏幕尺寸。

## 🔧 自定义配置

### 修改数据

编辑 `website_metrics.json` 文件来更新数据。运行 `calculate_website_metrics.py` 可以重新计算所有指标。

### 修改样式

编辑 `styles.css` 文件中的 CSS 变量来自定义颜色主题：

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #ec4899;
    /* ... */
}
```

### 修改图表

编辑 `app.js` 文件中的图表配置函数来调整图表样式和选项。

## 📝 数据更新

如果对话数据更新了，运行以下命令重新生成数据：

```bash
# 重新生成指标数据
python3 calculate_website_metrics.py

# 重新生成对话总结（可选）
python3 generate_conversation_summaries.py
```

## 🌐 部署

### 部署到 GitHub Pages

1. 将所有文件推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 选择主分支作为源

### 部署到其他静态托管服务

- **Netlify**: 拖拽文件夹到 Netlify
- **Vercel**: 使用 Vercel CLI 或 GitHub 集成
- **Cloudflare Pages**: 连接 GitHub 仓库

## 📄 许可证

本项目仅供个人使用。

## 🆘 故障排除

### 图表不显示
- 检查浏览器控制台是否有错误
- 确认 `website_metrics.json` 文件存在且格式正确
- 确认使用 HTTP 服务器而非直接打开文件

### 样式不正常
- 检查浏览器是否支持 CSS 变量
- 清除浏览器缓存

### 数据不更新
- 确认已运行 `calculate_website_metrics.py` 重新生成数据
- 检查 `website_metrics.json` 文件时间戳

