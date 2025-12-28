// 修复HTML文件中的重复海报
const fs = require('fs');
const path = require('path');

const htmlFile = path.join(__dirname, 'frontend-nuxt', 'public', 'index.html');

// 读取HTML
let content = fs.readFileSync(htmlFile, 'utf-8');

// 提取所有卡片
const cardPattern = /<a class="card"[^>]*>.*?<\/a>/gs;
const cards = content.match(cardPattern) || [];

console.log(`总卡片数: ${cards.length}`);

// 提取每个卡片的URL并去重
const urlPattern = /https:\/\/jubianage-1392491103\.cos\.ap-guangzhou\.myqcloud\.com\/poster\/([^"]+)/;
const seenUrls = new Map();
const uniqueCards = [];
let duplicateCount = 0;

cards.forEach((card, index) => {
  const urlMatch = card.match(urlPattern);
  if (urlMatch) {
    const url = urlMatch[0];
    if (!seenUrls.has(url)) {
      seenUrls.set(url, true);
      uniqueCards.push(card);
    } else {
      duplicateCount++;
      console.log(`发现重复: 卡片 ${index + 1}, URL: ${url}`);
    }
  } else {
    uniqueCards.push(card);
  }
});

console.log(`\n去重后: ${uniqueCards.length} 个唯一卡片`);
console.log(`删除了 ${duplicateCount} 个重复卡片`);

if (duplicateCount > 0) {
  // 找到 marquee__track 的开始和结束位置
  const startMarker = '<div class="marquee__track" data-marquee-track>';
  const startIdx = content.indexOf(startMarker);
  
  if (startIdx === -1) {
    console.log('❌ 未找到 marquee__track');
    process.exit(1);
  }
  
  const sectionEnd = content.indexOf('</section>', startIdx);
  if (sectionEnd === -1) {
    console.log('❌ 未找到 </section>');
    process.exit(1);
  }
  
  const trackSection = content.substring(startIdx, sectionEnd);
  const lastDivIdx = trackSection.lastIndexOf('</div>');
  
  if (lastDivIdx === -1) {
    console.log('❌ 未找到 marquee__track 结束标签');
    process.exit(1);
  }
  
  const endIdx = startIdx + lastDivIdx + '</div>'.length;
  
  // 生成新的卡片HTML
  const formattedCards = uniqueCards.map((card, index) => {
    // 提取URL以确定比例
    const urlMatch = card.match(urlPattern);
    let ratioAttr = '';
    if (urlMatch) {
      const url = urlMatch[1];
      if (url.includes('/3-4/')) {
        ratioAttr = ' data-ratio="3-4"';
      } else if (url.includes('/7-10/')) {
        ratioAttr = ' data-ratio="7-10"';
      }
    }
    
    // 如果没有data-ratio但需要添加
    if (ratioAttr && !card.includes('data-ratio=')) {
      card = card.replace('<a class="card"', `<a class="card"${ratioAttr}`);
    }
    
    return card;
  });
  
  const newCardsHtml = formattedCards.join('\n');
  
  // 替换
  const before = content.substring(0, startIdx);
  const after = content.substring(endIdx);
  
  const newTrack = `          <div class="marquee__track" data-marquee-track>
            <!-- 只需要写一份 items，JS 会自动复制一份用于无缝循环 -->
${newCardsHtml}
          </div>`;
  
  const newContent = before + newTrack + after;
  
  // 备份并保存
  const backup = htmlFile.replace('.html', '.html.bak');
  fs.copyFileSync(htmlFile, backup);
  console.log(`\n✅ 已备份到: ${backup}`);
  
  fs.writeFileSync(htmlFile, newContent, 'utf-8');
  
  console.log(`✅ index.html 已修复`);
  console.log(`   原始卡片数: ${cards.length}`);
  console.log(`   去重后卡片数: ${uniqueCards.length}`);
  console.log(`   删除了 ${duplicateCount} 个重复卡片`);
} else {
  console.log('\n✅ 未发现重复的URL');
}

