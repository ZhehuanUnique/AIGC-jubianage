# Vercel 配置说明

## 📋 当前配置状态

### ✅ 已配置（无需修改）

主前端项目 `frontend-nuxt` 已经在 Vercel 上正确配置：

**配置文件位置**: `frontend-nuxt/vercel.json`

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".output/public",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nuxtjs",
  "routes": [
    {
      "src": "/",
      "dest": "/index.html"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Vercel 项目设置**（在 Vercel Dashboard 中）：
- ✅ **Root Directory**: `frontend-nuxt`
- ✅ **Framework Preset**: `Nuxt.js`（自动检测）
- ✅ **Build Command**: `npm run build`（自动检测）
- ✅ **Output Directory**: `.output/public`（自动检测）

---

## 🔧 环境变量配置

### 在 Vercel Dashboard 中配置

1. 进入 Vercel 项目
2. 点击 **Settings** → **Environment Variables**
3. 添加以下变量：

#### 必需的环境变量

```env
# 后端 API 地址
BACKEND_URL=https://jubianai-backend.onrender.com
```

#### 可选的环境变量

```env
# COS 存储基础 URL（如果使用）
COS_BASE_URL=https://jubianage-1392491103.cos.ap-guangzhou.myqcloud.com

# 其他配置...
```

---

## 📝 环境变量说明

### BACKEND_URL

前端应用连接的后端 API 地址。

**当前值**: `https://jubianai-backend.onrender.com`

**如果后端部署在其他地方**，更新此值：
- Docker 部署: `http://your-server-ip:8000`
- 其他云服务: `https://your-backend-url.com`

---

## 🚀 部署流程

### 自动部署

Vercel 会自动：
1. 监听 GitHub 仓库的 `main` 分支
2. 检测到推送后自动构建
3. 部署到生产环境

### 手动部署

1. 在 Vercel Dashboard 中点击 **Deployments**
2. 选择最新的部署
3. 点击 **Redeploy**

---

## ⚠️ 注意事项

### 1. Root Directory 设置

**重要**: 确保 Root Directory 设置为 `frontend-nuxt`（**没有尾部斜杠**）

如果显示为 `frontend-nuxt/`，改为 `frontend-nuxt`

### 2. 文件大小限制

- **Serverless Function**: 250MB（未压缩）
- **静态文件**: 无限制（通过 COS 存储）

### 3. 构建时间

- 免费版: 45 分钟
- Pro 版: 无限制

---

## 🔍 检查 Vercel 配置

### 在 Vercel Dashboard 中检查

1. **Settings** → **General**
   - ✅ Root Directory: `frontend-nuxt`
   - ✅ Framework: `Nuxt.js`

2. **Settings** → **Environment Variables**
   - ✅ `BACKEND_URL` 已设置

3. **Deployments**
   - ✅ 最新部署状态为 "Ready"
   - ✅ 构建日志无错误

### 验证部署

访问你的 Vercel 域名，检查：
- ✅ 页面正常加载
- ✅ API 请求成功
- ✅ 静态资源加载正常

---

## 🆘 常见问题

### Q: 部署失败，提示路径错误

**A**: 检查 Root Directory 设置，确保为 `frontend-nuxt`（无尾部斜杠）

### Q: 环境变量未生效

**A**: 
1. 确保在 Vercel Dashboard 中正确设置
2. 重新部署项目
3. 检查变量名是否正确（区分大小写）

### Q: 构建时间过长

**A**: 
- 检查 `node_modules` 大小
- 使用 `.vercelignore` 排除不必要的文件
- 考虑升级到 Pro 版本

### Q: 静态资源加载失败

**A**: 
- 检查文件路径是否正确
- 确保文件在 `frontend-nuxt/public/` 目录下
- 如果使用 COS，检查 URL 是否正确

---

## 📚 相关文档

- [Vercel Nuxt.js 文档](https://vercel.com/docs/frameworks/nuxtjs)
- [Vercel 环境变量](https://vercel.com/docs/concepts/projects/environment-variables)
- [Vercel 部署配置](https://vercel.com/docs/concepts/projects/overview)

---

**最后更新**: 2025-12-28

