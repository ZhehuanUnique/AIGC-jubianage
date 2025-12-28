"""
RAG 服务：整合视频处理、向量化和检索
"""
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
import sys

# 添加当前目录到路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from video_processor import VideoProcessor
from vectorizer import ImageVectorizer
from vector_db import VectorDB


class RAGService:
    """RAG 服务，整合所有功能"""
    
    def __init__(
        self,
        db_path: str = "doubao-rag/vector_db",
        frames_dir: str = "doubao-rag/frames",
        model_name: str = "clip-ViT-B-32"
    ):
        """
        初始化 RAG 服务
        
        Args:
            db_path: 向量数据库路径
            frames_dir: 关键帧存储目录
            model_name: CLIP 模型名称
        """
        self.video_processor = VideoProcessor(output_dir=frames_dir)
        self.vectorizer = ImageVectorizer(model_name=model_name)
        self.vector_db = VectorDB(db_path=db_path)
    
    def process_video(
        self,
        video_path: str,
        video_id: Optional[str] = None,
        method: str = "interval",
        interval_seconds: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        处理视频：提取帧 → 向量化 → 存储
        
        Args:
            video_path: 视频文件路径
            video_id: 视频 ID（如果不提供，使用文件名）
            method: 提取方法 ("interval" 或 "scene")
            interval_seconds: 提取间隔（秒）
            metadata: 额外的元数据
            
        Returns:
            Dict: 处理结果
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        # 生成视频 ID
        if video_id is None:
            video_id = video_path.stem
        
        # 提取关键帧
        print(f"正在提取关键帧: {video_path}")
        if method == "interval":
            frames = self.video_processor.extract_frames_by_interval(
                str(video_path), 
                interval_seconds=interval_seconds
            )
        else:
            frames = self.video_processor.extract_frames_by_scene_change(
                str(video_path)
            )
        
        if not frames:
            raise ValueError("未能提取到关键帧")
        
        print(f"提取了 {len(frames)} 个关键帧")
        
        # 提取帧路径和时间戳
        frame_paths = [frame[0] for frame in frames]
        timestamps = [frame[1] for frame in frames]
        
        # 向量化
        print("正在向量化关键帧...")
        embeddings = self.vectorizer.encode_images(frame_paths)
        print(f"向量化完成，维度: {embeddings.shape}")
        
        # 准备元数据
        frame_metadata = []
        if metadata:
            for _ in frames:
                frame_metadata.append(metadata.copy())
        else:
            frame_metadata = None
        
        # 存储到向量数据库
        print("正在存储到向量数据库...")
        count = self.vector_db.add_frames(
            video_id=video_id,
            frame_paths=frame_paths,
            embeddings=embeddings,
            timestamps=timestamps,
            metadata=frame_metadata
        )
        
        return {
            "video_id": video_id,
            "frames_count": count,
            "frame_paths": frame_paths,
            "timestamps": timestamps,
            "embedding_dim": embeddings.shape[1]
        }
    
    def search_similar_frames(
        self,
        query: str,
        n_results: int = 5,
        video_id: Optional[str] = None
    ) -> List[Dict]:
        """
        检索相似帧（通过文本查询）
        
        Args:
            query: 查询文本（如 "快速运镜"、"特写镜头"）
            n_results: 返回结果数量
            video_id: 可选，限制在特定视频中搜索
            
        Returns:
            List[Dict]: 检索结果
        """
        # 将文本转为向量
        query_embedding = self.vectorizer.encode_text(query)
        
        # 构建过滤条件
        filter_dict = None
        if video_id:
            filter_dict = {"video_id": video_id}
        
        # 检索
        results = self.vector_db.search(
            query_embedding=query_embedding,
            n_results=n_results,
            filter_dict=filter_dict
        )
        
        return results
    
    def search_by_image(
        self,
        image_path: str,
        n_results: int = 5,
        video_id: Optional[str] = None
    ) -> List[Dict]:
        """
        通过图片检索相似帧
        
        Args:
            image_path: 查询图片路径
            n_results: 返回结果数量
            video_id: 可选，限制在特定视频中搜索
            
        Returns:
            List[Dict]: 检索结果
        """
        # 将图片转为向量
        query_embedding = self.vectorizer.encode_image(image_path)
        
        # 构建过滤条件
        filter_dict = None
        if video_id:
            filter_dict = {"video_id": video_id}
        
        # 检索
        results = self.vector_db.search(
            query_embedding=query_embedding,
            n_results=n_results,
            filter_dict=filter_dict
        )
        
        return results
    
    def enhance_prompt(
        self,
        original_prompt: str,
        n_references: int = 3,
        video_id: Optional[str] = None
    ) -> Dict:
        """
        增强提示词：通过 RAG 检索相关帧，增强原始提示词
        
        Args:
            original_prompt: 原始提示词
            n_references: 参考帧数量
            video_id: 可选，限制在特定视频中搜索
            
        Returns:
            Dict: 增强后的提示词和相关帧信息
        """
        # 检索相似帧
        similar_frames = self.search_similar_frames(
            query=original_prompt,
            n_results=n_references,
            video_id=video_id
        )
        
        # 构建增强提示词
        enhanced_prompt = original_prompt
        
        if similar_frames:
            # 可以从元数据中提取信息来增强提示词
            # 这里简单地将相似度信息加入提示词
            reference_info = []
            for frame in similar_frames:
                metadata = frame.get("metadata", {})
                timestamp = metadata.get("timestamp", "unknown")
                reference_info.append(f"参考时间点: {timestamp}s")
            
            if reference_info:
                enhanced_prompt = f"{original_prompt} [参考: {', '.join(reference_info)}]"
        
        return {
            "original_prompt": original_prompt,
            "enhanced_prompt": enhanced_prompt,
            "references": similar_frames,
            "reference_count": len(similar_frames)
        }
    
    def delete_video(self, video_id: str) -> bool:
        """
        删除视频及其所有帧
        
        Args:
            video_id: 视频 ID
            
        Returns:
            bool: 是否成功
        """
        return self.vector_db.delete_video(video_id)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.vector_db.get_stats()

