#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传视频文件到腾讯云 COS
"""
import os
import sys
from pathlib import Path
from qcloud_cos import CosConfig, CosS3Client

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# COS 配置（从环境变量或 .env 文件读取）
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

COS_SECRET_ID = os.getenv('COS_SECRET_ID')
COS_SECRET_KEY = os.getenv('COS_SECRET_KEY')
COS_REGION = os.getenv('COS_REGION', 'ap-guangzhou')
COS_BUCKET = os.getenv('COS_BUCKET', 'jubianage-1392491103')

# 检查配置
if not COS_SECRET_ID or not COS_SECRET_KEY:
    print("❌ 错误: 请在 .env 文件中配置 COS_SECRET_ID 和 COS_SECRET_KEY")
    sys.exit(1)

# COS 基础URL
COS_BASE_URL = f"https://{COS_BUCKET}.cos.{COS_REGION}.myqcloud.com"

def upload_file(client, local_path: Path, cos_key: str):
    """上传单个文件到 COS"""
    try:
        file_size = local_path.stat().st_size
        print(f"  文件大小: {file_size / 1024 / 1024:.2f} MB")
        
        # 使用分块上传（适用于大文件）
        if file_size > 100 * 1024 * 1024:  # 大于100MB使用分块上传
            print("  使用分块上传...")
            response = client.upload_file(
                Bucket=COS_BUCKET,
                LocalFilePath=str(local_path),
                Key=cos_key,
                PartSize=10 * 1024 * 1024,  # 10MB per part
                MAXThread=5
            )
        else:
            # 小文件直接上传
            with open(local_path, 'rb') as fp:
                response = client.put_object(
                    Bucket=COS_BUCKET,
                    Body=fp,
                    Key=cos_key,
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
        return True, None
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return False, f"{str(e)}\n详细信息:\n{error_detail}"

def main():
    print("=" * 60)
    print("上传视频文件到腾讯云 COS")
    print("=" * 60)
    print(f"存储桶: {COS_BUCKET}")
    print(f"地域: {COS_REGION}")
    print("-" * 60)
    
    # 初始化 COS 客户端
    try:
        config = CosConfig(
            Region=COS_REGION,
            SecretId=COS_SECRET_ID,
            SecretKey=COS_SECRET_KEY,
            Scheme='https'
        )
        client = CosS3Client(config)
        print("✅ COS 客户端初始化成功\n")
    except ImportError as e:
        print(f"❌ 错误: 未安装 qcloud_cos 库")
        print("请运行: pip install cos-python-sdk-v5")
        return
    except Exception as e:
        print(f"❌ COS 客户端初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 要上传的视频文件列表
    video_files = [
        ("index.mp4", Path("index.mp4")),
        ("index.webm", Path("index.webm")),
        ("frontend-nuxt/public/index.mp4", Path("frontend-nuxt/public/index.mp4")),
        ("frontend-nuxt/public/index.webm", Path("frontend-nuxt/public/index.webm")),
    ]
    
    uploaded_urls = {}
    stats = {"total": 0, "success": 0, "failed": 0}
    
    for display_name, local_path in video_files:
        if not local_path.exists():
            print(f"⚠️  跳过: {display_name} (文件不存在)")
            continue
        
        stats["total"] += 1
        cos_key = f"videos/{local_path.name}"
        
        print(f"📤 [{stats['total']}] 上传: {display_name}")
        print(f"  COS路径: {cos_key}")
        
        success, error = upload_file(client, local_path, cos_key)
        
        if success:
            stats["success"] += 1
            url = f"{COS_BASE_URL}/{cos_key}"
            uploaded_urls[local_path.name] = url
            print(f"  ✅ 成功")
            print(f"  URL: {url}")
        else:
            stats["failed"] += 1
            print(f"  ❌ 失败: {error}")
        print()
    
    # 输出统计
    print("=" * 60)
    print("上传统计")
    print("=" * 60)
    print(f"总计: {stats['total']} 个文件")
    print(f"成功: {stats['success']} 个")
    print(f"失败: {stats['failed']} 个")
    
    if stats['success'] > 0:
        print(f"\n✅ 上传完成！")
        print("\n上传的文件URL:")
        for filename, url in uploaded_urls.items():
            print(f"  {filename}: {url}")
        
        # 询问是否删除本地文件
        print("\n" + "=" * 60)
        print("删除本地文件")
        print("=" * 60)
        
        deleted_files = []
        for display_name, local_path in video_files:
            if local_path.exists() and local_path.name in uploaded_urls:
                try:
                    local_path.unlink()
                    deleted_files.append(display_name)
                    print(f"✅ 已删除: {display_name}")
                except Exception as e:
                    print(f"❌ 删除失败 {display_name}: {e}")
        
        if deleted_files:
            print(f"\n✅ 已删除 {len(deleted_files)} 个本地文件")
            
            # 更新 index.html 中的视频URL
            update_index_html_video_urls(uploaded_urls)
    else:
        print(f"\n❌ 没有文件上传成功")
    
    print("=" * 60)

def update_index_html_video_urls(uploaded_urls):
    """更新 index.html 中的视频URL为COS地址"""
    index_html_path = Path("frontend-nuxt/public/index.html")
    if not index_html_path.exists():
        index_html_path = Path("index.html")
    
    if not index_html_path.exists():
        print("\n⚠️  未找到 index.html，请手动更新视频URL")
        return
    
    try:
        content = index_html_path.read_text(encoding='utf-8')
        original_content = content
        
        # 替换视频URL
        if 'index.mp4' in uploaded_urls:
            mp4_url = uploaded_urls['index.mp4']
            content = content.replace('src="/index.mp4"', f'src="{mp4_url}"')
            content = content.replace('src="./index.mp4"', f'src="{mp4_url}"')
        
        if 'index.webm' in uploaded_urls:
            webm_url = uploaded_urls['index.webm']
            content = content.replace('src="/index.webm"', f'src="{webm_url}"')
            content = content.replace('src="./index.webm"', f'src="{webm_url}"')
        
        if content != original_content:
            index_html_path.write_text(content, encoding='utf-8')
            print(f"\n✅ 已更新 {index_html_path} 中的视频URL")
        else:
            print(f"\n⚠️  {index_html_path} 中未找到需要更新的视频URL")
    except Exception as e:
        print(f"\n❌ 更新 index.html 失败: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

