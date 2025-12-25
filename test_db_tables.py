#!/usr/bin/env python3
"""
测试数据库表是否存在
"""
import requests
import json
import sys

def test_database_tables(backend_url):
    """通过 API 测试数据库表是否存在"""
    print("=" * 60)
    print("测试数据库表")
    print("=" * 60)
    print(f"\n后端 URL: {backend_url}")
    
    # 1. 测试历史记录 API（如果表不存在，可能会报错）
    print("\n1. 测试历史记录 API:")
    try:
        response = requests.get(
            f"{backend_url}/api/v1/video/history?limit=1&offset=0",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] API 响应成功")
            print(f"       状态码: {response.status_code}")
            print(f"       响应格式: {list(data.keys())}")
            
            # 如果返回空列表但没有错误，说明表可能存在
            if 'total' in data and 'items' in data:
                print(f"   [OK] API 响应格式正确")
                return True
            else:
                print(f"   [X] API 响应格式异常")
                return False
        elif response.status_code == 500:
            print(f"   [X] 服务器错误（可能是表不存在）")
            print(f"       响应: {response.text[:500]}")
            return False
        else:
            print(f"   [X] API 请求失败: {response.status_code}")
            print(f"       响应: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"   [X] 请求失败: {e}")
        return False

if __name__ == "__main__":
    backend_url = sys.argv[1] if len(sys.argv) > 1 else "https://jubianai-backend.onrender.com"
    
    success = test_database_tables(backend_url)
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] 数据库表检查完成 - API 正常响应")
        print("\n如果视频生成记录仍未保存，可能的原因：")
        print("1. 数据库表不存在（需要运行 supabase_init.sql）")
        print("2. 保存逻辑有问题（需要查看 Render 日志）")
    else:
        print("[X] 数据库表检查失败")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


