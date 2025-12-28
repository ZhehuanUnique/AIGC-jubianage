"""
上传海报到腾讯云 COS
"""
import os
import sys
from pathlib import Path
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from dotenv import load_dotenv

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# 加载环境变量（尝试多个位置）
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
    load_dotenv()  # 尝试默认位置

# COS 配置
COS_SECRET_ID = os.getenv('COS_SECRET_ID')
COS_SECRET_KEY = os.getenv('COS_SECRET_KEY')
COS_REGION = os.getenv('COS_REGION', 'ap-guangzhou')
COS_BUCKET = os.getenv('COS_BUCKET', 'jubianage-1392491103')

# 调试：显示找到的配置（不显示完整密钥）
print(f"调试信息:")
print(f"  COS_SECRET_ID: {'已设置' if COS_SECRET_ID else '未设置'}")
print(f"  COS_SECRET_KEY: {'已设置' if COS_SECRET_KEY else '未设置'}")
print(f"  COS_REGION: {COS_REGION}")
print(f"  COS_BUCKET: {COS_BUCKET}")

# 检查配置
if not COS_SECRET_ID or not COS_SECRET_KEY:
    print("\n❌ 错误: 请在 .env 文件中配置 COS_SECRET_ID 和 COS_SECRET_KEY")
    print("   格式示例:")
    print("   COS_SECRET_ID=AKID...")
    print("   COS_SECRET_KEY=A7pI...")
    print("   COS_REGION=ap-guangzhou")
    sys.exit(1)

# 初始化 COS 客户端
config = CosConfig(
    Region=COS_REGION,
    SecretId=COS_SECRET_ID,
    SecretKey=COS_SECRET_KEY,
    Scheme='https'
)
client = CosS3Client(config)

# 海报源目录
POSTER_SOURCE = Path(__file__).parent / "poster"

# 路径映射：将中文冒号改为英文横线
PATH_MAPPING = {
    "2：3": "2-3",
    "3：4": "3-4",
    "7：10": "7-10"
}

def upload_file(local_path: Path, cos_key: str):
    """上传单个文件到 COS"""
    try:
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
        return False, str(e)

def upload_posters():
    """上传所有海报到 COS"""
    print("=" * 60)
    print("上传海报到腾讯云 COS")
    print("=" * 60)
    print(f"存储桶: {COS_BUCKET}")
    print(f"地域: {COS_REGION}")
    print(f"源目录: {POSTER_SOURCE}")
    print("-" * 60)
    
    if not POSTER_SOURCE.exists():
        print(f"❌ 源目录不存在: {POSTER_SOURCE}")
        return
    
    # 统计信息
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # 遍历所有图片文件
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    for ratio_folder in POSTER_SOURCE.iterdir():
        if not ratio_folder.is_dir():
            continue
        
        # 跳过非海报文件夹
        if ratio_folder.name not in PATH_MAPPING:
            continue
        
        # 获取 COS 中的路径（使用英文横线）
        cos_ratio = PATH_MAPPING[ratio_folder.name]
        print(f"\n📁 处理文件夹: {ratio_folder.name} -> {cos_ratio}")
        
        # 遍历文件夹中的图片
        for img_file in ratio_folder.iterdir():
            if not img_file.is_file():
                continue
            
            if img_file.suffix.lower() not in image_extensions:
                continue
            
            stats["total"] += 1
            
            # 构建 COS Key（路径）
            cos_key = f"poster/{cos_ratio}/{img_file.name}"
            
            # 检查文件是否已存在（可选，这里直接上传）
            print(f"  📤 上传: {img_file.name} -> {cos_key}")
            
            success, error = upload_file(img_file, cos_key)
            
            if success:
                stats["success"] += 1
                print(f"     ✅ 成功")
            else:
                stats["failed"] += 1
                print(f"     ❌ 失败: {error}")
    
    # 输出统计
    print("\n" + "=" * 60)
    print("上传统计")
    print("=" * 60)
    print(f"总计: {stats['total']} 个文件")
    print(f"成功: {stats['success']} 个")
    print(f"失败: {stats['failed']} 个")
    print(f"跳过: {stats['skipped']} 个")
    
    if stats['success'] > 0:
        print(f"\n✅ 上传完成！")
        print(f"访问地址: https://{COS_BUCKET}.cos.{COS_REGION}.myqcloud.com/poster/")
    else:
        print(f"\n❌ 没有文件上传成功")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        upload_posters()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

