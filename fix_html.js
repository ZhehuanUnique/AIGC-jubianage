// 修复 HTML：删除重复海报和 _1 后缀文件
const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'frontend-nuxt', 'public', 'index.html');

// 读取 HTML
let html = fs.readFileSync(htmlPath, 'utf-8');

// 提取所有唯一的 COS URL 海报（排除 _1 后缀）
const cosUrlPattern = /https:\/\/jubianage-1392491103\.cos\.ap-guangzhou\.myqcloud\.com\/poster\/([^"]+)/g;
const seenUrls = new Set();
const uniqueCards = [];

// 重新匹配所有 URL
html.replace(cosUrlPattern, (match, filename, offset) => {
  // 跳过 _1 后缀的文件
  if (filename.match(/_1\.(jpg|png|jpeg|JPG|PNG|JPEG)$/)) {
    return match;
  }
  
  // 只保留唯一的 URL
  if (!seenUrls.has(match)) {
    seenUrls.add(match);
    
    // 找到这个 URL 所在的完整卡片
    // 向前查找最近的 <a class="card"
    let cardStart = html.lastIndexOf('<a class="card"', offset);
    if (cardStart === -1) {
      cardStart = html.lastIndexOf('<a class="card"', offset - 1000);
    }
    
    // 向后查找对应的 </a>
    let cardEnd = html.indexOf('</a>', offset) + 5;
    
    if (cardStart !== -1 && cardEnd > cardStart && cardEnd < html.length) {
      const cardHtml = html.substring(cardStart, cardEnd);
      // 确保这是完整的卡片
      if (cardHtml.includes('card__img') && cardHtml.includes('card__meta')) {
        uniqueCards.push({ html: cardHtml, url: match });
      }
    }
  }
  
  return match;
});

console.log(`找到 ${uniqueCards.length} 个唯一海报`);

// 按比例和文件名排序
uniqueCards.sort((a, b) => {
  const getRatio = (url) => {
    if (url.includes('/2-3/')) return 1;
    if (url.includes('/3-4/')) return 2;
    if (url.includes('/7-10/')) return 3;
    return 0;
  };
  
  const ratioA = getRatio(a.url);
  const ratioB = getRatio(b.url);
  
  if (ratioA !== ratioB) {
    return ratioA - ratioB;
  }
  
  return a.url.localeCompare(b.url);
});

// 找到 marquee__track 的开始和结束
const trackStart = html.indexOf('<div class="marquee__track" data-marquee-track>');
const sectionEnd = html.indexOf('</section>', trackStart);

if (trackStart === -1 || sectionEnd === -1) {
  console.error('未找到 marquee__track 或 </section>');
  process.exit(1);
}

// 找到 marquee__track 的结束标签
const trackSection = html.substring(trackStart, sectionEnd);
const lastDiv = trackSection.lastIndexOf('</div>');
const trackEnd = trackStart + lastDiv + 6;

// 生成新的卡片 HTML（更新编号）
const newCards = uniqueCards.map((item, idx) => {
  const cardNum = String(idx + 1).padStart(2, '0');
  return item.html
    .replace(/aria-label="视频 \d+"/g, `aria-label="视频 ${cardNum}"`)
    .replace(/alt="封面 \d+"/g, `alt="封面 ${cardNum}"`)
    .replace(/AIGC 片段 \d+/g, `AIGC 片段 ${cardNum}`);
}).join('\n');

// 构建新的 marquee__track
const newTrack = `          <div class="marquee__track" data-marquee-track>
            <!-- 只需要写一份 items，JS 会自动复制一份用于无缝循环 -->
${newCards}
          </div>`;

// 替换
const newHtml = html.substring(0, trackStart) + newTrack + html.substring(trackEnd);

// 备份并保存
const backupPath = htmlPath + '.bak';
if (fs.existsSync(backupPath)) {
  fs.unlinkSync(backupPath);
}
fs.copyFileSync(htmlPath, backupPath);
console.log(`已备份到: ${backupPath}`);

fs.writeFileSync(htmlPath, newHtml, 'utf-8');
console.log(`✅ HTML 已修复，共 ${uniqueCards.length} 个唯一海报（已排除所有 _1 后缀文件）`);
