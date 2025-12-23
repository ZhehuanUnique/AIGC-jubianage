# Vercel Pro 方案配置指南

## 🎉 Vercel Pro 优势

使用 Vercel Pro 方案，你享有以下优势：

### 资源限制提升
- ✅ **更大的构建时间限制**：Pro 方案有更长的构建时间
- ✅ **更大的函数大小限制**：支持更大的 Serverless Functions
- ✅ **更多的带宽**：更高的流量限制
- ✅ **更好的性能**：更快的构建和部署速度
- ✅ **团队协作**：支持团队功能

## 📋 在 Vercel Pro 上配置项目

### 1. 项目设置

1. **登录 Vercel Dashboard**
   - 访问 https://vercel.com/dashboard
   - 确保你使用的是 Pro 账户

2. **导入项目**（如果还没导入）
   - 点击 "Add New..." → "Project"
   - 选择 `ZhehuanUnique/AIGC-jubianage`
   - 点击 "Import"

3. **配置 Root Directory** ⚠️ **非常重要**
   - 在 "Configure Project" 页面
   - 找到 "Root Directory"
   - 设置为：`frontend-nuxt`
   - 点击 "Save"

### 2. 环境变量配置

在 Vercel Dashboard 中配置环境变量：

1. **进入项目设置**
   - 在项目页面，点击顶部菜单 **"Settings"**
   - 选择 **"Environment Variables"**

2. **添加环境变量**

#### 前端环境变量（可选）

如果需要自定义后端地址：

- **Key**: `BACKEND_URL`
- **Value**: `https://jubianai-backend.onrender.com`
- **Environment**: Production, Preview, Development（全选）

#### 后端环境变量（如果后端也部署在 Vercel）

如果后端也部署在 Vercel（使用 Serverless Functions），需要添加：

- **Supabase 数据库**
  - **Key**: `SUPABASE_DB_URL`
  - **Value**: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`
  - **Environment**: Production, Preview, Development（全选）

- **对象存储配置**（二选一）

  **阿里云 OSS:**
  - `STORAGE_TYPE` = `aliyun_oss`
  - `ALIYUN_OSS_ACCESS_KEY_ID` = `your_access_key_id`
  - `ALIYUN_OSS_ACCESS_KEY_SECRET` = `your_access_key_secret`
  - `ALIYUN_OSS_BUCKET_NAME` = `your_bucket_name`
  - `ALIYUN_OSS_ENDPOINT` = `oss-cn-beijing.aliyuncs.com`
  - `ALIYUN_OSS_BUCKET_DOMAIN` = `your-cdn-domain.com`（可选）

  **AWS S3:**
  - `STORAGE_TYPE` = `s3`
  - `AWS_ACCESS_KEY_ID` = `your_access_key_id`
  - `AWS_SECRET_ACCESS_KEY` = `your_secret_access_key`
  - `AWS_S3_BUCKET_NAME` = `your_bucket_name`
  - `AWS_S3_REGION` = `us-east-1`

- **即梦 AI API 配置**（如果后端在 Vercel）
  - `VOLCENGINE_ACCESS_KEY_ID` = `your_access_key_id`
  - `VOLCENGINE_SECRET_ACCESS_KEY` = `your_secret_access_key`
  - `JIMENG_API_ENDPOINT` = `https://visual.volcengineapi.com`

### 3. 部署配置

1. **框架预设**
   - Framework Preset: **Nuxt.js**（应该自动检测）
   - Build Command: `npm run build`（自动）
   - Output Directory: `.output/public`（自动）
   - Install Command: `npm install`（自动）

2. **部署**
   - 点击 "Deploy"
   - 等待构建完成

## 🔧 Vercel Pro 特定配置

### 使用 Vercel Serverless Functions（可选）

如果你想将后端 API 也部署到 Vercel：

1. **创建 API 路由**
   - 在 `frontend-nuxt/server/api/` 目录下创建 API 路由
   - 例如：`frontend-nuxt/server/api/video/generate.ts`

