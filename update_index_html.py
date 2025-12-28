"""
更新 index.html，动态加载所有海报
"""
import sys
import json
import shutil
from pathlib import Path

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

POSTER_BASE = Path(__file__).parent / "poster"
INDEX_HTML = Path(__file__).parent / "index.html"
STATS_FILE = POSTER_BASE / "posters_stats.json"

# 比例文件夹映射
RATIO_FOLDERS = {
    "2:3": "2：3",
    "3:4": "3：4",
    "7:10": "7：10"
}

def generate_poster_cards():
    """生成海报卡片 HTML"""
    cards = []
    
    # 按比例顺序处理
    ratio_order = ["2:3", "3:4", "7:10"]
    
    for ratio in ratio_order:
        folder_name = RATIO_FOLDERS[ratio]
        folder_path = POSTER_BASE / folder_name
        
        if not folder_path.exists():
            continue
        
        # 获取该文件夹下的所有图片
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        images = []
        
        for ext in image_extensions:
            images.extend(folder_path.glob(f"*{ext}"))
            images.extend(folder_path.glob(f"*{ext.upper()}"))
        
        # 按文件名排序
        images.sort(key=lambda x: x.name)
        
        # 生成卡片
        for idx, img_path in enumerate(images, 1):
            # 使用相对路径（从网站根目录开始）
            img_src = f"/poster/{folder_name}/{img_path.name}"
            
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
    print("更新 index.html")
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
    # 查找 <div class="marquee__track" data-marquee-track> 和对应的 </div> 之间的内容
    start_marker = '<div class="marquee__track" data-marquee-track>'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("❌ 未找到 marquee__track 标记")
        return
    
    # 找到对应的结束标记（在 </section> 之前）
    section_end = content.find('</section>', start_idx)
    if section_end == -1:
        print("❌ 未找到 section 结束标记")
        return
    
    # 在 section 结束前找到最后一个 </div>（这是 marquee__track 的结束标签）
    track_section = content[start_idx:section_end]
    last_div_idx = track_section.rfind('</div>')
    
    if last_div_idx == -1:
        print("❌ 未找到结束标记")
        return
    
    # 计算实际结束位置
    end_idx = start_idx + len(start_marker) + last_div_idx
    
    # 替换内容：保留开始标记和结束标记，只替换中间的内容
    before = content[:start_idx + len(start_marker)]
    after = content[end_idx:]
    
    new_content = before + "\n            <!-- 只需要写一份 items，JS 会自动复制一份用于无缝循环 -->\n" + new_cards + "\n          " + after
    
    # 保存更新后的 HTML
    backup_path = INDEX_HTML.with_suffix('.html.bak')
    shutil.copy2(INDEX_HTML, backup_path)
    print(f"✅ 已备份原文件到: {backup_path}")
    
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ index.html 已更新")
    print(f"   共添加 {len(new_cards.split('</a>')) - 1} 个海报卡片")
    
    # 统计各比例的数量
    for ratio, folder_name in RATIO_FOLDERS.items():
        folder_path = POSTER_BASE / folder_name
        if folder_path.exists():
            images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
            print(f"   - {folder_name}: {len(images)} 个")

if __name__ == "__main__":
    try:
        update_index_html()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

