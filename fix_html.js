// 修复 HTML：删除重复海报
const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'frontend-nuxt', 'public', 'index.html');

// 读取 HTML
let html = fs.readFileSync(htmlPath, 'utf-8');

// 提取所有唯一的 COS URL 海报（排除 _1 后缀）
const cosUrlPattern = /https:\/\/jubianage-1392491103\.cos\.ap-guangzhou\.myqcloud\.com\/poster\/([^"]+)/g;
const seenUrls = new Set();
const uniqueCards = [];

let match;
while ((match = cosUrlPattern.exec(html)) !== null) {
  const url = match[0];
  const filename = match[1];
  
  // 跳过 _1 后缀的文件（包括 _1.jpg, _1.png, _1.jpeg 等）
  if (filename.match(/_1\.(jpg|png|jpeg|JPG|PNG|JPEG)$/)) {
    continue;
  }
  
  // 只保留唯一的 URL
  if (!seenUrls.has(url)) {
    seenUrls.add(url);
    
    // 提取完整的卡片 HTML
    const cardStart = html.lastIndexOf('<a class="card"', match.index);
    const cardEnd = html.indexOf('</a>', match.index) + 5;
    
    if (cardStart !== -1 && cardEnd > cardStart) {
      const cardHtml = html.substring(cardStart, cardEnd);
      uniqueCards.push(cardHtml);
    }
  }
}

console.log(`找到 ${uniqueCards.length} 个唯一海报`);

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

// 生成新的卡片 HTML
const newCards = uniqueCards.map((card, idx) => {
  // 更新编号
  return card
    .replace(/aria-label="视频 \d+"/g, `aria-label="视频 ${idx + 1}"`)
    .replace(/alt="封面 \d+"/g, `alt="封面 ${idx + 1}"`)
    .replace(/AIGC 片段 \d+/g, `AIGC 片段 ${idx + 1}`);
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
fs.copyFileSync(htmlPath, backupPath);
console.log(`已备份到: ${backupPath}`);

fs.writeFileSync(htmlPath, newHtml, 'utf-8');
console.log(`✅ HTML 已修复，共 ${uniqueCards.length} 个唯一海报`);

