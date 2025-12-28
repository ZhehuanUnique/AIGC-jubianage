#!/usr/bin/env python3
"""
通过 API 测试数据库配置
检查部署环境的数据库是否已配置
"""
import requests
import json
import sys

def check_database_via_api(backend_url):
    """通过 API 检查数据库配置"""
    print("=" * 60)
    print("通过 API 检查数据库配置")
    print("=" * 60)
    print(f"\n后端 URL: {backend_url}")
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查端点:")
    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        if response.status_code == 200:
            print(f"   [OK] 健康检查成功: {response.json()}")
        else:
            print(f"   [X] 健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"   [X] 无法连接到后端: {e}")
        return False
    
    # 2. 测试历史记录 API
    print("\n2. 测试历史记录 API:")
    try:
        response = requests.get(
            f"{backend_url}/api/v1/video/history?limit=1&offset=0",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] API 响应成功")
            print(f"       状态码: {response.status_code}")
            print(f"       总记录数: {data.get('total', 0)}")
            print(f"       返回记录数: {len(data.get('items', []))}")
            
            # 检查响应内容
            if data.get('total', 0) >= 0:
                print(f"   [OK] 数据库已配置（API 正常响应）")
                if data.get('total', 0) > 0:
                    print(f"   [OK] 数据库中有 {data.get('total', 0)} 条记录")
                else:
                    print(f"   [!] 数据库中暂无记录（这是正常的，如果还没有生成过视频）")
                return True
            else:
                print(f"   [X] API 响应格式异常")
                return False
        elif response.status_code == 503:
            print(f"   [X] 数据库未配置（服务不可用）")
            print(f"       响应: {response.text}")
            return False
        else:
            print(f"   [X] API 请求失败: {response.status_code}")
            print(f"       响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   [X] 请求失败: {e}")
        return False

if __name__ == "__main__":
    # 默认使用 Render 后端 URL，可以通过命令行参数覆盖
    backend_url = sys.argv[1] if len(sys.argv) > 1 else "https://jubianai-backend.onrender.com"
    
    success = check_database_via_api(backend_url)
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] 数据库配置检查完成 - 数据库已配置")
    else:
        print("[X] 数据库配置检查完成 - 数据库未配置或连接失败")
        print("\n解决方案:")
        print("1. 在 Render Dashboard 中设置 SUPABASE_DB_URL 环境变量")
        print("2. 参考 jubianai/RENDER_DB_SETUP.md 配置 Supabase")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


