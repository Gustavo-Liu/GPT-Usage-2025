FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY app.py .
COPY index.html .
COPY styles.css .
COPY app.js .
COPY website_metrics.json .
COPY detailed_explanations.json .

# 暴露端口（使用 PORT 环境变量）
EXPOSE 8000

# 启动应用
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"