2. **配置函数**
   - Vercel Pro 支持更大的函数大小
   - 可以部署完整的 FastAPI 后端

### 自定义域名配置

1. **添加域名**
   - 在项目 Settings → Domains
   - 添加 `jubianai.cn`
   - 按照提示配置 DNS

2. **SSL 证书**
   - Vercel Pro 自动配置 SSL 证书
   - 通常几分钟内生效

## 📊 当前架构建议

### 推荐架构

```
前端：Vercel Pro（Nuxt 3）
  ↓ API 调用
后端：Render（FastAPI + Supabase）
  ↓ 数据库
数据库：Supabase PostgreSQL
  ↓ 对象存储
对象存储：阿里云 OSS / AWS S3
```

### 为什么这样配置？

1. **前端在 Vercel Pro**
   - ✅ 全球 CDN，访问速度快
   - ✅ 自动 HTTPS
   - ✅ 自动部署（GitHub 集成）

2. **后端在 Render**
   - ✅ 支持长时间运行的任务
   - ✅ 更好的 Python 环境支持
   - ✅ 适合视频生成等耗时操作

3. **数据库在 Supabase**
   - ✅ 免费额度充足
   - ✅ 易于管理
   - ✅ 自动备份

## 🚀 部署流程

### 1. 前端部署（Vercel Pro）

1. 推送代码到 GitHub
2. Vercel 自动检测并部署
3. 配置环境变量（如需要）
4. 配置自定义域名

### 2. 后端部署（Render）

1. 在 Render 中部署后端
2. 配置环境变量（Supabase、对象存储等）
3. 确保后端 URL 正确

### 3. 数据库初始化

1. 在 Supabase 中执行 `supabase_init.sql`
2. 验证表创建成功

## 🔍 验证部署

### 前端验证

1. 访问 Vercel 提供的 URL 或自定义域名
2. 检查页面是否正常加载
3. 测试视频生成功能

### 后端验证

1. 访问后端健康检查：`https://jubianai-backend.onrender.com/health`
2. 测试 API：`https://jubianai-backend.onrender.com/api/v1/video/history`

### 数据库验证

1. 在 Supabase Table Editor 中查看数据
2. 生成一个视频，检查是否保存到数据库

## 💡 Pro 方案优势总结

- ✅ **更大的构建时间**：适合复杂的 Nuxt 3 项目
- ✅ **更大的函数大小**：可以部署更多功能
- ✅ **更多带宽**：支持更多用户访问
- ✅ **更好的性能**：更快的构建和响应
- ✅ **团队功能**：支持团队协作

## 📝 注意事项

1. **环境变量安全**
   - 不要在代码中硬编码敏感信息
   - 使用 Vercel 环境变量管理

2. **构建优化**
   - Vercel Pro 有更长的构建时间，但仍建议优化构建
   - 使用 `.vercelignore` 排除不必要的文件

3. **监控和日志**
   - 使用 Vercel Analytics（Pro 功能）
   - 查看构建日志和函数日志

## 🆘 常见问题

### 问题 1: 构建失败

**解决**:
- 检查 Root Directory 是否设置为 `frontend-nuxt`
- 查看构建日志中的错误信息
- 确认 `package.json` 和依赖正确

### 问题 2: 环境变量未生效

**解决**:
- 确认环境变量已添加到正确的环境（Production/Preview/Development）
- 重新部署项目
- 检查环境变量名称是否正确

### 问题 3: API 请求失败

**解决**:
- 检查后端 URL 是否正确
- 确认后端已部署并运行
- 检查 CORS 配置

## 🎯 下一步

1. ✅ 配置 Vercel 环境变量（如需要）
2. ✅ 确保 Root Directory 设置为 `frontend-nuxt`
3. ✅ 配置自定义域名 `jubianai.cn`
4. ✅ 测试所有功能

你的 Vercel Pro 方案已经为项目提供了充足的资源，可以放心使用！

