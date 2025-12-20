# FastAPI 后端部署指南

## 部署方案

FastAPI 后端可以部署到多个平台，推荐以下方案：

## 方案一：Vercel Serverless Functions（推荐，与主页面同平台）

### 优点
- ✅ 与主页面在同一平台，管理方便
- ✅ 自动 HTTPS 和 CDN
- ✅ 按需计费，成本低
- ✅ 部署简单

### 步骤

1. **准备部署文件**
   - 已创建 `jubianai/api/index.py` 作为 Vercel 入口
   - `vercel.json` 已配置

2. **在 Vercel 中创建新项目**
   ```bash
   cd jubianai
   vercel
   ```
   
   或者：
   - 在 Vercel 网页中创建新项目
   - 连接 GitHub 仓库：`ZhehuanUnique/AIGC-jubianage`
   - Root Directory: `jubianai`
   - Framework Preset: Other

3. **配置环境变量**
   在 Vercel 项目设置中添加：
   - `API_KEY`: 你的 API Key（如果需要）
   - `SEEDANCE_API_ENDPOINT`: Seedance API 地址
   - `ENV`: `production`
   - `ALLOWED_ORIGINS`: `https://jubianai.cn,https://www.jubianai.cn,https://jubianai.streamlit.app`

4. **获取部署地址**
   - Vercel 会提供地址，例如：`https://jubianai-api.vercel.app`
   - 或者使用自定义域名

5. **更新 Streamlit 配置**
   在 Streamlit Cloud 的环境变量中添加：
   - `BACKEND_URL`: `https://jubianai-api.vercel.app`（你的 Vercel API 地址）
   - `ENV`: `production`

## 方案二：Railway（简单易用）

### 步骤

1. **访问 Railway**
   - https://railway.app
   - 使用 GitHub 登录

2. **创建新项目**
   - 从 GitHub 导入 `AIGC-jubianage` 仓库
   - 选择 "Deploy from GitHub repo"

3. **配置服务**
   - Root Directory: `jubianai`
   - Start Command: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
   - 环境变量：
     - `API_KEY`
     - `SEEDANCE_API_ENDPOINT`
     - `ENV`: `production`
     - `ALLOWED_ORIGINS`: `https://jubianai.cn,https://jubianai.streamlit.app`

4. **获取地址**
   - Railway 会提供地址，例如：`https://jubianai-api.up.railway.app`

5. **更新 Streamlit 配置**
   - 在 Streamlit Cloud 中添加 `BACKEND_URL`

## 方案三：Render（免费方案）

### 步骤

1. **访问 Render**
   - https://render.com
   - 使用 GitHub 登录

2. **创建 Web Service**
   - 连接 GitHub 仓库
   - Root Directory: `jubianai`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
   - 环境变量：同上

3. **获取地址**
   - Render 会提供地址，例如：`https://jubianai-api.onrender.com`

## 推荐配置

### 环境变量清单

**后端（FastAPI）**：
- `API_KEY`: 你的 API Key
- `SEEDANCE_API_ENDPOINT`: Seedance API 地址
- `ENV`: `production`
- `ALLOWED_ORIGINS`: `https://jubianai.cn,https://www.jubianai.cn,https://jubianai.streamlit.app`

**前端（Streamlit）**：
- `BACKEND_URL`: 后端 API 地址（部署后获取）
- `ENV`: `production`

## 部署后验证

1. **测试 API 健康检查**
   ```bash
   curl https://your-api-url.vercel.app/health
   ```

2. **测试 API 文档**
   - 访问：`https://your-api-url.vercel.app/docs`
   - 应该能看到 FastAPI 自动生成的文档

3. **在 Streamlit 中测试**
   - 打开 Streamlit 应用
   - 在侧边栏输入后端 API 地址
   - 测试视频生成功能

## 注意事项

1. **CORS 配置**：确保 `ALLOWED_ORIGINS` 包含 Streamlit 应用地址
2. **API Key 安全**：使用环境变量，不要硬编码
3. **HTTPS**：确保所有服务都使用 HTTPS

## 快速开始（Vercel）

```bash
# 1. 进入 jubianai 目录
cd jubianai

# 2. 安装 Vercel CLI（如果还没有）
npm i -g vercel

# 3. 登录 Vercel
vercel login

# 4. 部署
vercel

# 5. 配置环境变量（在 Vercel 网页中）
# 6. 获取部署地址
# 7. 在 Streamlit Cloud 中配置 BACKEND_URL
```

