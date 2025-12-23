# Render 后端部署指南

## 📋 部署前准备

1. **GitHub 仓库**：确保代码已推送到 GitHub
2. **Render 账号**：注册 [Render](https://render.com/) 账号
3. **环境变量**：准备好即梦 AI 的 AK/SK

## 🚀 部署步骤

### 1. 创建 Web Service

1. 登录 [Render Dashboard](https://dashboard.render.com/)
2. 点击 "New +" → "Web Service"
3. 连接 GitHub 仓库：`ZhehuanUnique/AIGC-jubianage`
4. 配置服务设置：
   - **Name**: `jubianai-backend`（或你喜欢的名称）
   - **Region**: 选择离你最近的区域（如 `Singapore`）
   - **Branch**: `main`
   - **Root Directory**: 留空（使用根目录）
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r jubianai/requirements.txt`
   - **Start Command**: `python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`（免费计划）

### 2. 配置环境变量

在 Render Dashboard 的 "Environment" 部分添加以下环境变量：

```env
# 即梦 AI (火山引擎) API 配置（必需）
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com

# 服务器配置（可选，Render 会自动设置 PORT）
HOST=0.0.0.0
PORT=10000

# 数据库配置（可选，如果需要数据库功能）
# POSTGRES_URL=your_postgres_url_here
```

### 3. 部署

1. 点击 "Create Web Service"
2. Render 会自动开始构建和部署
3. 等待部署完成（通常需要 2-5 分钟）

### 4. 获取后端 URL

部署完成后，Render 会提供一个 URL，格式类似：
```
https://jubianai-backend.onrender.com
```

**⚠️ 重要**：免费计划的 Render 服务在 15 分钟无活动后会进入休眠状态，首次访问需要几秒钟唤醒。

## 🔧 配置 Streamlit Cloud

部署完成后，在 Streamlit Cloud 的 Secrets 中配置：

```toml
BACKEND_URL = "https://jubianai-backend.onrender.com"
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
```

## ✅ 验证部署

### 1. 健康检查

访问：
```
https://jubianai-backend.onrender.com/health
```

应该返回：
```json
{"status": "healthy"}
```

### 2. API 文档

访问：
```
https://jubianai-backend.onrender.com/docs
```

应该看到 FastAPI 自动生成的 API 文档。

### 3. 测试视频生成

```bash
curl -X POST https://jubianai-backend.onrender.com/api/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只可爱的小猫在花园里玩耍",
    "duration": 5,
    "fps": 24
  }'
```

## 🐛 常见问题

### 1. 部署失败

**原因**：依赖安装失败或构建超时

**解决方案**：
- 检查 `jubianai/requirements.txt` 中的依赖是否正确
- 确保没有包含 RAG 相关的大依赖（已从 requirements.txt 中移除）
- 查看 Render 的构建日志

### 2. 服务休眠

**原因**：免费计划的服务在 15 分钟无活动后会休眠

**解决方案**：
- 首次访问需要等待几秒钟唤醒
- 考虑使用付费计划（始终在线）
- 或使用外部监控服务定期 ping 健康检查端点

### 3. 环境变量未生效

**原因**：环境变量配置错误

**解决方案**：
- 检查 Render Dashboard 中的环境变量配置
- 确保变量名和值都正确
- 重新部署服务

### 4. CORS 错误

**原因**：前端无法访问后端 API

**解决方案**：
- 检查后端 API 的 CORS 配置（已在 `jubianai/backend/api.py` 中配置为允许所有来源）
- 确保 `BACKEND_URL` 配置正确

## 📝 注意事项

1. **免费计划限制**：
   - 服务会在 15 分钟无活动后休眠
   - 首次访问需要几秒钟唤醒
   - 每月有使用时间限制

2. **环境变量**：
   - 敏感信息（AK/SK）必须在 Render Dashboard 中配置
   - 不要将敏感信息提交到代码仓库

3. **依赖管理**：
   - `jubianai/requirements.txt` 只包含后端必需的依赖
   - RAG 相关依赖已移除（不需要在 Render 后端运行）

4. **数据库**（可选）：
   - 如果需要数据库功能，可以在 Render 创建 PostgreSQL 数据库
   - 然后在环境变量中配置 `POSTGRES_URL`

## 🔗 相关链接

- [Render 文档](https://render.com/docs)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [即梦 AI 官方文档](https://www.volcengine.com/docs/85621?lang=zh)


