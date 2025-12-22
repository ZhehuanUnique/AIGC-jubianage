# Vercel 部署指南

## 将 jubianai.cn 指向新的 Nuxt 3 前端

### 步骤 1: 在 Vercel 中部署 Nuxt 3 前端

1. **进入 Vercel Dashboard**
   - 访问 https://vercel.com/dashboard
   - 选择项目 `AIGC-jubianage` 或创建新项目

2. **配置项目设置**
   - **Root Directory**: 设置为 `frontend-nuxt`
   - **Framework Preset**: 选择 `Nuxt.js`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.output/public`
   - **Install Command**: `npm install`

3. **环境变量配置**
   在 Vercel 项目设置中添加环境变量：
   ```
   BACKEND_URL=https://jubianai-backend.onrender.com
   ```

### 步骤 2: 配置自定义域名 jubianai.cn

1. **在 Vercel 中添加域名**
   - 进入项目设置 → Domains
   - 添加域名：`jubianai.cn` 和 `www.jubianai.cn`

2. **配置 DNS 记录**
   在域名注册商（如阿里云、腾讯云等）的 DNS 管理中添加：
   
   **CNAME 记录**：
   ```
   类型: CNAME
   主机记录: @ (或留空)
   记录值: cname.vercel-dns.com
   ```
   
   **www 子域名**：
   ```
   类型: CNAME
   主机记录: www
   记录值: cname.vercel-dns.com
   ```

   **或者使用 A 记录**（如果 CNAME 不支持）：
   ```
   类型: A
   主机记录: @
   记录值: 76.76.21.21 (Vercel 的 IP，请查看 Vercel 提供的具体 IP)
   ```

3. **等待 DNS 生效**
   - DNS 记录通常需要几分钟到几小时生效
   - 可以在 Vercel Dashboard 中查看域名验证状态

### 步骤 3: 验证部署

1. **检查部署状态**
   - 在 Vercel Dashboard 的 Deployments 页面查看最新部署
   - 确保状态为 "Ready"（绿色）

2. **访问测试**
   - 访问 `https://jubianai.cn` 应该显示新的 Nuxt 3 前端
   - 检查页面功能是否正常

### 步骤 4: 更新根目录部署（如果需要保留旧页面）

如果根目录的 `index.html` 需要保留作为备用，可以：

1. **创建新的 Vercel 项目**专门用于 Nuxt 前端
2. **或者使用 Vercel 的路径重写**规则

### 注意事项

1. **SSL 证书**
   - Vercel 会自动为自定义域名配置 SSL 证书
   - 确保 DNS 记录正确后，SSL 证书会自动生成

2. **环境变量**
   - 确保在 Vercel 中设置了 `BACKEND_URL`
   - 生产环境使用：`https://jubianai-backend.onrender.com`

3. **构建优化**
   - Nuxt 3 会自动优化构建
   - 确保 `package.json` 中的依赖正确

### 故障排除

如果遇到问题：

1. **检查 DNS 解析**
   ```bash
   nslookup jubianai.cn
   ```

2. **检查 Vercel 部署日志**
   - 在 Vercel Dashboard → Deployments → 查看构建日志

3. **清除缓存**
   - 在 Vercel 中重新部署
   - 清除浏览器缓存

4. **检查环境变量**
   - 确保 `BACKEND_URL` 已正确配置

## 快速部署命令

如果使用 Vercel CLI：

```bash
cd frontend-nuxt
npm install -g vercel
vercel --prod
```

然后在 Vercel Dashboard 中添加自定义域名。

