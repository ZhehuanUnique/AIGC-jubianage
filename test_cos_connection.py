#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 COS 连接和配置
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 设置 UTF-8 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# 加载环境变量
env_paths = [
    Path(__file__).parent / ".env",
    Path(__file__).parent / "jubianai" / ".env",
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ 加载环境变量: {env_path}")
        break
else:
    load_dotenv()
    print("⚠️  使用默认位置加载环境变量")

# 检查配置
COS_SECRET_ID = os.getenv('COS_SECRET_ID')
COS_SECRET_KEY = os.getenv('COS_SECRET_KEY')
COS_REGION = os.getenv('COS_REGION', 'ap-guangzhou')
COS_BUCKET = os.getenv('COS_BUCKET', 'jubianage-1392491103')

print("\n" + "=" * 60)
print("COS 配置检查")
print("=" * 60)
print(f"COS_SECRET_ID: {'✅ 已设置' if COS_SECRET_ID else '❌ 未设置'}")
if COS_SECRET_ID:
    print(f"  值: {COS_SECRET_ID[:10]}...")
print(f"COS_SECRET_KEY: {'✅ 已设置' if COS_SECRET_KEY else '❌ 未设置'}")
if COS_SECRET_KEY:
    print(f"  值: {COS_SECRET_KEY[:10]}...")
print(f"COS_REGION: {COS_REGION}")
print(f"COS_BUCKET: {COS_BUCKET}")

if not COS_SECRET_ID or not COS_SECRET_KEY:
    print("\n❌ 错误: COS 配置不完整")
    sys.exit(1)

# 测试 COS 连接
try:
    from qcloud_cos import CosConfig, CosS3Client
    
    config = CosConfig(
        Region=COS_REGION,
        SecretId=COS_SECRET_ID,
        SecretKey=COS_SECRET_KEY,
        Scheme='https'
    )
    client = CosS3Client(config)
    
    print("\n" + "=" * 60)
    print("测试 COS 连接")
    print("=" * 60)
    
    # 列出存储桶中的文件
    try:
        response = client.list_objects(
            Bucket=COS_BUCKET,
            MaxKeys=10
        )
        
        if 'Contents' in response:
            print(f"✅ 连接成功！存储桶中有 {len(response['Contents'])} 个文件（显示前10个）:")
            for obj in response['Contents'][:10]:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("✅ 连接成功！但存储桶为空")
            
    except Exception as e:
        print(f"❌ 列出文件失败: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError:
    print("\n❌ 错误: 未安装 qcloud_cos 库")
    print("请运行: pip install cos-python-sdk-v5")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ 连接失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)

