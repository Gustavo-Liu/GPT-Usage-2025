"""
FastAPI 应用 - 提供 AI 使用习惯分析网站
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

app = FastAPI(title="AI Usage Analytics Dashboard")

# 获取项目根目录
BASE_DIR = Path(__file__).parent

# 挂载静态文件目录，支持所有静态资源
app.mount("/static", StaticFiles(directory=str(BASE_DIR)), name="static")

@app.get("/")
async def read_root():
    """返回主页面"""
    index_path = BASE_DIR / "index.html"
    return FileResponse(index_path)

# 为 JSON 和其他静态文件添加路由
@app.get("/{filename}")
async def serve_static(filename: str):
    """提供静态文件（CSS, JS, JSON）"""
    file_path = BASE_DIR / filename
    
    # 只允许特定的文件类型
    allowed_extensions = {'.css', '.js', '.json', '.png', '.jpg', '.svg', '.ico'}
    if file_path.suffix not in allowed_extensions:
        return {"error": "File not found"}, 404
    
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}, 404

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

