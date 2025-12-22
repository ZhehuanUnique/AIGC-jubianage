"""
后端 API 服务
使用 FastAPI 框架，后续接入 Seedance 1.0 Fast
"""
from fastapi import FastAPI, HTTPException, Header, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_KEY, SEEDANCE_API_ENDPOINT, DEFAULT_VIDEO_SETTINGS
from backend.assets_api import (
    upload_asset, get_assets_by_character, delete_asset, 
    get_asset_path, AssetMetadata
)

app = FastAPI(title="视频生成 API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return {"status": "healthy"}


@app.post("/api/v1/video/generate", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """
    生成视频接口
    
    支持 RAG 增强提示词：根据提示词检索相似视频帧，增强生成效果
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
        # RAG 增强提示词（可选）
        enhanced_prompt = request.prompt
        rag_references = None
        
        try:
            # 尝试导入 RAG 服务
            import sys
            from pathlib import Path
            rag_path = Path(__file__).parent.parent.parent / "doubao-rag" / "backend"
            if str(rag_path) not in sys.path:
                sys.path.insert(0, str(rag_path))
            
            from rag_service import RAGService
            
            # 初始化 RAG 服务
            rag_service = RAGService()
            
            # 增强提示词
            enhanced_result = rag_service.enhance_prompt(
                original_prompt=request.prompt,
                n_references=3  # 参考 3 个相似帧
            )
            
            enhanced_prompt = enhanced_result["enhanced_prompt"]
            rag_references = enhanced_result["references"]
            
        except ImportError:
            # RAG 服务不可用，使用原始提示词
            pass
        except Exception as e:
            # RAG 增强失败，使用原始提示词
            print(f"RAG 增强失败，使用原始提示词: {e}")
            pass
        
        # TODO: 接入 Seedance 1.0 Fast API
        # 使用增强后的提示词生成视频
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
        #             "prompt": enhanced_prompt,  # 使用增强后的提示词
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
        task_id = f"task_{hash(enhanced_prompt) % 1000000}"
        
        response_data = {
            "success": True,
            "task_id": task_id,
            "message": "视频生成任务已提交",
        }
        
        # 如果使用了 RAG，添加参考信息
        if rag_references:
            response_data["rag_enhanced"] = True
            response_data["original_prompt"] = request.prompt
            response_data["enhanced_prompt"] = enhanced_prompt
            response_data["rag_references_count"] = len(rag_references)
        
        return VideoGenerationResponse(**response_data)
        
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
async def upload_asset_endpoint(file: UploadFile = File(...)):
    """
    上传资产文件
    
    文件名格式：人物名-视图类型.扩展名
    例如：小明-正视图.jpg, 小美-侧视图.png
    """
    try:
        asset = await upload_asset(file)
        return asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/assets/list")
async def list_assets():
    """获取所有资产，按人物分组"""
    assets_by_character = get_assets_by_character()
    
    # 转换为 JSON 可序列化格式
    result = {}
    for character, assets in assets_by_character.items():
        result[character] = [asset.dict() for asset in assets]
    
    return result


@app.get("/api/v1/assets/characters")
async def list_characters():
    """获取所有人物列表"""
    assets_by_character = get_assets_by_character()
    return {
        "characters": list(assets_by_character.keys()),
        "count": len(assets_by_character)
    }


@app.get("/api/v1/assets/{filename:path}")
async def get_asset(filename: str):
    """获取资产文件"""
    file_path = get_asset_path(filename)
    
    if not file_path or not file_path.exists():
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
async def delete_asset_endpoint(filename: str):
    """删除资产"""
    success = delete_asset(filename)
    
    if not success:
        raise HTTPException(status_code=404, detail="资产文件不存在")
    
    return {"success": True, "message": "资产已删除"}


if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT
    
    uvicorn.run(app, host=HOST, port=PORT)

