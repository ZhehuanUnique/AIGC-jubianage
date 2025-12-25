"""
视频生成历史记录服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
from .database import VideoGeneration, User


class VideoHistoryService:
    """视频生成历史记录服务"""
    
    @staticmethod
    def create_generation_record(
        db: Session,
        task_id: str,
        user_id: int,
        prompt: str,
        duration: int,
        fps: int = 24,
        width: int = 720,
        height: int = 720,
        seed: Optional[int] = None,
        negative_prompt: Optional[str] = None,
        first_frame_url: Optional[str] = None,
        last_frame_url: Optional[str] = None,
        status: str = "pending"
    ) -> VideoGeneration:
        """创建视频生成记录"""
        try:
            print(f"🔍 创建 VideoGeneration 对象: task_id={task_id}, user_id={user_id}")
            generation = VideoGeneration(
                task_id=task_id,
                user_id=user_id,
                prompt=prompt,
                duration=duration,
                fps=fps,
                width=width,
                height=height,
                seed=seed,
                negative_prompt=negative_prompt,
                first_frame_url=first_frame_url,
                last_frame_url=last_frame_url,
                status=status
            )
            print(f"🔍 添加到数据库会话...")
            db.add(generation)
            print(f"🔍 提交事务...")
            db.commit()
            print(f"🔍 刷新对象...")
            db.refresh(generation)
            print(f"✅ 记录创建成功: id={generation.id}")
            return generation
        except Exception as e:
            print(f"❌ 创建记录时出错: {str(e)}")
            import traceback
            traceback.print_exc()
            db.rollback()
            raise
    
    @staticmethod
    def update_generation_status(
        db: Session,
        task_id: str,
        status: str,
        video_url: Optional[str] = None,
        video_name: Optional[str] = None,
        video_size: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> Optional[VideoGeneration]:
        """更新视频生成状态"""
        generation = db.query(VideoGeneration).filter(
            VideoGeneration.task_id == task_id
        ).first()
        
        if not generation:
            return None
        
        generation.status = status
        if video_url:
            generation.video_url = video_url
        if video_name:
            generation.video_name = video_name
        if video_size:
            generation.video_size = video_size
        if error_message:
            generation.error_message = error_message
        if status in ["completed", "failed"]:
            generation.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(generation)
        return generation
    
    @staticmethod
    def get_generation_by_task_id(
        db: Session,
        task_id: str
    ) -> Optional[VideoGeneration]:
        """根据任务ID获取生成记录"""
        return db.query(VideoGeneration).filter(
            VideoGeneration.task_id == task_id
        ).first()
    
    @staticmethod
    def get_user_generations(
        db: Session,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[VideoGeneration]:
        """获取用户的视频生成历史"""
        query = db.query(VideoGeneration).filter(
            VideoGeneration.user_id == user_id
        )
        
        if status:
            query = query.filter(VideoGeneration.status == status)
        
        return query.order_by(desc(VideoGeneration.created_at)).limit(limit).offset(offset).all()
    
    @staticmethod
    def get_user_generation_count(
        db: Session,
        user_id: int,
        status: Optional[str] = None
    ) -> int:
        """获取用户的视频生成总数"""
        query = db.query(VideoGeneration).filter(
            VideoGeneration.user_id == user_id
        )
        
        if status:
            query = query.filter(VideoGeneration.status == status)
        
        return query.count()
    
    @staticmethod
    def delete_generation(
        db: Session,
        generation_id: int,
        user_id: int
    ) -> bool:
        """删除视频生成记录（只能删除自己的）"""
        generation = db.query(VideoGeneration).filter(
            VideoGeneration.id == generation_id,
            VideoGeneration.user_id == user_id
        ).first()
        
        if not generation:
            return False
        
        db.delete(generation)
        db.commit()
        return True
    
    @staticmethod
    def cleanup_timeout_tasks(
        db: Session,
        timeout_minutes: int = 5
    ) -> int:
        """清理超时的任务（pending 或 processing 状态超过指定时间）"""
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        
        # 查找所有超时的 pending 或 processing 任务
        timeout_tasks = db.query(VideoGeneration).filter(
            VideoGeneration.status.in_(["pending", "processing"]),
            VideoGeneration.created_at < cutoff_time
        ).all()
        
        count = len(timeout_tasks)
        
        if count > 0:
            print(f"🧹 清理 {count} 个超时任务（超过 {timeout_minutes} 分钟）")
            for task in timeout_tasks:
                elapsed_minutes = (datetime.utcnow() - task.created_at.replace(tzinfo=None) if task.created_at.tzinfo else datetime.utcnow() - task.created_at).total_seconds() / 60
                task.status = "failed"
                task.error_message = f"任务超时：已等待 {elapsed_minutes:.1f} 分钟（正常应在1-3分钟内完成）"
                task.completed_at = datetime.utcnow()
                print(f"  - 任务 {task.task_id} 已标记为失败（等待 {elapsed_minutes:.1f} 分钟）")
            
            db.commit()
        
        return count

