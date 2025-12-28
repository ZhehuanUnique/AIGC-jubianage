"""
视频处理模块：提取关键帧
"""
import cv2
import os
from pathlib import Path
from typing import List, Tuple
import numpy as np


class VideoProcessor:
    """视频处理器，用于提取关键帧"""
    
    def __init__(self, output_dir: str = "doubao-rag/frames"):
        """
        初始化视频处理器
        
        Args:
            output_dir: 关键帧输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_frames_by_interval(
        self, 
        video_path: str, 
        interval_seconds: float = 1.0
    ) -> List[Tuple[str, float]]:
        """
        按时间间隔提取关键帧
        
        Args:
            video_path: 视频文件路径
            interval_seconds: 提取间隔（秒）
            
        Returns:
            List[Tuple[frame_path, timestamp]]: 提取的帧路径和时间戳列表
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_seconds)
        
        frames = []
        frame_count = 0
        timestamp = 0.0
        
        # 创建视频专用的输出目录
        video_name = video_path.stem
        video_output_dir = self.output_dir / video_name
        video_output_dir.mkdir(parents=True, exist_ok=True)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 按间隔提取帧
            if frame_count % frame_interval == 0:
                frame_filename = f"frame_{int(timestamp):06d}.jpg"
                frame_path = video_output_dir / frame_filename
                
                # 保存帧
                cv2.imwrite(str(frame_path), frame)
                frames.append((str(frame_path), timestamp))
            
            frame_count += 1
            timestamp = frame_count / fps
        
        cap.release()
        return frames
    
    def extract_frames_by_scene_change(
        self, 
        video_path: str, 
        threshold: float = 0.3
    ) -> List[Tuple[str, float]]:
        """
        基于场景变化提取关键帧（使用帧差法）
        
        Args:
            video_path: 视频文件路径
            threshold: 场景变化阈值（0-1）
            
        Returns:
            List[Tuple[frame_path, timestamp]]: 提取的帧路径和时间戳列表
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = []
        prev_frame = None
        frame_count = 0
        timestamp = 0.0
        
        # 创建视频专用的输出目录
        video_name = video_path.stem
        video_output_dir = self.output_dir / video_name
        video_output_dir.mkdir(parents=True, exist_ok=True)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # 计算帧差
                diff = cv2.absdiff(gray, prev_frame)
                diff_ratio = np.sum(diff > 30) / (diff.shape[0] * diff.shape[1])
                
                # 如果变化超过阈值，保存为关键帧
                if diff_ratio > threshold:
                    frame_filename = f"frame_{int(timestamp):06d}.jpg"
                    frame_path = video_output_dir / frame_filename
                    cv2.imwrite(str(frame_path), frame)
                    frames.append((str(frame_path), timestamp))
            
            prev_frame = gray
            frame_count += 1
            timestamp = frame_count / fps
        
        cap.release()
        
        # 确保至少提取第一帧
        if not frames:
            cap = cv2.VideoCapture(str(video_path))
            ret, frame = cap.read()
            if ret:
                frame_filename = "frame_000000.jpg"
                frame_path = video_output_dir / frame_filename
                cv2.imwrite(str(frame_path), frame)
                frames.append((str(frame_path), 0.0))
            cap.release()
        
        return frames
    
    def extract_frames(
        self, 
        video_path: str, 
        method: str = "interval",
        **kwargs
    ) -> List[Tuple[str, float]]:
        """
        提取关键帧（统一接口）
        
        Args:
            video_path: 视频文件路径
            method: 提取方法 ("interval" 或 "scene")
            **kwargs: 其他参数（interval_seconds, threshold 等）
            
        Returns:
            List[Tuple[frame_path, timestamp]]: 提取的帧路径和时间戳列表
        """
        if method == "interval":
            interval = kwargs.get("interval_seconds", 1.0)
            return self.extract_frames_by_interval(video_path, interval)
        elif method == "scene":
            threshold = kwargs.get("threshold", 0.3)
            return self.extract_frames_by_scene_change(video_path, threshold)
        else:
            raise ValueError(f"不支持的提取方法: {method}")


