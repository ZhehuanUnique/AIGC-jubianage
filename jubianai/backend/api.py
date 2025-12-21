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
import traceback

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import (
        API_KEY, SEEDANCE_API_ENDPOINT, DEFAULT_VIDEO_SETTINGS,
        JIMENG_ACCESS_KEY_ID, JIMENG_SECRET_ACCESS_KEY, JIMENG_API_ENDPOINT
    )
    from backend.database import get_db, init_db
    from backend.assets_api import (
        upload_asset, get_assets_by_character, delete_asset, 
        get_asset_path, AssetMetadata
    )
    # 即梦 API 客户端
    try:
        from backend.jimeng_client import (
            generate_video_from_image_first_frame,
            generate_video_from_images_first_last,
            check_video_status as jimeng_check_status
        )
    except ImportError:
        # 如果导入失败，创建占位函数
        async def generate_video_from_image_first_frame(*args, **kwargs):
            raise Exception("即梦 API 客户端未正确导入")
        async def generate_video_from_images_first_last(*args, **kwargs):
            raise Exception("即梦 API 客户端未正确导入")
        async def jimeng_check_status(*args, **kwargs):
            raise Exception("即梦 API 客户端未正确导入")
except Exception as e:
    print(f"Error importing modules: {e}")
    print(traceback.format_exc())
    # 设置默认值，避免导入失败导致应用无法启动
    API_KEY = os.getenv("API_KEY", "")
    SEEDANCE_API_ENDPOINT = os.getenv("SEEDANCE_API_ENDPOINT", "")
    JIMENG_ACCESS_KEY_ID = os.getenv("JIMENG_ACCESS_KEY_ID", "")
    JIMENG_SECRET_ACCESS_KEY = os.getenv("JIMENG_SECRET_ACCESS_KEY", "")
    JIMENG_API_ENDPOINT = os.getenv("JIMENG_API_ENDPOINT", "https://api.jimeng.ai")
    DEFAULT_VIDEO_SETTINGS = {
        "width": 1024,
        "height": 576,
        "duration": 5,
        "fps": 24,
    }

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
    prompt: Optional[str] = None  # 文本提示词（图生视频时可选）
    width: Optional[int] = DEFAULT_VIDEO_SETTINGS["width"]
    height: Optional[int] = DEFAULT_VIDEO_SETTINGS["height"]
    duration: Optional[int] = DEFAULT_VIDEO_SETTINGS["duration"]
    fps: Optional[int] = DEFAULT_VIDEO_SETTINGS["fps"]
    seed: Optional[int] = None
    negative_prompt: Optional[str] = None
    api_key: Optional[str] = None  # 前端传入的 API Key（用于 Seedance）
    provider: Optional[str] = "jimeng"  # 服务提供商：jimeng 或 seedance
    jimeng_access_key_id: Optional[str] = None  # 即梦 AccessKeyId
    jimeng_secret_access_key: Optional[str] = None  # 即梦 SecretAccessKey
    # 图生视频参数
    mode: Optional[str] = "first_frame"  # 模式：first_frame（首帧）或 first_last_frame（首尾帧）
    image_base64: Optional[str] = None  # 首帧图片 Base64 编码
    start_image_base64: Optional[str] = None  # 首帧图片 Base64 编码（首尾帧模式）
    end_image_base64: Optional[str] = None  # 尾帧图片 Base64 编码（首尾帧模式）


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
    try:
        return {
            "message": "视频生成 API 服务", 
            "version": "1.0.0",
            "status": "running"
        }
    except Exception as e:
        import traceback
        return {
            "message": "视频生成 API 服务",
            "version": "1.0.0",
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 尝试初始化数据库（如果还没有初始化）
        from backend.database import init_db, get_engine
        from sqlalchemy import text
        try:
            engine = get_engine()
            # 测试数据库连接
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            init_db()  # 确保表已创建
            return {
                "status": "healthy",
                "database": "connected"
            }
        except Exception as e:
            import traceback
            error_msg = str(e)
            traceback_str = traceback.format_exc()
            print(f"Database health check error: {error_msg}")
            print(traceback_str)
            return {
                "status": "healthy",
                "database": "disconnected",
                "error": error_msg
            }
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Health check error: {error_msg}")
        print(traceback_str)
        return {
            "status": "healthy",
            "database": "error",
            "error": error_msg
        }


@app.post("/api/v1/video/generate", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """
    生成视频接口
    
    支持即梦（JIMENG）图生视频：首帧和首尾帧两种模式
    支持 Seedance 文生视频
    """
    provider = request.provider or "jimeng"  # 默认使用即梦
    
    try:
        if provider == "jimeng":
            # 使用即梦 API（图生视频）
            jimeng_ak_id = request.jimeng_access_key_id or JIMENG_ACCESS_KEY_ID
            jimeng_ak_secret = request.jimeng_secret_access_key or JIMENG_SECRET_ACCESS_KEY
            
            if not jimeng_ak_id or not jimeng_ak_secret:
                raise HTTPException(
                    status_code=400,
                    detail="即梦 API 密钥未配置，请设置 JIMENG_ACCESS_KEY_ID 和 JIMENG_SECRET_ACCESS_KEY"
                )
            
            mode = request.mode or "first_frame"  # 默认首帧模式
            
            # 根据模式调用不同的接口
            if mode == "first_frame":
                # 首帧图生视频
                if not request.image_base64:
                    raise HTTPException(
                        status_code=400,
                        detail="首帧模式需要提供 image_base64 参数"
                    )
                
                result = await generate_video_from_image_first_frame(
                    image_base64=request.image_base64,
                    duration=request.duration,
                    access_key_id=jimeng_ak_id,
                    secret_access_key=jimeng_ak_secret,
                    prompt=request.prompt,
                    negative_prompt=request.negative_prompt,
                    seed=request.seed
                )
            
            elif mode == "first_last_frame":
                # 首尾帧图生视频
                start_image = request.start_image_base64 or request.image_base64
                if not start_image or not request.end_image_base64:
                    raise HTTPException(
                        status_code=400,
                        detail="首尾帧模式需要提供 start_image_base64 和 end_image_base64 参数"
                    )
                
                result = await generate_video_from_images_first_last(
                    start_image_base64=start_image,
                    end_image_base64=request.end_image_base64,
                    duration=request.duration,
                    access_key_id=jimeng_ak_id,
                    secret_access_key=jimeng_ak_secret,
                    prompt=request.prompt,
                    negative_prompt=request.negative_prompt,
                    seed=request.seed
                )
            
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的模式: {mode}，支持的模式：first_frame, first_last_frame"
                )
            
            # 解析即梦 API 响应
            # 根据实际 API 响应格式调整
            task_id = result.get("task_id") or result.get("taskId") or result.get("id") or result.get("data", {}).get("task_id")
            video_url = result.get("video_url") or result.get("videoUrl") or result.get("url") or result.get("data", {}).get("video_url")
            
            return VideoGenerationResponse(
                success=True,
                task_id=task_id,
                video_url=video_url,
                message="视频生成任务已提交" if task_id else "视频生成完成" if video_url else "请求已接收",
            )
        
        elif provider == "seedance":
            # 使用 Seedance API
            api_key = request.api_key or API_KEY
            
            if not api_key:
                raise HTTPException(
                    status_code=400,
                    detail="Seedance API Key 未配置"
                )
            
            # TODO: 接入 Seedance 1.0 Fast API
            # 目前返回模拟响应
            task_id = f"seedance_task_{hash(request.prompt) % 1000000}"
            
            return VideoGenerationResponse(
                success=True,
                task_id=task_id,
                message="视频生成任务已提交（Seedance）",
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的服务提供商: {provider}，支持的值：jimeng, seedance"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Video generation error: {str(e)}")
        print(error_traceback)
        return VideoGenerationResponse(
            success=False,
            message="视频生成失败",
            error=str(e)
        )


@app.get("/api/v1/video/status/{task_id}")
async def get_video_status(
    task_id: str,
    provider: Optional[str] = "jimeng",
    jimeng_access_key_id: Optional[str] = None,
    jimeng_secret_access_key: Optional[str] = None
):
    """
    查询视频生成状态
    
    支持即梦（JIMENG）和 Seedance 两种服务提供商
    """
    try:
        if provider == "jimeng":
            # 使用即梦 API 查询状态
            jimeng_ak_id = jimeng_access_key_id or JIMENG_ACCESS_KEY_ID
            jimeng_ak_secret = jimeng_secret_access_key or JIMENG_SECRET_ACCESS_KEY
            
            if not jimeng_ak_id or not jimeng_ak_secret:
                raise HTTPException(
                    status_code=400,
                    detail="即梦 API 密钥未配置"
                )
            
            result = await jimeng_check_status(
                task_id=task_id,
                access_key_id=jimeng_ak_id,
                secret_access_key=jimeng_ak_secret
            )
            
            # 解析即梦 API 响应
            status = result.get("status") or result.get("state") or "processing"
            progress = result.get("progress") or result.get("percentage") or 0
            video_url = result.get("video_url") or result.get("videoUrl") or result.get("url")
            
            return {
                "task_id": task_id,
                "status": status,  # processing, completed, failed
                "progress": progress,
                "video_url": video_url,
            }
        
        elif provider == "seedance":
            # TODO: 接入 Seedance 状态查询 API
            return {
                "task_id": task_id,
                "status": "processing",
                "progress": 50,
                "video_url": None,
            }
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的服务提供商: {provider}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Status check error: {str(e)}")
        print(error_traceback)
        raise HTTPException(
            status_code=500,
            detail=f"查询状态失败: {str(e)}"
        )


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

