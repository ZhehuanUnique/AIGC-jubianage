#!/usr/bin/env python3
"""
RAG API 测试脚本（Python 版本）
"""
import requests
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8001"

def test_health():
    """测试健康检查"""
    print("1. 测试健康检查接口...")
    response = requests.get(f"{BASE_URL}/health")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_stats():
    """测试统计信息"""
    print("2. 获取统计信息...")
    response = requests.get(f"{BASE_URL}/api/v1/rag/stats")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_upload_video(video_path: str = None):
    """测试上传视频"""
    if not video_path:
        video_path = Path(__file__).parent.parent / "index.mp4"
    
    if not Path(video_path).exists():
        print(f"3. 跳过视频上传（文件不存在: {video_path}）")
        print()
        return
    
    print(f"3. 上传视频 ({video_path})...")
    with open(video_path, 'rb') as f:
        files = {'file': f}
        data = {
            'video_id': f'test_video_{Path(video_path).stem}',
            'method': 'interval',
            'interval_seconds': 2.0
        }
        response = requests.post(f"{BASE_URL}/api/v1/rag/video/upload", files=files, data=data)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_search():
    """测试文本搜索"""
    print("4. 测试文本搜索...")
    data = {
        "query": "视频画面",
        "n_results": 3
    }
    response = requests.post(f"{BASE_URL}/api/v1/rag/search", json=data)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_enhance_prompt():
    """测试提示词增强"""
    print("5. 测试提示词增强...")
    data = {
        "prompt": "一个快速移动的镜头",
        "n_references": 2
    }
    response = requests.post(f"{BASE_URL}/api/v1/rag/enhance-prompt", json=data)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_search_by_image(image_path: str = None):
    """测试图片搜索"""
    if not image_path:
        # 尝试找一个帧图片
        frames_dir = Path(__file__).parent.parent / "doubao-rag" / "frames"
        if frames_dir.exists():
            for frame_file in frames_dir.rglob("*.jpg"):
                image_path = frame_file
                break
    
    if not image_path or not Path(image_path).exists():
        print("6. 跳过图片搜索（没有可用的图片）")
        print()
        return
    
    print(f"6. 测试图片搜索 ({image_path})...")
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'n_results': 3}
        response = requests.post(f"{BASE_URL}/api/v1/rag/search/image", files=files, data=data)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def main():
    """主函数"""
    print("=" * 50)
    print("RAG API 测试脚本")
    print("=" * 50)
    print()
    
    try:
        # 测试各个接口
        test_health()
        test_stats()
        
        # 如果有视频文件，测试上传
        video_path = sys.argv[1] if len(sys.argv) > 1 else None
        test_upload_video(video_path)
        
        test_search()
        test_enhance_prompt()
        test_search_by_image()
        
        # 再次获取统计信息
        print("7. 获取更新后的统计信息...")
        test_stats()
        
        print("=" * 50)
        print("测试完成！")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到 RAG 服务！")
        print("请确保服务正在运行：")
        print("  python -m uvicorn doubao-rag.backend.api:app --host 0.0.0.0 --port 8001")
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


