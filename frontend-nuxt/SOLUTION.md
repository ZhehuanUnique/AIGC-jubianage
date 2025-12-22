# 解决 Vercel 250MB 限制问题

## 问题分析

Vercel 免费版限制：
- Serverless Function 未压缩大小不能超过 250MB
- 当前项目包含大量文件（后端代码、RAG 系统、视频文件等）

## 解决方案（推荐）：单独部署 Nuxt 前端

### 方案 A: 在现有仓库中单独部署前端（最简单）

**优点**：不需要创建新仓库，配置简单

**步骤**：

1. **在 Vercel 中修改项目设置**
   - 进入 Vercel Dashboard → 项目设置
   - **Root Directory**: 设置为 `frontend-nuxt`
   - **Framework Preset**: 选择 `Nuxt.js`
   - **Build Command**: `npm run build`（自动检测）
   - **Output Directory**: `.output/public`（自动检测）

2. **确保 `.vercelignore` 正确**
   - 已创建 `frontend-nuxt/.vercelignore`
   - 排除所有不必要的文件

3. **重新部署**
   - 在 Vercel Dashboard 中点击 "Redeploy"
   - 或推送新的 commit 到 GitHub

### 方案 B: 创建新的 GitHub 仓库（更清晰）

**优点**：项目结构更清晰，部署更独立

**步骤**：

1. **创建新的 GitHub 仓库**
   ```bash
   # 在本地创建新仓库
   mkdir jubianai-frontend
   cd jubianai-frontend
   git init
   ```

2. **复制前端文件**
   ```bash
   # 从当前项目复制 frontend-nuxt 目录的内容
   cp -r /workspaces/AIGC-jubianage/frontend-nuxt/* .
   ```

3. **创建新的 README**
   ```markdown
   # 剧变时代 - 前端应用
   
   基于 Vue 3 + Nuxt 3 的视频生成前端
   ```

4. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Nuxt 3 frontend"
   git remote add origin https://github.com/你的用户名/jubianai-frontend.git
   git push -u origin main
   ```

5. **在 Vercel 中创建新项目**
   - 连接新的 GitHub 仓库
   - 框架自动检测为 Nuxt.js
   - 添加自定义域名 `jubianai.cn`

### 方案 C: 使用 Monorepo 结构（高级）

如果未来需要同时管理多个项目，可以使用 Monorepo 工具如 Turborepo 或 Nx。

## 推荐方案：方案 A（最简单）

**为什么推荐方案 A**：
1. ✅ 不需要创建新仓库
2. ✅ 配置简单，只需修改 Root Directory
3. ✅ 代码仍然在一个仓库中，便于管理
4. ✅ 免费版即可使用

## 实施步骤（方案 A）

### 1. 在 Vercel Dashboard 中配置

1. 进入项目：`AIGC-jubianage`
2. 进入 **Settings** → **General**
3. 找到 **Root Directory** 设置
4. 输入：`frontend-nuxt`
5. 保存

### 2. 验证配置

Vercel 会自动检测：
- Framework: Nuxt.js
- Build Command: `npm run build`
- Output Directory: `.output/public`
- Install Command: `npm install`

### 3. 重新部署

1. 在 Vercel Dashboard 中点击 **Deployments**
2. 找到最新的部署
3. 点击 **...** → **Redeploy**
4. 或推送新的 commit 触发自动部署

### 4. 检查部署

- 查看构建日志，确认只构建了 `frontend-nuxt` 目录
- 确认构建大小小于 250MB
- 测试部署的页面功能

## 如果仍然超过 250MB

### 进一步优化

1. **检查 node_modules**
   ```bash
   cd frontend-nuxt
   du -sh node_modules
   ```
   如果太大，检查是否有不必要的依赖

2. **优化依赖**
   - 移除未使用的依赖
   - 使用 `npm prune` 清理

3. **检查构建产物**
   ```bash
   npm run build
   du -sh .output
   ```

4. **使用 Vercel 的 Build Cache**
   - Vercel 会自动缓存 node_modules
   - 确保 `.vercelignore` 正确配置

## 关于 Vercel 会员

**不需要充值会员**：
- 免费版已经足够使用
- 250MB 限制只针对 Serverless Functions
- Nuxt 3 前端部署通常远小于 250MB
- 通过正确配置 Root Directory 可以解决

**如果需要更大限制**：
- Pro 计划：500MB
- Enterprise：自定义限制
- 但对于前端项目，通常不需要

## 验证清单

部署前检查：
- [ ] Root Directory 设置为 `frontend-nuxt`
- [ ] `.vercelignore` 已创建并正确配置
- [ ] `vercel.json` 配置正确
- [ ] `package.json` 依赖合理
- [ ] 构建命令和输出目录正确

部署后检查：
- [ ] 构建成功（无 250MB 错误）
- [ ] 页面正常加载
- [ ] API 连接正常
- [ ] 功能测试通过

