"""
LangGraph 状态定义
"""
from typing import TypedDict, List, Dict, Optional
from typing_extensions import Annotated
import operator


class VideoProcessState(TypedDict):
    """视频处理状态"""
    video_path: str
    video_id: str
    method: str  # "interval" 或 "scene"
    interval_seconds: float
    metadata: Optional[Dict]
    frames: Annotated[List[tuple], operator.add]  # List[Tuple[frame_path, timestamp]]
    frame_paths: List[str]
    timestamps: List[float]
    embeddings: Optional[any]  # numpy array
    result: Optional[Dict]


class RAGSearchState(TypedDict):
    """RAG 检索状态"""
    query: str
    query_type: str  # "text" 或 "image"
    query_image_path: Optional[str]
    query_embedding: Optional[any]  # numpy array
    video_id: Optional[str]
    n_results: int
    search_results: List[Dict]
    enhanced_prompt: Optional[str]
    original_prompt: Optional[str]


class PromptEnhanceState(TypedDict):
    """提示词增强状态"""
    original_prompt: str
    n_references: int
    video_id: Optional[str]
    query_embedding: Optional[any]
    search_results: List[Dict]
    enhanced_prompt: str
    reference_info: List[str]

