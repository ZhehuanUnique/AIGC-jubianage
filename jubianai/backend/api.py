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
from backend.volcengine_sdk_helper import create_visual_service, submit_video_task
from backend.api_history import router as history_router
import json

app = FastAPI(title="视频生成 API", version="1.0.0")

# 注册历史记录 API 路由
app.include_router(history_router)

# 配置 CORS
# 允许的源列表
allowed_origins = [
    "http://localhost:3001",
    "http://localhost:3000",
    "https://www.jubianai.cn",
    "https://jubianai.cn",
    "https://aigc-jubianage.vercel.app",
    "https://*.vercel.app",  # Vercel 预览域名
]

# 从环境变量读取额外的允许源
import os
extra_origins = os.getenv("CORS_ORIGINS", "").split(",")
if extra_origins and extra_origins[0]:
    allowed_origins.extend([origin.strip() for origin in extra_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
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
async def generate_video(
    request: VideoGenerationRequest,
    x_api_key: Optional[str] = None
):
    """
    生成视频接口
    
    支持 RAG 增强提示词：根据提示词检索相似视频帧，增强生成效果
    """
    # 验证提示词
    if not request.prompt:
        return VideoGenerationResponse(
            success=False,
            message="提示词不能为空",
            error="提示词不能为空"
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
        # 优先使用环境变量中的配置，如果没有则使用请求中的 api_key（兼容旧方式）
        volc_access_key = VOLCENGINE_ACCESS_KEY_ID or request.api_key or API_KEY
        volc_secret_key = VOLCENGINE_SECRET_ACCESS_KEY
        
        if not volc_access_key:
            return VideoGenerationResponse(
                success=False,
                message="即梦 API 认证信息未配置",
                error="请设置环境变量 VOLCENGINE_ACCESS_KEY_ID，或在请求中传入 api_key"
            )
        
        if not volc_secret_key:
            return VideoGenerationResponse(
                success=False,
                message="即梦 API 认证信息未配置",
                error="请设置环境变量 VOLCENGINE_SECRET_ACCESS_KEY"
            )
        
        # 根据即梦 API 文档构建请求体
        # 参考：https://www.volcengine.com/docs/85621/1791184?lang=zh
        
        # 确定 req_key：根据是否有首尾帧选择不同的 req_key
        if request.first_frame and request.last_frame:
            req_key = "jimeng_i2v_first_tail_v30"  # 首尾帧
        elif request.first_frame:
            req_key = "jimeng_i2v_first_v30"  # 仅首帧
        else:
            req_key = "jimeng_i2v_first_v30"  # 默认使用首帧（如果没有首尾帧，可能需要文生视频）
        
        # 构建图片 URL 数组（即梦 API 使用 image_urls，不是 base64）
        image_urls = []
        
        # 处理首帧和尾帧
        # 注意：即梦 API 需要图片 URL，如果传入的是 base64，需要先上传到对象存储或转换为 URL
        # 这里暂时使用 base64 数据，实际使用时可能需要先上传图片获取 URL
        if request.first_frame:
            # TODO: 如果 first_frame 是 base64，需要先上传获取 URL
            # 暂时假设是 URL 或需要处理
            if request.first_frame.startswith("http"):
                image_urls.append(request.first_frame)
            else:
                # base64 数据，需要转换为 URL 或使用 binary_data_base64
                # 根据文档，可以使用 binary_data_base64 数组
                pass
        
        if request.last_frame:
            if request.last_frame.startswith("http"):
                image_urls.append(request.last_frame)
            else:
                # base64 数据
                pass
        
        # 根据即梦 API 文档构建请求体
        # 文档：https://www.volcengine.com/docs/85621/1785204?lang=zh
        api_payload = {
            "req_key": req_key,
            "prompt": enhanced_prompt,  # 使用增强后的提示词（必选）
        }
        
        # 处理图片输入（二选一：binary_data_base64 或 image_urls）
        binary_data_base64 = []
        image_urls = []
        
        if request.first_frame:
            if request.first_frame.startswith("http"):
                image_urls.append(request.first_frame)
            else:
                # base64 数据，移除 data:image/...;base64, 前缀
                base64_data = request.first_frame
                if "," in base64_data:
                    base64_data = base64_data.split(",")[1]
                binary_data_base64.append(base64_data)
        
        if request.last_frame:
            if request.last_frame.startswith("http"):
                image_urls.append(request.last_frame)
            else:
                base64_data = request.last_frame
                if "," in base64_data:
                    base64_data = base64_data.split(",")[1]
                binary_data_base64.append(base64_data)
        
        # 根据文档，binary_data_base64 和 image_urls 二选一
        if binary_data_base64:
            api_payload["binary_data_base64"] = binary_data_base64
        elif image_urls:
            api_payload["image_urls"] = image_urls
        
        # 计算 frames（总帧数）
        # 根据文档：frames = 24 * n + 1，支持 5秒(121帧) 和 10秒(241帧)
        calculated_frames = request.duration * request.fps
        if calculated_frames <= 121:
            frames = 121  # 5秒
        elif calculated_frames <= 241:
            frames = 241  # 10秒
        else:
            frames = 241  # 默认 10秒
        
        api_payload["frames"] = frames
        
        # 添加可选参数
        if request.seed is not None:
            api_payload["seed"] = request.seed
        else:
            api_payload["seed"] = -1  # 默认值（随机种子）
        
        # 注意：即梦 API 不支持 negative_prompt、width、height 等参数
        # 这些参数可能需要通过其他方式传递或忽略
        
        # 使用官方 SDK 调用即梦 API
        # 官方 SDK 会自动处理签名、Action、Version 等参数
        # 参考：https://github.com/volcengine/volc-sdk-python
        try:
            # 创建 VisualService 实例
            visual_service = create_visual_service(volc_access_key, volc_secret_key)
            
            # 准备图片数据
            image_urls_list = image_urls if image_urls else None
            binary_data_list = binary_data_base64 if binary_data_base64 else None
            
            # 调用官方 SDK 提交任务
            api_result = submit_video_task(
                service=visual_service,
                req_key=req_key,
                prompt=enhanced_prompt,
                frames=frames,
                seed=api_payload.get("seed", -1),
                image_urls=image_urls_list,
                binary_data_base64=binary_data_list
            )
            
            # 解析响应
            # 官方 SDK 返回的格式可能是：
            # 1. 直接返回 {"code": 10000, "data": {"task_id": "..."}, ...}
            # 2. 或者返回 {"ResponseMetadata": {...}, "Result": {...}}
            response_code = api_result.get("code")
            if response_code is None:
                # 可能是火山引擎格式，检查 ResponseMetadata
                if "ResponseMetadata" in api_result:
                    metadata = api_result["ResponseMetadata"]
                    if "Error" in metadata:
                        error_info = metadata["Error"]
                        error_code = error_info.get("Code", "Unknown")
                        error_message = error_info.get("Message", "未知错误")
                        request_id = metadata.get("RequestId", "")
                        raise Exception(f"即梦 API 调用失败: 错误码={error_code}, 错误信息={error_message}, RequestId={request_id}")
                    # 如果没有错误，检查 Result
                    if "Result" in api_result:
                        result = api_result["Result"]
                        task_id = result.get("task_id") or result.get("TaskId")
                        if task_id:
                            api_result = {"code": 10000, "data": {"task_id": task_id}, "message": "Success"}
                        else:
                            raise Exception("即梦 API 响应格式异常，未找到 task_id")
            
            if response_code != 10000:
                error_msg = api_result.get("message", "未知错误")
                request_id = api_result.get("request_id", "")
                
                # 特殊处理并发限制错误
                if response_code == 50430 or "concurrent" in error_msg.lower() or "Concurrent Limit" in error_msg:
                    raise Exception(f"即梦 API 并发限制: {error_msg}。请稍后重试，或等待其他任务完成。")
                
                raise Exception(f"即梦 API 调用失败: code={response_code}, message={error_msg}, request_id={request_id}")
        
            # 从即梦 API 响应中提取任务 ID
            task_id = api_result.get("data", {}).get("task_id")
            if not task_id:
                raise Exception("即梦 API 响应中未找到 task_id，请检查响应格式")
            
            # 保存到数据库（可选，如果数据库未配置则跳过）
            try:
                from backend.database import get_db, SessionLocal
                from backend.video_history import VideoHistoryService
                from backend.auth import AuthService
                
                # 检查数据库是否可用
                if SessionLocal:
                    # 获取数据库会话
                    db = next(get_db())
                    
                    # 获取用户ID
                    user_id = None
                    if x_api_key:
                        user = AuthService.get_user_by_api_key(db, x_api_key)
                        if user:
                            user_id = user.id
                    
                    if not user_id:
                        # 使用默认用户
                        default_user = AuthService.get_or_create_default_user(db)
                        user_id = default_user.id
                    
                    # 创建生成记录
                    VideoHistoryService.create_generation_record(
                        db=db,
                        task_id=task_id,
                        user_id=user_id,
                        prompt=request.prompt,
                        duration=request.duration,
                        fps=request.fps or DEFAULT_VIDEO_SETTINGS["fps"],
                        width=request.width or DEFAULT_VIDEO_SETTINGS["width"],
                        height=request.height or DEFAULT_VIDEO_SETTINGS["height"],
                        seed=request.seed,
                        negative_prompt=request.negative_prompt,
                        first_frame_url=request.first_frame,
                        last_frame_url=request.last_frame,
                        status="pending"
                    )
                    print(f"视频生成记录已保存: task_id={task_id}, user_id={user_id}")
                else:
                    print("数据库未配置，跳过保存历史记录")
            except Exception as db_error:
                # 数据库保存失败不影响视频生成，只记录错误
                print(f"保存视频生成记录失败: {str(db_error)}")
            
            # 构建响应数据（在 try 块内）
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
            # 处理即梦 API 调用错误
            error_msg = str(e)
            print(f"即梦 API 调用错误: {error_msg}")
            return VideoGenerationResponse(
                success=False,
                message=f"视频生成失败: {error_msg}",
                error=error_msg
            )
        
    except HTTPException as e:
        return VideoGenerationResponse(
            success=False,
            message="请求错误",
            error=e.detail
        )
    except Exception as e:
        import traceback
        error_detail = str(e)
        error_traceback = traceback.format_exc()
        print(f"视频生成错误: {error_detail}\n{error_traceback}")
        return VideoGenerationResponse(
            success=False,
            message="视频生成失败",
            error=f"{error_detail}。请检查后端日志获取详细信息。"
        )


@app.get("/api/v1/video/status/{task_id}")
async def get_video_status(task_id: str):
    """
    查询视频生成状态
    
    调用即梦 API 查询任务状态
    参考：https://www.volcengine.com/docs/85621/1785204?lang=zh
    """
    try:
        # 使用火山引擎 AK/SK 认证
        volc_access_key = VOLCENGINE_ACCESS_KEY_ID or API_KEY
        volc_secret_key = VOLCENGINE_SECRET_ACCESS_KEY
        
        if not volc_access_key or not volc_secret_key:
            return {
                "task_id": task_id,
                "status": "error",
                "progress": 0,
                "video_url": None,
                "error": "即梦 API 认证信息未配置"
            }
        
        # 创建 VisualService 实例
        from backend.volcengine_sdk_helper import create_visual_service, query_video_task
        
        visual_service = create_visual_service(volc_access_key, volc_secret_key)
        
        # 尝试不同的 req_key（可能是首帧或首尾帧）
        req_keys = ["jimeng_i2v_first_v30", "jimeng_i2v_first_tail_v30"]
        
        for req_key in req_keys:
            try:
                # 查询任务状态
                api_result = query_video_task(
                    service=visual_service,
                    req_key=req_key,
                    task_id=task_id
                )
                
                # 解析响应
                # 根据即梦 API 文档，响应格式为：
                # {
                #   "code": 10000,
                #   "data": {
                #     "status": "done",  # in_queue, generating, done, not_found, expired
                #     "video_url": "https://..."
                #   },
                #   "message": "Success"
                # }
                response_code = api_result.get("code")
                
                if response_code == 10000:
                    data = api_result.get("data", {})
                    status = data.get("status", "processing")
                    video_url = data.get("video_url")
                    
                    # 转换状态
                    if status == "done":
                        # 视频生成完成，上传到对象存储并更新数据库
                        final_video_url = video_url
                        
                        try:
                            from backend.database import get_db
                            from backend.video_history import VideoHistoryService
                            from backend.storage import get_storage_service
                            import uuid
                            from datetime import datetime
                            
                            # 获取数据库会话
                            db = next(get_db())
                            
                            # 获取生成记录
                            generation = VideoHistoryService.get_generation_by_task_id(db, task_id)
                            
                            if generation and video_url:
                                # 尝试上传到对象存储
                                storage_service = get_storage_service()
                                if storage_service:
                                    try:
                                        # 生成视频文件名
                                        video_name = f"{task_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.mp4"
                                        
                                        # 上传到对象存储
                                        storage_url = await storage_service.upload_video(video_url, video_name)
                                        
                                        if storage_url:
                                            final_video_url = storage_url
                                            print(f"视频已上传到对象存储: {storage_url}")
                                        else:
                                            print(f"对象存储上传失败，使用原始URL: {video_url}")
                                    except Exception as storage_error:
                                        print(f"对象存储上传错误: {str(storage_error)}")
                                        # 上传失败不影响，使用原始URL
                                
                                # 更新数据库状态
                                VideoHistoryService.update_generation_status(
                                    db=db,
                                    task_id=task_id,
                                    status="completed",
                                    video_url=final_video_url,
                                    video_name=generation.video_name or f"{task_id}.mp4"
                                )
                                print(f"视频生成记录已更新: task_id={task_id}, video_url={final_video_url}")
                        except Exception as db_error:
                            # 数据库更新失败不影响状态返回，只记录错误
                            print(f"更新视频生成记录失败: {str(db_error)}")
                        
                        return {
                            "task_id": task_id,
                            "status": "completed",
                            "progress": 100,
                            "video_url": final_video_url
                        }
                    elif status == "in_queue":
                        # 更新数据库状态为 processing
                        try:
                            from backend.database import get_db
                            from backend.video_history import VideoHistoryService
                            db = next(get_db())
                            VideoHistoryService.update_generation_status(
                                db=db,
                                task_id=task_id,
                                status="processing"
                            )
                        except Exception:
                            pass
                        
                        return {
                            "task_id": task_id,
                            "status": "processing",
                            "progress": 10,
                            "video_url": None
                        }
                    elif status == "generating":
                        # 更新数据库状态为 processing
                        try:
                            from backend.database import get_db
                            from backend.video_history import VideoHistoryService
                            db = next(get_db())
                            VideoHistoryService.update_generation_status(
                                db=db,
                                task_id=task_id,
                                status="processing"
                            )
                        except Exception:
                            pass
                        
                        return {
                            "task_id": task_id,
                            "status": "processing",
                            "progress": 50,
                            "video_url": None
                        }
                    elif status in ["not_found", "expired"]:
                        # 更新数据库状态为 failed
                        try:
                            from backend.database import get_db
                            from backend.video_history import VideoHistoryService
                            db = next(get_db())
                            VideoHistoryService.update_generation_status(
                                db=db,
                                task_id=task_id,
                                status="failed",
                                error_message=f"任务状态: {status}"
                            )
                        except Exception:
                            pass
                        
                        return {
                            "task_id": task_id,
                            "status": "failed",
                            "progress": 0,
                            "video_url": None,
                            "error": f"任务状态: {status}"
                        }
                    else:
                        return {
                            "task_id": task_id,
                            "status": "processing",
                            "progress": 30,
                            "video_url": None,
                            "status_detail": status
                        }
                else:
                    # 如果 code != 10000，记录错误但继续尝试下一个 req_key
                    error_msg = api_result.get("message", "未知错误")
                    print(f"查询任务失败 (req_key={req_key}): code={response_code}, message={error_msg}")
                    # 检查是否是并发限制错误
                    if response_code == 50430 or "Concurrent Limit" in error_msg or "concurrent" in error_msg.lower():
                        return {
                            "task_id": task_id,
                            "status": "failed",
                            "progress": 0,
                            "video_url": None,
                            "error": "API 并发限制，请稍后重试。即梦 API 有并发请求限制，请等待其他任务完成后再试。"
                        }
                    continue
                    
            except Exception as e:
                # 如果查询失败，记录错误但继续尝试下一个 req_key
                error_msg = str(e)
                print(f"查询任务异常 (req_key={req_key}): {error_msg}")
                # 检查是否是并发限制错误
                if "Concurrent Limit" in error_msg or "50430" in error_msg:
                    return {
                        "task_id": task_id,
                        "status": "processing",
                        "progress": 30,
                        "video_url": None,
                        "warning": "API 并发限制，请稍后重试"
                    }
                continue
        
        # 所有 req_key 都失败，返回处理中状态（可能是任务不存在或查询失败）
        return {
            "task_id": task_id,
            "status": "processing",
            "progress": 30,
        "video_url": None,
            "note": "无法查询到任务状态，可能任务不存在或仍在处理中"
        }
        
    except Exception as e:
        return {
            "task_id": task_id,
            "status": "error",
            "progress": 0,
            "video_url": None,
            "error": str(e)
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

