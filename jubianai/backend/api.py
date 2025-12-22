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
from config import (
    API_KEY, SEEDANCE_API_ENDPOINT, DEFAULT_VIDEO_SETTINGS,
    VOLCENGINE_ACCESS_KEY_ID, VOLCENGINE_SECRET_ACCESS_KEY, JIMENG_API_ENDPOINT
)
from backend.assets_api import (
    upload_asset, get_assets_by_character, delete_asset, 
    get_asset_path, AssetMetadata
)
from backend.volcengine_auth import generate_signature, generate_simple_signature
import json

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
    first_frame: Optional[str] = None  # 首帧图片（base64 或 URL）
    last_frame: Optional[str] = None  # 尾帧图片（base64 或 URL）


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
        
        # 调用即梦 API 生成视频（视频生成3.0 720P - 图生视频-首尾帧）
        # 参考：https://www.volcengine.com/docs/85621/1791184?lang=zh
        
        # 使用火山引擎 AK/SK 认证
        volc_access_key = VOLCENGINE_ACCESS_KEY_ID or api_key
        volc_secret_key = VOLCENGINE_SECRET_ACCESS_KEY
        
        if not volc_access_key or not volc_secret_key:
            raise HTTPException(
                status_code=400,
                detail="即梦 API 认证信息未配置，请设置 VOLCENGINE_ACCESS_KEY_ID 和 VOLCENGINE_SECRET_ACCESS_KEY"
            )
        
        # 根据即梦 API 文档构建请求体
        api_payload = {
            "req_key": "video_generation_720p",  # 即梦 API 的 req_key
            "prompt": enhanced_prompt,  # 使用增强后的提示词
            "width": request.width,
            "height": request.height,
            "duration": request.duration,
            "fps": request.fps,
        }
        
        # 添加可选参数
        if request.seed is not None:
            api_payload["seed"] = request.seed
        if request.negative_prompt:
            api_payload["negative_prompt"] = request.negative_prompt
        
        # 首尾帧处理（根据即梦 API 文档格式）
        if request.first_frame:
            # 即梦 API 首帧参数格式：base64 编码的图片
            api_payload["first_frame"] = request.first_frame
        if request.last_frame:
            # 即梦 API 尾帧参数格式：base64 编码的图片
            api_payload["last_frame"] = request.last_frame
        
        # 构建请求 URI 和请求体
        # 根据即梦 API 文档，完整的 API 端点
        api_uri = "/video_generation/v1/video_generation_720p"  # API 路径
        
        # 确定基础端点
        if SEEDANCE_API_ENDPOINT and SEEDANCE_API_ENDPOINT.startswith("http"):
            # 如果 SEEDANCE_API_ENDPOINT 是完整 URL，直接使用
            full_url = SEEDANCE_API_ENDPOINT
            # 从完整 URL 中提取基础端点用于签名
            from urllib.parse import urlparse
            parsed = urlparse(SEEDANCE_API_ENDPOINT)
            base_endpoint = f"{parsed.scheme}://{parsed.netloc}"
            api_uri = parsed.path
        elif JIMENG_API_ENDPOINT:
            # 使用 JIMENG_API_ENDPOINT 作为基础端点
            base_endpoint = JIMENG_API_ENDPOINT.rstrip("/")
            full_url = f"{base_endpoint}{api_uri}"
        else:
            # 默认端点
            base_endpoint = "https://visual.volcengineapi.com"
            full_url = f"{base_endpoint}{api_uri}"
        
        body_str = json.dumps(api_payload, ensure_ascii=False)
        
        # 生成签名
        try:
            # 尝试使用标准签名方式
            auth_headers = generate_signature(
                access_key_id=volc_access_key,
                secret_access_key=volc_secret_key,
                method="POST",
                uri=api_uri,
                headers={"Content-Type": "application/json"},
                body=body_str
            )
        except Exception as e:
            # 如果标准签名失败，尝试简化签名
            print(f"标准签名失败，尝试简化签名: {e}")
            auth_headers = generate_simple_signature(
                access_key_id=volc_access_key,
                secret_access_key=volc_secret_key,
                method="POST",
                uri=api_uri,
                body=body_str
            )
        
        # 调用即梦 API（火山引擎格式）
        async with httpx.AsyncClient() as client:
            headers = {
                **auth_headers,
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                full_url,
                headers=headers,
                json=api_payload,
                timeout=300.0
            )
            response.raise_for_status()
            api_result = response.json()
            
            # 从即梦 API 响应中提取任务 ID
            # 即梦 API 返回格式可能包含 task_id、taskId 或 data.task_id
            task_id = (
                api_result.get("task_id") or 
                api_result.get("taskId") or 
                api_result.get("data", {}).get("task_id") or
                api_result.get("data", {}).get("taskId") or
                f"task_{hash(enhanced_prompt) % 1000000}"
            )
        
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

