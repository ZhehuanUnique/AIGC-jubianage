# Vercel 部署配置指南

## 当前状态

✅ **代码已提交到本地仓库**
- 包含完整的 Nuxt 3 前端项目
- 已配置 Vercel 部署文件

## Vercel 部署步骤

### 1. 在 Vercel Dashboard 中配置项目

1. **登录 Vercel Dashboard**
   - 访问 https://vercel.com/dashboard
   - 使用 GitHub 账号登录

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择 `ZhehuanUnique/AIGC-jubianage` 仓库
   - 点击 "Import"

3. **配置项目设置** ⚠️ **重要**
   
   **Root Directory**: 设置为 `frontend-nuxt`
   - 在 "Configure Project" 页面
   - 找到 "Root Directory" 选项
   - 点击 "Edit"
   - 输入：`frontend-nuxt`
   - 点击 "Save"

4. **框架预设**
   - Framework Preset: **Nuxt.js**（应该自动检测）
   - Build Command: `npm run build`（自动）
   - Output Directory: `.output/public`（自动）
   - Install Command: `npm install`（自动）

5. **环境变量**（可选）
   - 如果需要自定义后端地址，添加：
     - Key: `BACKEND_URL`
     - Value: `https://jubianai-backend.onrender.com`

6. **部署**
   - 点击 "Deploy"
   - 等待构建完成

### 2. 自定义域名（可选）

如果你有 `jubianai.cn` 域名：

1. 在项目设置中，进入 "Domains"
2. 添加你的域名：`jubianai.cn`
3. 按照提示配置 DNS 记录
4. 等待 DNS 生效（通常几分钟到几小时）

### 3. 自动部署

✅ **已配置自动部署**
- 每次推送到 `main` 分支，Vercel 会自动部署
- 你可以在 Vercel Dashboard 中查看部署状态

## 项目结构

```
AIGC-jubianage/
├── frontend-nuxt/          # Nuxt 3 前端项目（Vercel 部署此目录）
│   ├── pages/              # 页面
│   ├── layouts/            # 布局
│   ├── stores/             # Pinia 状态管理
│   ├── assets/             # 静态资源
│   ├── nuxt.config.ts      # Nuxt 配置
│   ├── vercel.json         # Vercel 配置
│   └── package.json        # 依赖
├── jubianai/               # 后端项目（Render 部署）
└── ...
```

## 验证部署

部署成功后：

1. **访问部署 URL**
   - Vercel 会提供一个 URL，如：`https://aigc-jubianage.vercel.app`
   - 或者你的自定义域名：`https://jubianai.cn`

2. **测试功能**
   - ✅ 视频生成页面
   - ✅ 资产管理页面
   - ✅ 知识库页面（预留）
   - ✅ 首尾帧上传
   - ✅ 视频生成和下载

## 常见问题

### 问题 1: 构建失败

**原因**: Root Directory 未设置或设置错误

**解决**: 
- 在 Vercel Dashboard 中设置 Root Directory 为 `frontend-nuxt`
- 重新部署

### 问题 2: 页面 404

**原因**: Nuxt 路由配置问题

**解决**: 
- 检查 `vercel.json` 中的 `rewrites` 配置
- 确保所有路由都重定向到 `/index.html`

### 问题 3: API 请求失败

**原因**: 后端地址配置错误或 CORS 问题

**解决**:
- 检查 `nuxt.config.ts` 中的 `backendUrl`
- 确保后端（Render）已部署并运行
- 检查后端 CORS 配置

## 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] Vercel 项目已创建
- [ ] Root Directory 设置为 `frontend-nuxt`
- [ ] 框架预设为 Nuxt.js
- [ ] 环境变量已配置（如需要）
- [ ] 首次部署成功
- [ ] 自定义域名已配置（如需要）
- [ ] 所有功能测试通过

## 下一步

1. **推送代码到 GitHub**（如果还没推送）
   ```bash
   git push origin main
   ```

2. **在 Vercel Dashboard 中配置项目**
   - 设置 Root Directory 为 `frontend-nuxt`
   - 点击 Deploy

3. **等待部署完成**
   - 查看构建日志
   - 确认部署成功

4. **测试部署**
   - 访问部署 URL
   - 测试所有功能

