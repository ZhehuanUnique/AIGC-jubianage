"""
修复 index.html：删除重复海报，只保留唯一的 COS URL
"""
import sys
from pathlib import Path
import re

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

INDEX_HTML = Path(__file__).parent / "frontend-nuxt" / "public" / "index.html"
POSTER_BASE = Path("C:/Users/Administrator/Desktop/poster")

# COS 配置
COS_BUCKET = "jubianage-1392491103"
COS_REGION = "ap-guangzhou"
COS_BASE_URL = f"https://{COS_BUCKET}.cos.{COS_REGION}.myqcloud.com"

# 比例文件夹映射
RATIO_FOLDERS = {
    "2:3": ("2：3", "2-3"),
    "3:4": ("3：4", "3-4"),
    "7:10": ("7：10", "7-10")
}

def get_unique_images():
    """获取所有唯一的图片文件（排除 _1 后缀）"""
    all_images = {}
    
    for ratio, (local_name, cos_name) in RATIO_FOLDERS.items():
        folder_path = POSTER_BASE / local_name
        if not folder_path.exists():
            continue
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        images = []
        
        for ext in image_extensions:
            images.extend(folder_path.glob(f"*{ext}"))
            images.extend(folder_path.glob(f"*{ext.upper()}"))
        
        # 过滤掉带 _1 后缀的文件
        images = [img for img in images if not any(img.name.endswith(f'_1{ext}') for ext in image_extensions)]
        
        # 去重
        seen = set()
        for img in images:
            if img.name not in seen:
                seen.add(img.name)
                all_images[f"{cos_name}/{img.name}"] = {
                    'path': img,
                    'ratio': ratio,
                    'cos_url': f"{COS_BASE_URL}/poster/{cos_name}/{img.name}"
                }
    
    return all_images

def generate_cards():
    """生成唯一的卡片 HTML"""
    images = get_unique_images()
    
    # 按比例和文件名排序
    sorted_items = sorted(images.items(), key=lambda x: (
        ['2:3', '3:4', '7:10'].index(x[1]['ratio']),
        x[0]
    ))
    
    cards = []
    for idx, (key, info) in enumerate(sorted_items, 1):
        ratio = info['ratio']
        descriptions = {
            "2:3": "竖版海报 · 2:3 比例",
            "3:4": "竖版海报 · 3:4 比例",
            "7:10": "竖版海报 · 7:10 比例"
        }
        subtitle = descriptions.get(ratio, "海报展示")
        
        card_html = f'''            <a class="card" href="javascript:void(0)" aria-label="视频 {idx:02d}">
              <div class="card__thumb">
                <img class="card__img" src="{info['cos_url']}" alt="封面 {idx:02d}" loading="lazy" />
              </div>
              <div class="card__meta">
                <div class="card__title">AIGC 片段 {idx:02d}</div>
                <div class="card__sub">{subtitle}</div>
              </div>
            </a>'''
        cards.append(card_html)
    
    return "\n".join(cards), len(cards)

def fix_html():
    """修复 HTML 文件"""
    print("=" * 60)
    print("修复 index.html：删除重复海报")
    print("=" * 60)
    
    if not INDEX_HTML.exists():
        print(f"❌ index.html 不存在: {INDEX_HTML}")
        return
    
    # 读取 HTML
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新的卡片
    new_cards, card_count = generate_cards()
    print(f"✅ 生成了 {card_count} 个唯一海报卡片")
    
    # 找到 marquee__track 的开始和结束
    start_marker = '<div class="marquee__track" data-marquee-track>'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("❌ 未找到 marquee__track")
        return
    
    # 找到 </section>（rail 的结束）
    section_end = content.find('</section>', start_idx)
    if section_end == -1:
        print("❌ 未找到 </section>")
        return
    
    # 在 start_idx 和 section_end 之间找到最后一个 </div>（marquee__track 的结束）
    track_section = content[start_idx:section_end]
    last_div_idx = track_section.rfind('</div>')
    
    if last_div_idx == -1:
        print("❌ 未找到 marquee__track 结束标签")
        return
    
    end_idx = start_idx + last_div_idx + len('</div>')
    
    # 替换
    before = content[:start_idx]
    after = content[end_idx:]
    
    new_track = f'''          <div class="marquee__track" data-marquee-track>
            <!-- 只需要写一份 items，JS 会自动复制一份用于无缝循环 -->
{new_cards}
          </div>'''
    
    new_content = before + new_track + after
    
    # 备份并保存
    import shutil
    backup = INDEX_HTML.with_suffix('.html.bak')
    shutil.copy2(INDEX_HTML, backup)
    print(f"✅ 已备份到: {backup}")
    
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ index.html 已修复")
    print(f"   共 {card_count} 个唯一海报卡片")
    print(f"   COS 地址: {COS_BASE_URL}/poster/")

if __name__ == "__main__":
    try:
        fix_html()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

