# 部署检查清单

## ✅ 已完成

- [x] 代码已提交到本地仓库
  - Commit 1: `9c61cbd` - feat: 使用 Nuxt 3 替换 Streamlit 前端
  - Commit 2: `27a57d1` - chore: 更新前端配置和文档
- [x] 已切换到 HTTPS 远程地址
- [x] Vercel 配置文件已准备就绪

## 📋 待完成（请在本地执行）

### 1. 推送到 GitHub

在本地终端执行：

```bash
cd /workspaces/AIGC-jubianage

# 检查状态
git status

# 推送到 GitHub
git push origin main
```

如果提示输入凭据：
- **用户名**: 你的 GitHub 用户名
- **密码**: 使用 Personal Access Token（不是 GitHub 密码）
  - 生成 Token: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
  - 权限: 至少需要 `repo` 权限

### 2. 在 Vercel Dashboard 中配置

1. **访问 Vercel Dashboard**
   - https://vercel.com/dashboard

2. **导入项目**（如果还没导入）
   - 点击 "Add New..." → "Project"
   - 选择 `ZhehuanUnique/AIGC-jubianage`
   - 点击 "Import"

3. **设置 Root Directory** ⚠️ **非常重要**
   - 在项目设置中找到 "Root Directory"
   - 设置为：`frontend-nuxt`
   - 点击 "Save"

4. **检查框架预设**
   - Framework Preset: **Nuxt.js**
   - Build Command: `npm run build`
   - Output Directory: `.output/public`
   - Install Command: `npm install`

5. **环境变量**（可选）
   - 如果需要自定义后端地址：
     - Key: `BACKEND_URL`
     - Value: `https://jubianai-backend.onrender.com`

6. **部署**
   - 点击 "Deploy"
   - 等待构建完成（通常 2-5 分钟）

### 3. 验证部署

部署成功后：

1. **访问部署 URL**
   - Vercel 会提供：`https://aigc-jubianage-xxx.vercel.app`
   - 或你的自定义域名

2. **测试功能**
   - ✅ 首页加载正常
   - ✅ 视频生成页面可用
   - ✅ 可以输入提示词
   - ✅ 可以上传首帧图片
   - ✅ 可以点击"生成视频"按钮
   - ✅ 视频生成和下载功能正常

## 🎯 快速命令

```bash
# 1. 推送代码
git push origin main

# 2. 检查推送状态
git log --oneline origin/main..HEAD

# 3. 如果推送成功，Vercel 会自动部署
# 在 Vercel Dashboard 中查看部署状态
```

## 📝 注意事项

1. **Root Directory 必须设置**
   - 如果不设置，Vercel 会在根目录查找 `package.json`，可能找不到或找到错误的项目

2. **会员账户优势**
   - 更大的构建时间限制
   - 更大的函数大小限制
   - 更多的带宽

3. **自动部署**
   - 每次推送到 `main` 分支，Vercel 会自动触发部署
   - 可以在 Vercel Dashboard 中查看部署历史

## 🆘 如果遇到问题

1. **推送失败**
   - 检查网络连接
   - 确认 GitHub 凭据正确
   - 尝试使用 Personal Access Token

2. **Vercel 构建失败**
   - 检查 Root Directory 设置
   - 查看构建日志中的错误信息
   - 确认 `frontend-nuxt/package.json` 存在

3. **页面 404**
   - 检查 `vercel.json` 配置
   - 确认路由配置正确

## 📞 需要帮助？

如果遇到问题，请提供：
- 错误信息
- 构建日志
- 部署 URL

