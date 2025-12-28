"""
基于 LangGraph 的 RAG 服务
"""
from pathlib import Path
from typing import List, Dict, Optional
import sys

# 添加当前目录到路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from langgraph_workflows import (
    VideoProcessWorkflow,
    RAGSearchWorkflow,
    PromptEnhanceWorkflow
)


class LangGraphRAGService:
    """基于 LangGraph 的 RAG 服务"""
    
    def __init__(
        self,
        db_path: str = "doubao-rag/vector_db",
        frames_dir: str = "doubao-rag/frames",
        model_name: str = "clip-ViT-B-32"
    ):
        """
        初始化 LangGraph RAG 服务
        
        Args:
            db_path: 向量数据库路径
            frames_dir: 关键帧存储目录
            model_name: CLIP 模型名称
        """
        self.video_workflow = VideoProcessWorkflow(
            db_path=db_path,
            frames_dir=frames_dir,
            model_name=model_name
        )
        self.search_workflow = RAGSearchWorkflow(
            db_path=db_path,
            model_name=model_name
        )
        self.enhance_workflow = PromptEnhanceWorkflow(
            db_path=db_path,
            model_name=model_name
        )
    
    def process_video(
        self,
        video_path: str,
        video_id: Optional[str] = None,
        method: str = "interval",
        interval_seconds: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        处理视频：使用 LangGraph 工作流
        
        Args:
            video_path: 视频文件路径
            video_id: 视频 ID
            method: 提取方法
            interval_seconds: 提取间隔
            metadata: 元数据
            
        Returns:
            Dict: 处理结果
        """
        if video_id is None:
            video_id = Path(video_path).stem
        
        return self.video_workflow.process(
            video_path=video_path,
            video_id=video_id,
            method=method,
            interval_seconds=interval_seconds,
            metadata=metadata
        )
    
    def search_similar_frames(
        self,
        query: str,
        n_results: int = 5,
        video_id: Optional[str] = None
    ) -> List[Dict]:
        """
        搜索相似帧：使用 LangGraph 工作流
        
        Args:
            query: 查询文本
            n_results: 返回结果数量
            video_id: 可选，限制在特定视频中搜索
            
        Returns:
            List[Dict]: 检索结果
        """
        return self.search_workflow.search(
            query=query,
            n_results=n_results,
            video_id=video_id
        )
    
    def search_by_image(
        self,
        image_path: str,
        n_results: int = 5,
        video_id: Optional[str] = None
    ) -> List[Dict]:
        """
        通过图片搜索相似帧：使用 LangGraph 工作流
        
        Args:
            image_path: 查询图片路径
            n_results: 返回结果数量
            video_id: 可选，限制在特定视频中搜索
            
        Returns:
            List[Dict]: 检索结果
        """
        return self.search_workflow.search(
            image_path=image_path,
            n_results=n_results,
            video_id=video_id
        )
    
    def enhance_prompt(
        self,
        original_prompt: str,
        n_references: int = 3,
        video_id: Optional[str] = None
    ) -> Dict:
        """
        增强提示词：使用 LangGraph 工作流
        
        Args:
            original_prompt: 原始提示词
            n_references: 参考帧数量
            video_id: 可选，限制在特定视频中搜索
            
        Returns:
            Dict: 增强结果
        """
        return self.enhance_workflow.enhance(
            prompt=original_prompt,
            n_references=n_references,
            video_id=video_id
        )
    
    def delete_video(self, video_id: str) -> bool:
        """删除视频及其所有帧"""
        return self.video_workflow.vector_db.delete_video(video_id)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.video_workflow.vector_db.get_stats()




