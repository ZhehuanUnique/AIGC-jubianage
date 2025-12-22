# 静态文件部署检查清单

## 🔴 当前问题

- ✅ API 正常：`/api/health` 返回正常
- ❌ 主页 404：`/` 返回 404
- ❌ 静态资源 404：`/styles.css`、`/main.js` 返回 404

## ✅ 必须检查的 Vercel 设置

### 1. Root Directory（最重要！）

在 Vercel Dashboard：
1. 进入项目 → **Settings** → **General**
2. 找到 **Root Directory**
3. **必须设置为空或 `./`**
4. ❌ **不能是 `jubianai` 或其他子目录**

**为什么重要？**
- 如果 Root Directory = `jubianai`，Vercel 只会部署 `jubianai/` 目录
- 根目录的 `index.html`、`styles.css`、`main.js` 不会被部署
- 这就是为什么 API 正常（在 `api/` 目录），但静态文件 404

### 2. 文件必须在 Git 中

检查文件是否已提交：
```bash
git ls-files | grep -E "(index.html|styles.css|main.js|vercel.json)"
```

如果文件不在列表中，需要：
```bash
git add index.html styles.css main.js index.mp4 vercel.json
git add logo/ 封面/
git commit -m "Add static files for deployment"
git push
```

### 3. 检查 .gitignore

确保以下文件**没有被忽略**：
- `index.html`
- `styles.css`
- `main.js`
- `index.mp4`
- `vercel.json`
- `logo/`
- `封面/`

## 🚀 修复步骤

### 步骤 1：检查 Root Directory

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择项目
3. **Settings** → **General** → **Root Directory**
4. 设置为**空**（留空）或 `./`
5. 保存

### 步骤 2：确认文件已提交

```bash
# 检查文件是否存在
ls -la index.html styles.css main.js vercel.json

# 检查是否在 Git 中
git status

# 如果不在，添加并提交
git add index.html styles.css main.js index.mp4 vercel.json logo/ 封面/
git commit -m "Fix: Ensure static files are committed"
git push
```

### 步骤 3：重新部署

在 Vercel Dashboard：
1. **Deployments** → 最新部署
2. 点击 **Redeploy**
3. 等待部署完成

### 步骤 4：验证

部署完成后，检查：
- ✅ `https://www.jubianai.cn/` - 应该显示主页
- ✅ `https://www.jubianai.cn/styles.css` - 应该返回 CSS
- ✅ `https://www.jubianai.cn/main.js` - 应该返回 JS
- ✅ `https://www.jubianai.cn/api/health` - API 正常（已确认）

## 📋 必需文件清单

项目根目录必须包含：

```
AIGC-jubianage/
├── index.html          ✅ 主页
├── styles.css          ✅ 样式文件
├── main.js            ✅ JavaScript
├── index.mp4          ✅ 背景视频
├── vercel.json        ✅ Vercel 配置
├── api/
│   └── index.py       ✅ API（已正常工作）
├── logo/              ✅ Logo 文件
└── 封面/              ✅ 封面图片
```

## 🔍 如果还是 404

### 检查构建日志

1. Vercel Dashboard → **Deployments** → 最新部署
2. 点击部署 → **Build Logs**
3. 查找：
   - "Uploading static files"
   - "Uploading build outputs"
   - 任何错误信息

### 检查文件路径

确保文件路径正确：
- 文件必须在**项目根目录**（不是 `jubianai/` 子目录）
- `vercel.json` 必须在根目录

### 尝试手动触发

```bash
# 创建一个空提交触发部署
git commit --allow-empty -m "Trigger Vercel deployment"
git push
```

## 💡 常见问题

### Q: 为什么 API 正常但静态文件 404？

A: 因为：
- API 在 `api/` 目录（Vercel 标准位置），自动识别
- 静态文件在根目录，如果 Root Directory 设置错误，不会被部署

### Q: Root Directory 必须设置为空吗？

A: 是的，如果静态文件在根目录，Root Directory 必须为空或 `./`

### Q: 可以移动静态文件到子目录吗？

A: 可以，但需要：
1. 创建 `public/` 目录
2. 移动文件到 `public/`
3. 更新 `vercel.json` 配置
4. 但**不推荐**，保持根目录更简单

