"""
视频生成历史记录 API
新增的 API 端点，用于查询和管理视频生成历史
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .database import get_db, VideoGeneration
from .video_history import VideoHistoryService
from .auth import AuthService

router = APIRouter(prefix="/api/v1/video", tags=["video-history"])


class VideoGenerationHistoryItem(BaseModel):
    """视频生成历史记录项"""
    id: int
    task_id: str
    prompt: str
    duration: int
    fps: int
    width: int
    height: int
    status: str
    video_url: Optional[str] = None
    video_name: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    is_ultra_hd: Optional[bool] = False
    is_favorite: Optional[bool] = False
    is_liked: Optional[bool] = False
    
    class Config:
        from_attributes = True


class VideoGenerationHistoryResponse(BaseModel):
    """视频生成历史响应"""
    total: int
    items: List[VideoGenerationHistoryItem]
    limit: int
    offset: int


def get_current_user_id(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> int:
    """获取当前用户ID（通过 API Key 或默认用户）"""
    try:
        if x_api_key:
            user = AuthService.get_user_by_api_key(db, x_api_key)
            if user:
                return user.id
        
        # 如果没有提供 API Key 或无效，使用默认用户
        default_user = AuthService.get_or_create_default_user(db)
        return default_user.id
    except HTTPException:
        raise
    except Exception as e:
        # 如果数据库不可用，抛出 HTTPException
        raise HTTPException(
            status_code=503,
            detail=f"数据库不可用: {str(e)}。请配置 SUPABASE_DB_URL 环境变量。"
        )


@router.get("/history", response_model=VideoGenerationHistoryResponse)
async def get_video_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None, regex="^(pending|processing|completed|failed)$"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    获取视频生成历史记录
    
    - **limit**: 每页数量（1-100）
    - **offset**: 偏移量
    - **status**: 筛选状态（pending/processing/completed/failed）
    - **x_api_key**: API Key（可选，用于多用户模式）
    """
    try:
        # 如果数据库未初始化，返回空列表
        try:
            user_id = get_current_user_id(x_api_key, db)
        except Exception as db_init_error:
            # 数据库未初始化或表不存在，返回空列表
            print(f"数据库初始化错误: {str(db_init_error)}")
            return VideoGenerationHistoryResponse(
                total=0,
                items=[],
                limit=limit,
                offset=offset
            )
        
        # 获取历史记录
        try:
            generations = VideoHistoryService.get_user_generations(
                db, user_id, limit=limit, offset=offset, status=status
            )
            
            # 获取总数
            total = VideoHistoryService.get_user_generation_count(db, user_id, status=status)
        except Exception as query_error:
            # 查询失败，可能是表不存在，返回空列表
            print(f"查询历史记录失败: {str(query_error)}")
            return VideoGenerationHistoryResponse(
                total=0,
                items=[],
                limit=limit,
                offset=offset
            )
        
        # 转换为响应模型
        items = [
            VideoGenerationHistoryItem(
                id=gen.id,
                task_id=gen.task_id,
                prompt=gen.prompt,
                duration=gen.duration,
                fps=gen.fps,
                width=gen.width,
                height=gen.height,
                status=gen.status,
                video_url=gen.video_url,
                video_name=gen.video_name,
                created_at=gen.created_at,
                completed_at=gen.completed_at,
                is_ultra_hd=getattr(gen, 'is_ultra_hd', False),
                is_favorite=getattr(gen, 'is_favorite', False),
                is_liked=getattr(gen, 'is_liked', False)
            )
            for gen in generations
        ]
        
        return VideoGenerationHistoryResponse(
            total=total,
            items=items,
            limit=limit,
            offset=offset
        )
    except HTTPException:
        raise
    except Exception as e:
        # 其他错误，返回空列表而不是抛出异常
        print(f"获取历史记录异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return VideoGenerationHistoryResponse(
            total=0,
            items=[],
            limit=limit,
            offset=offset
        )


@router.get("/history/{task_id}")
async def get_video_by_task_id(
    task_id: str,
    x_api_key: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """根据任务ID获取视频生成记录"""
    try:
        user_id = get_current_user_id(x_api_key, db)
        
        generation = VideoHistoryService.get_generation_by_task_id(db, task_id)
        
        if not generation:
            raise HTTPException(status_code=404, detail="视频记录不存在")
        
        # 检查权限（只能查看自己的记录）
        if generation.user_id != user_id:
            raise HTTPException(status_code=403, detail="无权访问此记录")
        
        return VideoGenerationHistoryItem(
            id=generation.id,
            task_id=generation.task_id,
            prompt=generation.prompt,
            duration=generation.duration,
            fps=generation.fps,
            width=generation.width,
            height=generation.height,
            status=generation.status,
            video_url=generation.video_url,
            video_name=generation.video_name,
            created_at=generation.created_at,
            completed_at=generation.completed_at,
            is_ultra_hd=getattr(generation, 'is_ultra_hd', False),
            is_favorite=getattr(generation, 'is_favorite', False),
            is_liked=getattr(generation, 'is_liked', False)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取视频记录失败: {str(e)}")


@router.delete("/history/{generation_id}")
async def delete_video_history(
    generation_id: int,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """删除视频生成记录"""
    try:
        user_id = get_current_user_id(x_api_key, db)
        
        success = VideoHistoryService.delete_generation(db, generation_id, user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="视频记录不存在或无权删除")
        
        return {"success": True, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


@router.patch("/history/{generation_id}/favorite")
async def toggle_favorite(
    generation_id: int,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """切换收藏状态"""
    try:
        user_id = get_current_user_id(x_api_key, db)
        
        generation = db.query(VideoGeneration).filter(
            VideoGeneration.id == generation_id,
            VideoGeneration.user_id == user_id
        ).first()
        
        if not generation:
            raise HTTPException(status_code=404, detail="视频记录不存在")
        
        generation.is_favorite = not generation.is_favorite
        db.commit()
        
        return {"success": True, "is_favorite": generation.is_favorite}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"操作失败: {str(e)}")


@router.patch("/history/{generation_id}/like")
async def toggle_like(
    generation_id: int,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """切换点赞状态"""
    try:
        user_id = get_current_user_id(x_api_key, db)
        
        generation = db.query(VideoGeneration).filter(
            VideoGeneration.id == generation_id,
            VideoGeneration.user_id == user_id
        ).first()
        
        if not generation:
            raise HTTPException(status_code=404, detail="视频记录不存在")
        
        generation.is_liked = not generation.is_liked
        db.commit()
        
        return {"success": True, "is_liked": generation.is_liked}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"操作失败: {str(e)}")


@router.patch("/history/{generation_id}/ultra-hd")
async def toggle_ultra_hd(
    generation_id: int,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """切换超清标记"""
    try:
        user_id = get_current_user_id(x_api_key, db)
        
        generation = db.query(VideoGeneration).filter(
            VideoGeneration.id == generation_id,
            VideoGeneration.user_id == user_id
        ).first()
        
        if not generation:
            raise HTTPException(status_code=404, detail="视频记录不存在")
        
        generation.is_ultra_hd = not generation.is_ultra_hd
        db.commit()
        
        return {"success": True, "is_ultra_hd": generation.is_ultra_hd}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"操作失败: {str(e)}")

