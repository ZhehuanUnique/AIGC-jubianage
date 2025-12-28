"""
LangGraph 工作流定义
"""
from typing import Dict, List
import sys
from pathlib import Path

# 添加当前目录到路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from langgraph.graph import StateGraph, END

from langgraph_state import VideoProcessState, RAGSearchState, PromptEnhanceState
from video_processor import VideoProcessor
from vectorizer import ImageVectorizer
from vector_db import VectorDB


class VideoProcessWorkflow:
    """视频处理工作流：提取帧 → 向量化 → 存储"""
    
    def __init__(
        self,
        db_path: str = "doubao-rag/vector_db",
        frames_dir: str = "doubao-rag/frames",
        model_name: str = "clip-ViT-B-32"
    ):
        self.video_processor = VideoProcessor(output_dir=frames_dir)
        self.vectorizer = ImageVectorizer(model_name=model_name)
        self.vector_db = VectorDB(db_path=db_path)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建工作流图"""
        workflow = StateGraph(VideoProcessState)
        
        # 添加节点
        workflow.add_node("extract_frames", self.extract_frames_node)
        workflow.add_node("vectorize", self.vectorize_node)
        workflow.add_node("store", self.store_node)
        
        # 定义流程
        workflow.set_entry_point("extract_frames")
        workflow.add_edge("extract_frames", "vectorize")
        workflow.add_edge("vectorize", "store")
        workflow.add_edge("store", END)
        
        return workflow.compile()
    
    def extract_frames_node(self, state: VideoProcessState) -> Dict:
        """提取关键帧"""
        video_path = state["video_path"]
        method = state["method"]
        interval_seconds = state.get("interval_seconds", 1.0)
        
        print(f"正在提取关键帧: {video_path}")
        
        if method == "interval":
            frames = self.video_processor.extract_frames_by_interval(
                video_path,
                interval_seconds=interval_seconds
            )
        else:
            frames = self.video_processor.extract_frames_by_scene_change(video_path)
        
        if not frames:
            raise ValueError("未能提取到关键帧")
        
        print(f"提取了 {len(frames)} 个关键帧")
        
        frame_paths = [frame[0] for frame in frames]
        timestamps = [frame[1] for frame in frames]
        
        return {
            "frames": frames,
            "frame_paths": frame_paths,
            "timestamps": timestamps
        }
    
    def vectorize_node(self, state: VideoProcessState) -> Dict:
        """向量化帧"""
        frame_paths = state["frame_paths"]
        
        print("正在向量化关键帧...")
        embeddings = self.vectorizer.encode_images(frame_paths)
        print(f"向量化完成，维度: {embeddings.shape}")
        
        return {"embeddings": embeddings}
    
    def store_node(self, state: VideoProcessState) -> Dict:
        """存储到向量数据库"""
        video_id = state["video_id"]
        frame_paths = state["frame_paths"]
        embeddings = state["embeddings"]
        timestamps = state["timestamps"]
        metadata = state.get("metadata")
        
        print("正在存储到向量数据库...")
        
        # 准备元数据
        frame_metadata = []
        if metadata:
            for _ in frame_paths:
                frame_metadata.append(metadata.copy())
        else:
            frame_metadata = None
        
        count = self.vector_db.add_frames(
            video_id=video_id,
            frame_paths=frame_paths,
            embeddings=embeddings,
            timestamps=timestamps,
            metadata=frame_metadata
        )
        
        result = {
            "video_id": video_id,
            "frames_count": count,
            "frame_paths": frame_paths,
            "timestamps": timestamps,
            "embedding_dim": embeddings.shape[1]
        }
        
        return {"result": result}
    
    def process(self, video_path: str, video_id: str, method: str = "interval", 
                interval_seconds: float = 1.0, metadata: Dict = None) -> Dict:
        """执行工作流"""
        initial_state = {
            "video_path": video_path,
            "video_id": video_id,
            "method": method,
            "interval_seconds": interval_seconds,
            "metadata": metadata,
            "frames": [],
            "frame_paths": [],
            "timestamps": [],
            "embeddings": None,
            "result": None
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["result"]


class RAGSearchWorkflow:
    """RAG 检索工作流：查询 → 向量化 → 检索"""
    
    def __init__(
        self,
        db_path: str = "doubao-rag/vector_db",
        model_name: str = "clip-ViT-B-32"
    ):
        self.vectorizer = ImageVectorizer(model_name=model_name)
        self.vector_db = VectorDB(db_path=db_path)
        self.db_path = db_path
        self.model_name = model_name
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建工作流图"""
        workflow = StateGraph(RAGSearchState)
        
        # 添加节点
        workflow.add_node("encode_query", self.encode_query_node)
        workflow.add_node("search", self.search_node)
        
        # 定义流程
        workflow.set_entry_point("encode_query")
        workflow.add_edge("encode_query", "search")
        workflow.add_edge("search", END)
        
        return workflow.compile()
    
    def encode_query_node(self, state: RAGSearchState) -> Dict:
        """编码查询（文本或图片）"""
        query_type = state["query_type"]
        
        if query_type == "text":
            query = state["query"]
            print(f"正在编码文本查询: {query}")
            embedding = self.vectorizer.encode_text(query)
        else:
            image_path = state["query_image_path"]
            print(f"正在编码图片查询: {image_path}")
            embedding = self.vectorizer.encode_image(image_path)
        
        return {"query_embedding": embedding}
    
    def search_node(self, state: RAGSearchState) -> Dict:
        """检索相似帧"""
        embedding = state["query_embedding"]
        n_results = state["n_results"]
        video_id = state.get("video_id")
        
        # 构建过滤条件
        filter_dict = None
        if video_id:
            filter_dict = {"video_id": video_id}
        
        print(f"正在检索，返回 {n_results} 个结果...")
        results = self.vector_db.search(
            query_embedding=embedding,
            n_results=n_results,
            filter_dict=filter_dict
        )
        
        return {"search_results": results}
    
    def search(self, query: str = None, image_path: str = None, 
               n_results: int = 5, video_id: str = None) -> List[Dict]:
        """执行检索工作流"""
        if query:
            query_type = "text"
            initial_state = {
                "query": query,
                "query_type": query_type,
                "query_image_path": None,
                "query_embedding": None,
                "video_id": video_id,
                "n_results": n_results,
                "search_results": [],
                "enhanced_prompt": None,
                "original_prompt": None
            }
        else:
            query_type = "image"
            initial_state = {
                "query": "",
                "query_type": query_type,
                "query_image_path": image_path,
                "query_embedding": None,
                "video_id": video_id,
                "n_results": n_results,
                "search_results": [],
                "enhanced_prompt": None,
                "original_prompt": None
            }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["search_results"]


