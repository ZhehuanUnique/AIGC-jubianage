# Vercel 部署修复指南 - www.jubianai.cn

## 🔴 当前问题

访问 https://www.jubianai.cn/ 返回 404 错误，说明静态文件没有被正确部署。

## ✅ 解决方案

### 步骤 1：检查 Vercel 项目设置

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 进入项目 `jubianai` 或 `AIGC-jubianage`
3. 点击 **Settings** → **General**
4. **检查 Root Directory 设置**：
   - ✅ 应该设置为 **空** 或 **`./`**
   - ❌ 不能是 `jubianai` 或其他子目录

### 步骤 2：确认文件已提交到 Git

确保以下文件已提交到 Git：

```bash
git add index.html styles.css main.js index.mp4 vercel.json
git add logo/ 封面/
git commit -m "Fix: Add static files for Vercel deployment"
git push
```

### 步骤 3：检查 vercel.json 配置

当前 `vercel.json` 配置应该是：

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    },
    {
      "source": "/(.*\\.(css|js|mp4|webm|jpg|jpeg|png|gif|svg|ico|woff|woff2|ttf|eot))",
      "destination": "/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 步骤 4：重新部署

在 Vercel Dashboard：
1. 点击 **Deployments**
2. 找到最新部署
3. 点击 **Redeploy**（重新部署）

或者推送代码后自动触发部署。

### 步骤 5：验证部署

部署完成后，检查以下 URL：

- ✅ `https://www.jubianai.cn/` - 应该显示主页（不是 404）
- ✅ `https://www.jubianai.cn/index.html` - 应该返回 HTML
- ✅ `https://www.jubianai.cn/styles.css` - 应该返回 CSS
- ✅ `https://www.jubianai.cn/main.js` - 应该返回 JavaScript
- ✅ `https://www.jubianai.cn/api/health` - 应该返回 API 响应

## 🔍 故障排查

### 如果还是 404

1. **检查构建日志**：
   - Vercel Dashboard → Deployments → 最新部署 → Build Logs
   - 查看是否有 "Uploading static files" 或错误信息

2. **检查文件是否存在**：
   ```bash
   # 在项目根目录
   ls -la index.html styles.css main.js
   ```

3. **检查 .gitignore**：
   确保 `index.html`、`styles.css`、`main.js` 没有被忽略

4. **尝试手动触发部署**：
   - 在 Vercel Dashboard 点击 "Redeploy"
   - 或者推送一个空提交：`git commit --allow-empty -m "Trigger deployment" && git push`

## 📋 必需文件清单

确保以下文件在项目根目录：

```
AIGC-jubianage/
├── index.html          ✅ 必需
├── styles.css          ✅ 必需
├── main.js            ✅ 必需
├── index.mp4          ✅ 必需（背景视频）
├── vercel.json        ✅ 必需（配置）
├── api/
│   └── index.py       ✅ 必需（API）
├── logo/              ✅ 必需（Logo 文件）
└── 封面/              ✅ 必需（封面图片）
```

## 🚀 快速修复命令

```bash
# 1. 确保所有文件已提交
git add index.html styles.css main.js index.mp4 vercel.json
git add logo/ 封面/ api/
git commit -m "Fix: Ensure all static files are committed"
git push

# 2. 在 Vercel Dashboard 重新部署
```

## 📝 注意事项

- **Root Directory 必须为空**：如果设置为 `jubianai`，Vercel 只会部署 `jubianai/` 目录，不会部署根目录的文件
- **文件必须在 Git 中**：Vercel 只部署 Git 仓库中的文件
- **vercel.json 必须在根目录**：用于配置路由和重写规则

