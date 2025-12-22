# 部署指南

本文档介绍如何将项目部署到各种平台。

## 📋 部署前准备

1. **环境变量配置**：确保所有必要的环境变量已配置
2. **依赖安装**：确保 `requirements.txt` 包含所有依赖
3. **数据库设置**：如需要，配置 PostgreSQL 数据库

## 🚀 部署平台

### Vercel

#### 快速部署

1. 连接 GitHub 仓库到 Vercel
2. 配置环境变量：
   - `VOLCENGINE_ACCESS_KEY_ID`
   - `VOLCENGINE_SECRET_ACCESS_KEY`
   - `JIMENG_API_ENDPOINT`
   - `POSTGRES_URL`（如需要）
3. 部署会自动开始

#### 配置文件

项目已包含 `vercel.json` 配置：
- API 路由转发
- 静态文件服务
- CORS 配置

### Railway

#### 部署步骤

1. 在 Railway 创建新项目
2. 连接 GitHub 仓库
3. 配置环境变量
4. 设置启动命令：
   ```bash
   python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT
   ```

#### 配置文件

项目包含 `railway.json` 和 `Procfile`。

### Render

#### 部署步骤

1. 在 Render 创建 Web Service
2. 连接 GitHub 仓库
3. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT`
4. 设置环境变量

#### 配置文件

项目包含 `render.yaml` 配置文件。

### Streamlit Cloud

#### 部署步骤

1. 在 [Streamlit Cloud](https://streamlit.io/cloud) 创建应用
2. 连接 GitHub 仓库
3. 设置主文件路径：`jubianai/frontend/app.py`
4. 配置环境变量（在 Streamlit Cloud Dashboard）

## 🔧 环境变量清单

部署时需要配置以下环境变量：

```env
# 即梦 AI API
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com

# 服务器
HOST=0.0.0.0
PORT=8000

# 数据库（可选）
POSTGRES_URL=your_postgres_url
```

## 📝 注意事项

1. **敏感信息**：不要将敏感信息提交到代码仓库
2. **环境变量**：在部署平台设置环境变量，不要硬编码
3. **数据库**：如果使用 PostgreSQL，确保连接字符串正确
4. **端口**：某些平台（如 Railway、Render）使用动态端口，使用 `$PORT` 环境变量

## 🔍 故障排查

### 常见问题

1. **API 调用失败**：检查环境变量是否正确配置
2. **数据库连接失败**：检查 `POSTGRES_URL` 是否正确
3. **静态文件 404**：检查 `vercel.json` 配置

### 日志查看

- Vercel: Dashboard → Deployments → 查看日志
- Railway: Dashboard → 查看日志
- Render: Dashboard → Logs

