#!/usr/bin/env python3
"""
测试视频生成时是否会保存到数据库
"""
import requests
import json
import sys
import time

def test_video_generation_save(backend_url):
    """测试视频生成并检查是否保存到数据库"""
    print("=" * 60)
    print("测试视频生成记录保存")
    print("=" * 60)
    print(f"\n后端 URL: {backend_url}")
    
    # 1. 先检查当前历史记录数量
    print("\n1. 检查当前历史记录:")
    try:
        response = requests.get(
            f"{backend_url}/api/v1/video/history?limit=100",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            initial_count = data.get('total', 0)
            print(f"   [OK] 当前记录数: {initial_count}")
        else:
            print(f"   [X] 获取历史记录失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [X] 请求失败: {e}")
        return False
    
    # 2. 提交一个测试视频生成任务
    print("\n2. 提交测试视频生成任务:")
    test_prompt = f"测试视频生成 - {int(time.time())}"
    try:
        payload = {
            "prompt": test_prompt,
            "duration": 5,
            "fps": 24,
            "width": 1280,
            "height": 720,
            "resolution": "720p"
        }
        
        print(f"   提示词: {test_prompt}")
        response = requests.post(
            f"{backend_url}/api/v1/video/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('task_id'):
                task_id = data.get('task_id')
                print(f"   [OK] 任务提交成功")
                print(f"   任务 ID: {task_id}")
            else:
                print(f"   [X] 任务提交失败: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"   [X] 请求失败: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   [X] 请求异常: {e}")
        return False
    
    # 3. 等待几秒，让后端有时间保存记录
    print("\n3. 等待后端保存记录...")
    time.sleep(3)
    
    # 4. 再次检查历史记录
    print("\n4. 检查历史记录是否更新:")
    try:
        response = requests.get(
            f"{backend_url}/api/v1/video/history?limit=100",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            new_count = data.get('total', 0)
            items = data.get('items', [])
            
            print(f"   [OK] 新记录数: {new_count}")
            
            # 查找刚提交的任务
            found_task = None
            for item in items:
                if item.get('task_id') == task_id or item.get('prompt') == test_prompt:
                    found_task = item
                    break
            
            if found_task:
                print(f"   [OK] 找到新任务记录!")
                print(f"       任务 ID: {found_task.get('task_id')}")
                print(f"       状态: {found_task.get('status')}")
                print(f"       提示词: {found_task.get('prompt')[:50]}...")
                return True
            else:
                print(f"   [X] 未找到新任务记录")
                print(f"   所有记录:")
                for item in items[:5]:  # 只显示前5条
                    print(f"      - {item.get('task_id')}: {item.get('prompt')[:30]}...")
                return False
        else:
            print(f"   [X] 获取历史记录失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [X] 请求失败: {e}")
        return False

if __name__ == "__main__":
    backend_url = sys.argv[1] if len(sys.argv) > 1 else "https://jubianai-backend.onrender.com"
    
    success = test_video_generation_save(backend_url)
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] 测试完成 - 视频生成记录已保存到数据库")
    else:
        print("[X] 测试完成 - 视频生成记录未保存到数据库")
        print("\n可能的原因:")
        print("1. 数据库未配置（SUPABASE_DB_URL 未设置）")
        print("2. 数据库保存失败（查看 Render 日志）")
        print("3. 数据库表不存在（需要运行 supabase_init.sql）")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


