"""
向量数据库模块：使用 Chroma 存储和检索向量
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
import json
from datetime import datetime


class VectorDB:
    """向量数据库管理器"""
    
    def __init__(self, db_path: str = "doubao-rag/vector_db", collection_name: str = "video_frames"):
        """
        初始化向量数据库
        
        Args:
            db_path: 数据库存储路径
            collection_name: 集合名称
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化 Chroma 客户端
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "视频关键帧向量库"}
        )
    
    def add_frames(
        self,
        video_id: str,
        frame_paths: List[str],
        embeddings: np.ndarray,
        timestamps: List[float],
        metadata: Optional[List[Dict]] = None
    ) -> int:
        """
        添加视频帧向量到数据库
        
        Args:
            video_id: 视频 ID
            frame_paths: 帧文件路径列表
            embeddings: 向量矩阵 (n_frames, embedding_dim)
            timestamps: 时间戳列表
            metadata: 可选的元数据列表
            
        Returns:
            int: 添加的帧数量
        """
        if len(frame_paths) != len(embeddings) or len(frame_paths) != len(timestamps):
            raise ValueError("frame_paths, embeddings 和 timestamps 长度必须一致")
        
        # 准备数据
        ids = [f"{video_id}_frame_{i:06d}" for i in range(len(frame_paths))]
        embeddings_list = embeddings.tolist()
        
        # 准备元数据
        if metadata is None:
            metadata = [{}] * len(frame_paths)
        
        metadatas = []
        for i, (frame_path, timestamp, meta) in enumerate(zip(frame_paths, timestamps, metadata)):
            metadatas.append({
                "video_id": video_id,
                "frame_path": frame_path,
                "timestamp": str(timestamp),
                "frame_index": str(i),
                **meta
            })
        
        # 添加到集合
        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadatas
        )
        
        return len(frame_paths)
    
    def search(
        self,
        query_embedding: np.ndarray,
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        检索相似帧
        
        Args:
            query_embedding: 查询向量
            n_results: 返回结果数量
            filter_dict: 过滤条件（如 {"video_id": "xxx"}）
            
        Returns:
            List[Dict]: 检索结果，包含 id, distance, metadata
        """
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            where=filter_dict
        )
        
        # 格式化结果
        formatted_results = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "distance": results["distances"][0][i],
                    "metadata": results["metadatas"][0][i]
                })
        
        return formatted_results
    
    def search_by_text(
        self,
        text: str,
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        通过文本检索（需要先将文本转为向量）
        
        Args:
            text: 查询文本
            n_results: 返回结果数量
            filter_dict: 过滤条件
            
        Returns:
            List[Dict]: 检索结果
        """
        # 注意：这个方法需要外部提供文本向量化
        # 实际使用时，应该先调用 vectorizer.encode_text(text) 获取向量
        # 然后调用 search() 方法
        raise NotImplementedError("请先使用 vectorizer.encode_text() 获取向量，然后调用 search()")
    
    def get_video_frames(self, video_id: str) -> List[Dict]:
        """
        获取某个视频的所有帧
        
        Args:
            video_id: 视频 ID
            
        Returns:
            List[Dict]: 帧信息列表
        """
        results = self.collection.get(
            where={"video_id": video_id}
        )
        
        frames = []
        if results["ids"]:
            for i in range(len(results["ids"])):
                frames.append({
                    "id": results["ids"][i],
                    "metadata": results["metadatas"][i]
                })
        
        return frames
    
    def delete_video(self, video_id: str) -> bool:
        """
        删除某个视频的所有帧
        
        Args:
            video_id: 视频 ID
            
        Returns:
            bool: 是否成功
        """
        try:
            # 获取该视频的所有 ID
            results = self.collection.get(where={"video_id": video_id})
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
            return True
        except Exception as e:
            print(f"删除视频失败: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """
        获取数据库统计信息
        
        Returns:
            Dict: 统计信息
        """
        count = self.collection.count()
        return {
            "total_frames": count,
            "collection_name": self.collection.name
        }


