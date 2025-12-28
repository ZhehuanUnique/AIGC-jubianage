"""
向量化模块：将图片转为向量（使用 CLIP）
"""
from sentence_transformers import SentenceTransformer
from PIL import Image
import torch
from typing import List, Union
import numpy as np
from pathlib import Path


class ImageVectorizer:
    """图片向量化器，使用 CLIP 模型"""
    
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        """
        初始化向量化器
        
        Args:
            model_name: CLIP 模型名称
                - "clip-ViT-B-32": 默认，平衡速度和精度
                - "clip-ViT-L-14": 更高精度，但更慢
        """
        print(f"正在加载 CLIP 模型: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        print(f"模型已加载到设备: {self.device}")
    
    def encode_image(self, image_path: Union[str, Path, Image.Image]) -> np.ndarray:
        """
        将单张图片转为向量
        
        Args:
            image_path: 图片路径或 PIL Image 对象
            
        Returns:
            np.ndarray: 向量（通常是 512 维）
        """
        if isinstance(image_path, (str, Path)):
            image = Image.open(image_path)
        else:
            image = image_path
        
        # 确保图片是 RGB 模式
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # 使用 CLIP 编码图片
        embedding = self.model.encode(image, convert_to_numpy=True)
        return embedding
    
    def encode_images(self, image_paths: List[Union[str, Path]]) -> np.ndarray:
        """
        批量将图片转为向量
        
        Args:
            image_paths: 图片路径列表
            
        Returns:
            np.ndarray: 向量矩阵 (n_images, embedding_dim)
        """
        images = []
        for path in image_paths:
            image = Image.open(path)
            if image.mode != "RGB":
                image = image.convert("RGB")
            images.append(image)
        
        # 批量编码
        embeddings = self.model.encode(images, convert_to_numpy=True, show_progress_bar=True)
        return embeddings
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        将文本转为向量（用于文本检索）
        
        Args:
            text: 文本内容
            
        Returns:
            np.ndarray: 向量
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def get_embedding_dim(self) -> int:
        """获取向量维度"""
        # 测试编码获取维度
        test_image = Image.new("RGB", (224, 224), color="white")
        test_embedding = self.encode_image(test_image)
        return test_embedding.shape[0]


