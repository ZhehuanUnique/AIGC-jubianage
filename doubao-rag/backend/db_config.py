"""
数据库配置模块
支持独立配置数据库路径，方便单独使用
"""
import os
from pathlib import Path
from typing import Optional


class RAGDatabaseConfig:
    """RAG 数据库配置类"""
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        frames_dir: Optional[str] = None,
        collection_name: str = "video_frames"
    ):
        """
        初始化数据库配置
        
        Args:
            db_path: 向量数据库路径（如果为 None，使用默认路径或环境变量）
            frames_dir: 关键帧存储目录（如果为 None，使用默认路径或环境变量）
            collection_name: 集合名称
        """
        # 从环境变量获取配置，如果没有则使用默认值
        self.db_path = Path(
            db_path or 
            os.getenv("RAG_DB_PATH") or 
            "doubao-rag/vector_db"
        )
        
        self.frames_dir = Path(
            frames_dir or 
            os.getenv("RAG_FRAMES_DIR") or 
            "doubao-rag/frames"
        )
        
        self.collection_name = collection_name
    
    def get_db_path(self) -> Path:
        """获取数据库路径（绝对路径）"""
        db_path = self.db_path
        if not db_path.is_absolute():
            # 如果是相对路径，尝试从项目根目录解析
            project_root = self._find_project_root()
            if project_root:
                db_path = project_root / db_path
        return db_path.resolve()
    
    def get_frames_dir(self) -> Path:
        """获取关键帧目录（绝对路径）"""
        frames_dir = self.frames_dir
        if not frames_dir.is_absolute():
            # 如果是相对路径，尝试从项目根目录解析
            project_root = self._find_project_root()
            if project_root:
                frames_dir = project_root / frames_dir
        return frames_dir.resolve()
    
    def _find_project_root(self) -> Optional[Path]:
        """查找项目根目录（包含 doubao-rag 目录的父目录）"""
        current = Path(__file__).parent.resolve()
        
        # 向上查找，直到找到包含 doubao-rag 的目录
        for parent in [current] + list(current.parents):
            if (parent / "doubao-rag").exists():
                return parent
        
        # 如果找不到，返回当前文件的父目录的父目录（假设在 doubao-rag/backend/）
        return current.parent.parent if current.name == "backend" else None
    
    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        return {
            "db_path": str(self.db_path),
            "frames_dir": str(self.frames_dir),
            "collection_name": self.collection_name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RAGDatabaseConfig":
        """从字典创建配置"""
        return cls(
            db_path=data.get("db_path"),
            frames_dir=data.get("frames_dir"),
            collection_name=data.get("collection_name", "video_frames")
        )
    
    def __repr__(self) -> str:
        return f"RAGDatabaseConfig(db_path={self.db_path}, frames_dir={self.frames_dir}, collection_name={self.collection_name})"


# 默认配置实例
default_config = RAGDatabaseConfig()

