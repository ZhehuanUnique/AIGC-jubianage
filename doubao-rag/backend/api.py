"""
RAG API：提供视频处理和检索接口
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import shutil
from pathlib import Path
import sys
from pathlib import Path

# 添加当前目录到路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from langgraph_service import LangGraphRAGService

app = FastAPI(title="视频 RAG API (LangGraph)", version="2.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 LangGraph RAG 服务
rag_service = LangGraphRAGService()

# 上传目录
UPLOAD_DIR = Path("doubao-rag/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class VideoProcessRequest(BaseModel):
    """视频处理请求"""
    video_id: Optional[str] = None
    method: str = "interval"  # "interval" 或 "scene"
    interval_seconds: float = 1.0
    metadata: Optional[Dict] = None


class SearchRequest(BaseModel):
    """搜索请求"""
    query: str
    n_results: int = 5
    video_id: Optional[str] = None


class EnhancePromptRequest(BaseModel):
    """增强提示词请求"""
    prompt: str
    n_references: int = 3
    video_id: Optional[str] = None


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "message": "RAG 服务运行正常"}


@app.post("/api/v1/rag/video/upload")
async def upload_video(
    file: UploadFile = File(...),
    video_id: Optional[str] = None,
    method: str = "interval",
    interval_seconds: float = 1.0
):
    """
    上传并处理视频
    
    1. 保存视频文件
    2. 提取关键帧
    3. 向量化
    4. 存储到向量数据库
    """
    try:
        # 保存上传的视频
        if video_id is None:
            video_id = Path(file.filename).stem
        
        video_path = UPLOAD_DIR / f"{video_id}_{file.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 处理视频
        result = rag_service.process_video(
            video_path=str(video_path),
            video_id=video_id,
            method=method,
            interval_seconds=interval_seconds
        )
        
        return {
            "success": True,
            "video_id": result["video_id"],
            "frames_count": result["frames_count"],
            "message": "视频处理完成"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rag/search")
async def search_frames(request: SearchRequest):
    """
    搜索相似帧
    
    通过文本查询检索相似的关键帧
    """
    try:
        results = rag_service.search_similar_frames(
            query=request.query,
            n_results=request.n_results,
            video_id=request.video_id
        )
        
        return {
            "success": True,
            "query": request.query,
            "results": results,
            "count": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rag/search/image")
async def search_by_image(
    file: UploadFile = File(...),
    n_results: int = 5,
    video_id: Optional[str] = None
):
    """
    通过图片搜索相似帧
    """
    try:
        # 保存临时图片
        temp_path = UPLOAD_DIR / f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 搜索
        results = rag_service.search_by_image(
            image_path=str(temp_path),
            n_results=n_results,
            video_id=video_id
        )
        
        # 删除临时文件
        temp_path.unlink()
        
        return {
            "success": True,
            "results": results,
            "count": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rag/enhance-prompt")
async def enhance_prompt(request: EnhancePromptRequest):
    """
    增强提示词
    
    通过 RAG 检索相关帧，增强原始提示词
    """
    try:
        result = rag_service.enhance_prompt(
            original_prompt=request.prompt,
            n_references=request.n_references,
            video_id=request.video_id
        )
        
        return {
            "success": True,
            **result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/rag/video/{video_id}")
async def delete_video(video_id: str):
    """删除视频及其所有帧"""
    try:
        success = rag_service.delete_video(video_id)
        return {
            "success": success,
            "video_id": video_id,
            "message": "删除成功" if success else "删除失败"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/rag/stats")
async def get_stats():
    """获取统计信息"""
    try:
        stats = rag_service.get_stats()
        return {
            "success": True,
            **stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

