"""
导入桌面 Posters 文件夹中的图片，根据尺寸自动分类到 poster 文件夹
"""
import os
import sys
import shutil
from pathlib import Path
from PIL import Image
import json

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# 配置路径
DESKTOP_PATH = Path.home() / "Desktop"
POSTERS_SOURCE = DESKTOP_PATH / "Posters"
POSTER_BASE = Path(__file__).parent / "poster"

# 比例文件夹映射
RATIO_FOLDERS = {
    "2:3": "2：3",
    "3:4": "3：4",
    "7:10": "7：10"
}

# 比例容差（允许一定的误差）
RATIO_TOLERANCE = 0.05

def calculate_ratio(width, height):
    """计算宽高比"""
    if height == 0:
        return None
    return width / height

def classify_ratio(width, height):
    """
    根据尺寸分类图片到对应的比例文件夹
    返回比例名称（如 "2:3"）或 None
    """
    ratio = calculate_ratio(width, height)
    if ratio is None:
        return None
    
    # 定义目标比例
    target_ratios = {
        "2:3": 2/3,      # 0.6667
        "3:4": 3/4,      # 0.75
        "7:10": 7/10     # 0.7
    }
    
    # 找到最接近的比例
    best_match = None
    min_diff = float('inf')
    
    for ratio_name, target_ratio in target_ratios.items():
        diff = abs(ratio - target_ratio)
        if diff < min_diff and diff < RATIO_TOLERANCE:
            min_diff = diff
            best_match = ratio_name
    
    return best_match

def get_image_size(image_path):
    """获取图片尺寸"""
    try:
        with Image.open(image_path) as img:
            return img.size  # (width, height)
    except Exception as e:
        print(f"❌ 无法读取图片 {image_path}: {e}")
        return None

def import_posters():
    """导入并分类海报"""
    print("=" * 60)
    print("海报导入工具")
    print("=" * 60)
    
    # 1. 检查源文件夹
    if not POSTERS_SOURCE.exists():
        print(f"❌ 源文件夹不存在: {POSTERS_SOURCE}")
        print(f"   请确保桌面上有 'Posters' 文件夹")
        return
    
    print(f"✅ 源文件夹: {POSTERS_SOURCE}")
    
    # 2. 创建目标文件夹
    POSTER_BASE.mkdir(exist_ok=True)
    print(f"✅ 目标文件夹: {POSTER_BASE}")
    
    # 创建所有比例文件夹
    for ratio_name, folder_name in RATIO_FOLDERS.items():
        folder_path = POSTER_BASE / folder_name
        folder_path.mkdir(exist_ok=True)
        print(f"✅ 创建/检查文件夹: {folder_name}")
    
    # 3. 查找所有图片文件
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(POSTERS_SOURCE.glob(f"*{ext}"))
        image_files.extend(POSTERS_SOURCE.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"❌ 在 {POSTERS_SOURCE} 中未找到图片文件")
        return
    
    print(f"\n📁 找到 {len(image_files)} 个图片文件")
    print("-" * 60)
    
    # 4. 分类并复制图片
    stats = {
        "2:3": [],
        "3:4": [],
        "7:10": [],
        "unknown": []
    }
    
    for img_path in image_files:
        size = get_image_size(img_path)
        if size is None:
            stats["unknown"].append(str(img_path.name))
            continue
        
        width, height = size
        ratio_class = classify_ratio(width, height)
        
        if ratio_class:
            # 复制到对应文件夹
            folder_name = RATIO_FOLDERS[ratio_class]
            dest_folder = POSTER_BASE / folder_name
            dest_path = dest_folder / img_path.name
            
            # 如果文件已存在，添加序号
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                counter += 1
            
            shutil.copy2(img_path, dest_path)
            stats[ratio_class].append({
                "name": dest_path.name,
                "size": f"{width}x{height}",
                "ratio": f"{width/height:.4f}"
            })
            print(f"✅ {img_path.name} ({width}x{height}) → {folder_name}/{dest_path.name}")
        else:
            stats["unknown"].append({
                "name": img_path.name,
                "size": f"{width}x{height}",
                "ratio": f"{width/height:.4f}"
            })
            print(f"⚠️  {img_path.name} ({width}x{height}, 比例 {width/height:.4f}) → 未分类")
    
    # 5. 输出统计信息
    print("\n" + "=" * 60)
    print("导入统计")
    print("=" * 60)
    for ratio, items in stats.items():
        if ratio == "unknown":
            print(f"\n❓ 未分类 ({len(items)} 个):")
            for item in items[:5]:  # 只显示前5个
                if isinstance(item, dict):
                    print(f"   - {item['name']} ({item['size']}, 比例 {item['ratio']})")
                else:
                    print(f"   - {item}")
            if len(items) > 5:
                print(f"   ... 还有 {len(items) - 5} 个")
        else:
            folder_name = RATIO_FOLDERS[ratio]
            print(f"\n✅ {folder_name} ({len(items)} 个):")
            for item in items[:3]:  # 只显示前3个
                print(f"   - {item['name']} ({item['size']})")
            if len(items) > 3:
                print(f"   ... 还有 {len(items) - 3} 个")
    
    # 6. 保存统计信息到 JSON（用于后续生成 HTML）
    stats_file = POSTER_BASE / "posters_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 统计信息已保存到: {stats_file}")
    
    print("\n" + "=" * 60)
    print("✅ 导入完成！")
    print("=" * 60)

if __name__ == "__main__":
    try:
        import_posters()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

