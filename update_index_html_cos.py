"""
更新 index.html，使用 COS 的图片路径
"""
import sys
from pathlib import Path

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

POSTER_BASE = Path("C:/Users/Administrator/Desktop/poster")
INDEX_HTML = Path(__file__).parent / "frontend-nuxt" / "public" / "index.html"

# COS 配置
COS_BUCKET = "jubianage-1392491103"
COS_REGION = "ap-guangzhou"
COS_BASE_URL = f"https://{COS_BUCKET}.cos.{COS_REGION}.myqcloud.com"

# 比例文件夹映射（本地 -> COS）
RATIO_FOLDERS = {
    "2:3": ("2：3", "2-3"),
    "3:4": ("3：4", "3-4"),
    "7:10": ("7：10", "7-10")
}

def generate_poster_cards():
    """生成海报卡片 HTML（使用 COS URL）"""
    cards = []
    
    # 只处理2:3比例的海报
    ratio_order = ["2:3"]
    
    for ratio in ratio_order:
        local_folder_name, cos_folder_name = RATIO_FOLDERS[ratio]
        folder_path = POSTER_BASE / local_folder_name
        
        if not folder_path.exists():
            print(f"⚠️  文件夹不存在: {folder_path}")
            continue
        
        # 获取该文件夹下的所有图片
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        images = []
        
        for ext in image_extensions:
            images.extend(folder_path.glob(f"*{ext}"))
            images.extend(folder_path.glob(f"*{ext.upper()}"))
        
        # 过滤掉带 _1 后缀的文件（这些是重复的）
        images = [img for img in images if not img.name.endswith('_1.jpg') and not img.name.endswith('_1.png') and not img.name.endswith('_1.jpeg') and not img.name.endswith('_1.JPG') and not img.name.endswith('_1.PNG')]
        
        # 去重：使用文件名（不含路径）作为唯一标识，并排除 _1 后缀
        seen_names = set()
        unique_images = []
        for img in images:
            # 跳过 _1 后缀的文件
            base_name = img.name
            if base_name.endswith('_1.jpg') or base_name.endswith('_1.png') or base_name.endswith('_1.jpeg'):
                continue
            # 如果文件名（去掉_1后缀）已经存在，也跳过
            name_without_suffix = base_name.replace('_1.jpg', '.jpg').replace('_1.png', '.png').replace('_1.jpeg', '.jpeg')
            if name_without_suffix in seen_names:
                continue
            if img.name not in seen_names:
                seen_names.add(img.name)
                seen_names.add(name_without_suffix)  # 也记录去掉_1后缀的版本
                unique_images.append(img)
        images = unique_images
        
        # 按文件名排序
        images.sort(key=lambda x: x.name)
        
        print(f"📁 {local_folder_name}: 找到 {len(images)} 个唯一图片")
        
        # 生成卡片
        for idx, img_path in enumerate(images, 1):
            # 使用 COS 的完整 URL
            img_src = f"{COS_BASE_URL}/poster/{cos_folder_name}/{img_path.name}"
            
            # 生成标题和描述
            card_num = len(cards) + 1
            title = f"AIGC 片段 {card_num:02d}"
            
            # 根据比例生成描述
            descriptions = {
                "2:3": "竖版海报 · 2:3 比例",
                "3:4": "竖版海报 · 3:4 比例",
                "7:10": "竖版海报 · 7:10 比例"
            }
            subtitle = descriptions.get(ratio, "海报展示")
            
            # 统一使用2:3比例，不添加data-ratio属性
            card_html = f'''            <a class="card" href="javascript:void(0)" aria-label="视频 {card_num:02d}">
              <div class="card__thumb">
                <img class="card__img" src="{img_src}" alt="封面 {card_num:02d}" loading="lazy" />
              </div>
              <div class="card__meta">
                <div class="card__title">{title}</div>
                <div class="card__sub">{subtitle}</div>
              </div>
            </a>'''
            
            cards.append(card_html)
    
    return "\n".join(cards)

def update_index_html():
    """更新 index.html 文件"""
    print("=" * 60)
    print("更新 index.html（使用 COS URL）")
    print("=" * 60)
    
    if not INDEX_HTML.exists():
        print(f"❌ index.html 不存在: {INDEX_HTML}")
        return
    
    # 读取原始 HTML
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新的海报卡片
    new_cards = generate_poster_cards()
    
    if not new_cards:
        print("⚠️  未找到任何海报图片")
        return
    
    # 查找并替换海报卡片部分
    start_marker = '<div class="marquee__track" data-marquee-track>'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("❌ 未找到 marquee__track 标记")
        return
    
    # 找到 marquee__track 的结束标签（下一个 </div>）
    # 需要找到与开始标签匹配的结束标签
    # 先找到 </section>（rail 的结束）
    section_end = content.find('</section>', start_idx)
    if section_end == -1:
        print("❌ 未找到 </section> 标记")
        return
    
    # 在 start_idx 和 section_end 之间查找 marquee__track 的结束标签
    # 查找最后一个 </div>，它应该是 marquee__track 的结束
    track_section = content[start_idx:section_end]
    
    # 找到最后一个 </div>（这是 marquee__track 的结束标签）
    # 需要找到与 <div class="marquee__track" 匹配的 </div>
    # 简单方法：从后往前找第一个 </div>
    last_div_idx = track_section.rfind('</div>')
    
    if last_div_idx == -1:
        print("❌ 未找到 marquee__track 结束标记")
        return
    
    # 计算实际结束位置（start_idx + last_div_idx + len('</div>')）
    end_idx = start_idx + last_div_idx + len('</div>')
    
    # 替换整个 marquee__track 内容（包括开始和结束标签）
    before = content[:start_idx]
    after = content[end_idx:]
    
    # 新的 marquee__track 内容
    new_track_content = f'''          <div class="marquee__track" data-marquee-track>
            <!-- 只需要写一份 items，JS 会自动复制一份用于无缝循环 -->
{new_cards}
          </div>'''
    
    new_content = before + new_track_content + after
    
    # 保存更新后的 HTML
    import shutil
    backup_path = INDEX_HTML.with_suffix('.html.bak')
    shutil.copy2(INDEX_HTML, backup_path)
    print(f"✅ 已备份原文件到: {backup_path}")
    
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ index.html 已更新")
    print(f"   共添加 {len(new_cards.split('</a>')) - 1} 个海报卡片")
    print(f"   COS 地址: {COS_BASE_URL}/poster/")
    
    # 统计各比例的数量
    for ratio, (local_name, cos_name) in RATIO_FOLDERS.items():
        folder_path = POSTER_BASE / local_name
        if folder_path.exists():
            images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
            print(f"   - {local_name} ({cos_name}): {len(images)} 个")

if __name__ == "__main__":
    try:
        update_index_html()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