class PromptEnhanceWorkflow:
    """提示词增强工作流：查询 → 检索 → 增强"""
    
    def __init__(
        self,
        db_path: str = "doubao-rag/vector_db",
        model_name: str = "clip-ViT-B-32"
    ):
        self.vectorizer = ImageVectorizer(model_name=model_name)
        self.vector_db = VectorDB(db_path=db_path)
        self.db_path = db_path
        self.model_name = model_name
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建工作流图"""
        workflow = StateGraph(PromptEnhanceState)
        
        # 添加节点
        workflow.add_node("encode_query", self.encode_query_node)
        workflow.add_node("search", self.search_node)
        workflow.add_node("enhance", self.enhance_node)
        
        # 定义流程
        workflow.set_entry_point("encode_query")
        workflow.add_edge("encode_query", "search")
        workflow.add_edge("search", "enhance")
        workflow.add_edge("enhance", END)
        
        return workflow.compile()
    
    def encode_query_node(self, state: PromptEnhanceState) -> Dict:
        """编码查询文本"""
        prompt = state["original_prompt"]
        print(f"正在编码提示词: {prompt}")
        embedding = self.vectorizer.encode_text(prompt)
        return {"query_embedding": embedding}
    
    def search_node(self, state: PromptEnhanceState) -> Dict:
        """检索相似帧"""
        embedding = state["query_embedding"]
        n_references = state["n_references"]
        video_id = state.get("video_id")
        
        # 构建过滤条件
        filter_dict = None
        if video_id:
            filter_dict = {"video_id": video_id}
        
        print(f"正在检索 {n_references} 个参考帧...")
        results = self.vector_db.search(
            query_embedding=embedding,
            n_results=n_references,
            filter_dict=filter_dict
        )
        
        return {"search_results": results}
    
    def enhance_node(self, state: PromptEnhanceState) -> Dict:
        """增强提示词"""
        original_prompt = state["original_prompt"]
        search_results = state["search_results"]
        
        enhanced_prompt = original_prompt
        reference_info = []
        
        if search_results:
            for frame in search_results:
                metadata = frame.get("metadata", {})
                timestamp = metadata.get("timestamp", "unknown")
                reference_info.append(f"参考时间点: {timestamp}s")
            
            if reference_info:
                enhanced_prompt = f"{original_prompt} [参考: {', '.join(reference_info)}]"
        
        return {
            "enhanced_prompt": enhanced_prompt,
            "reference_info": reference_info
        }
    
    def enhance(self, prompt: str, n_references: int = 3, 
                video_id: str = None) -> Dict:
        """执行增强工作流"""
        initial_state = {
            "original_prompt": prompt,
            "n_references": n_references,
            "video_id": video_id,
            "query_embedding": None,
            "search_results": [],
            "enhanced_prompt": "",
            "reference_info": []
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return {
            "original_prompt": final_state["original_prompt"],
            "enhanced_prompt": final_state["enhanced_prompt"],
            "references": final_state["search_results"],
            "reference_count": len(final_state["search_results"]),
            "reference_info": final_state["reference_info"]
        }

