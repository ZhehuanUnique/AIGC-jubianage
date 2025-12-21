"""
后端 API 服务
使用 FastAPI 框架，后续接入 Seedance 1.0 Fast
"""
from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
import httpx
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_KEY, SEEDANCE_API_ENDPOINT, DEFAULT_VIDEO_SETTINGS
from backend.database import get_db, init_db
from backend.assets_api import (
    upload_asset, get_assets_by_character, delete_asset, 
    get_asset_path, AssetMetadata
)

app = FastAPI(title="视频生成 API", version="1.0.0")

# 配置 CORS
# 生产环境应该限制特定域名，开发环境允许所有
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", 
    "*" if os.getenv("ENV") != "production" else "https://jubianai.cn,https://www.jubianai.cn"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注意：Vercel Serverless Functions 不支持 startup 事件
# 数据库初始化会在第一次请求时自动进行（通过 get_db() 延迟初始化）


class VideoGenerationRequest(BaseModel):
    """视频生成请求模型"""
    prompt: str  # 文本提示词
    width: Optional[int] = DEFAULT_VIDEO_SETTINGS["width"]
    height: Optional[int] = DEFAULT_VIDEO_SETTINGS["height"]
    duration: Optional[int] = DEFAULT_VIDEO_SETTINGS["duration"]
    fps: Optional[int] = DEFAULT_VIDEO_SETTINGS["fps"]
    seed: Optional[int] = None
    negative_prompt: Optional[str] = None
    api_key: Optional[str] = None  # 前端传入的 API Key


class VideoGenerationResponse(BaseModel):
    """视频生成响应模型"""
    success: bool
    task_id: Optional[str] = None
    video_url: Optional[str] = None
    message: str
    error: Optional[str] = None


@app.get("/")
async def root():
    """根路径"""
    return {"message": "视频生成 API 服务", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 尝试初始化数据库（如果还没有初始化）
        from backend.database import init_db, get_engine
        try:
            engine = get_engine()
            # 测试数据库连接
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            init_db()  # 确保表已创建
            return {
                "status": "healthy",
                "database": "connected"
            }
        except Exception as e:
            return {
                "status": "healthy",
                "database": "disconnected",
                "error": str(e)
            }
    except Exception as e:
        return {
            "status": "healthy",
            "database": "error",
            "error": str(e)
        }


@app.post("/api/v1/video/generate", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """
    生成视频接口
    
    后续接入 Seedance 1.0 Fast API
    """
    # 使用请求中的 API Key 或配置文件中的 API Key
    api_key = request.api_key or API_KEY
    
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="API Key 未配置，请在配置文件中设置或通过请求传入"
        )
    
    if not request.prompt:
        raise HTTPException(
            status_code=400,
            detail="提示词不能为空"
        )
    
    try:
        # TODO: 接入 Seedance 1.0 Fast API
        # 目前返回模拟响应
        # 实际接入时，需要根据 Seedance API 文档进行调用
        
        # 示例调用（需要根据实际 API 文档调整）:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         SEEDANCE_API_ENDPOINT,
        #         headers={
        #             "Authorization": f"Bearer {api_key}",
        #             "Content-Type": "application/json"
        #         },
        #         json={
        #             "prompt": request.prompt,
        #             "width": request.width,
        #             "height": request.height,
        #             "duration": request.duration,
        #             "fps": request.fps,
        #             "seed": request.seed,
        #             "negative_prompt": request.negative_prompt,
        #         },
        #         timeout=300.0
        #     )
        #     result = response.json()
        
        # 模拟响应
        task_id = f"task_{hash(request.prompt) % 1000000}"
        
        return VideoGenerationResponse(
            success=True,
            task_id=task_id,
            message="视频生成任务已提交",
        )
        
    except Exception as e:
        return VideoGenerationResponse(
            success=False,
            message="视频生成失败",
            error=str(e)
        )


@app.get("/api/v1/video/status/{task_id}")
async def get_video_status(task_id: str):
    """
    查询视频生成状态
    
    后续接入 Seedance 1.0 Fast API 的状态查询接口
    """
    # TODO: 接入实际的状态查询 API
    return {
        "task_id": task_id,
        "status": "processing",  # processing, completed, failed
        "progress": 50,
        "video_url": None,
    }


# ========== 资产管理 API ==========

@app.post("/api/v1/assets/upload", response_model=AssetMetadata)
async def upload_asset_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传资产文件
    
    文件名格式：人物名-视图类型.扩展名
    例如：小明-正视图.jpg, 小美-侧视图.png
    
    注意：在 Vercel Serverless 环境中，文件应该先上传到云存储，
    然后通过 file_url 参数传入。这里只存储元数据。
    """
    try:
        asset = await upload_asset(file, db=db)
        return asset
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/assets/list")
async def list_assets(db: Session = Depends(get_db)):
    """获取所有资产，按人物分组（从数据库）"""
    try:
        assets_by_character = get_assets_by_character(db=db)
        
        # 转换为 JSON 可序列化格式
        result = {}
        for character, assets in assets_by_character.items():
            result[character] = [asset.dict() for asset in assets]
        
        return result
    except Exception as e:
        # 如果出错，返回空结果而不是 500 错误
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error listing assets: {error_msg}")
        print(traceback_str)
        # 返回空结果，避免 500 错误
        return {}


@app.get("/api/v1/assets/characters")
async def list_characters(db: Session = Depends(get_db)):
    """获取所有人物列表（从数据库）"""
    try:
        assets_by_character = get_assets_by_character(db=db)
        return {
            "characters": list(assets_by_character.keys()),
            "count": len(assets_by_character)
        }
    except Exception as e:
        print(f"Error listing characters: {e}")
        return {"characters": [], "count": 0}


@app.get("/api/v1/assets/{filename:path}")
async def get_asset(filename: str, db: Session = Depends(get_db)):
    """
    获取资产文件
    
    如果 file_url 是完整 URL，重定向到该 URL
    如果是本地路径，返回文件（仅开发环境）
    """
    file_path_or_url = get_asset_path(filename, db=db)
    
    if not file_path_or_url:
        raise HTTPException(status_code=404, detail="资产文件不存在")
    
    # 如果是 URL，重定向
    if file_path_or_url.startswith(('http://', 'https://')):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=file_path_or_url)
    
    # 如果是本地路径，返回文件（仅开发环境）
    file_path = Path(file_path_or_url)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="资产文件不存在")
    
    # 根据文件扩展名确定媒体类型
    ext = file_path.suffix.lower()
    media_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    media_type = media_type_map.get(ext, 'image/jpeg')
    
    return FileResponse(path=file_path, media_type=media_type)


@app.delete("/api/v1/assets/{filename:path}")
async def delete_asset_endpoint(filename: str, db: Session = Depends(get_db)):
    """删除资产（从数据库）"""
    try:
        success = delete_asset(filename, db=db)
        
        if not success:
            raise HTTPException(status_code=404, detail="资产文件不存在")
        
        return {"success": True, "message": "资产已删除"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除资产失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT
    
    uvicorn.run(app, host=HOST, port=PORT)

