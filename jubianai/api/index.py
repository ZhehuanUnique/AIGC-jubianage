"""
Vercel Serverless Function 入口
将 FastAPI 应用适配为 Vercel Serverless Function
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

# 创建 FastAPI 应用
app = FastAPI(title="视频生成 API", version="1.0.0")

# 配置 CORS
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", 
    "*" if os.getenv("ENV") != "production" else "https://jubianai.cn,https://www.jubianai.cn,https://jubianai.streamlit.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "视频生成 API 服务", 
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "database": "not_configured"
    }

@app.get("/api/v1/assets/list")
async def list_assets():
    """获取所有资产（返回空列表）"""
    return {}

@app.get("/api/v1/assets/characters")
async def list_characters():
    """获取所有人物列表"""
    return {
        "characters": [],
        "count": 0
    }

# 使用 Mangum 将 FastAPI 适配为 ASGI
# 注意：Mangum 2.0+ 使用不同的 API
try:
    # 尝试使用新版本 API
    handler = Mangum(app, lifespan="off")
except:
    # 如果失败，使用旧版本 API
    handler = Mangum(app)
