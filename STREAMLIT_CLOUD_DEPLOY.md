# Streamlit Cloud 部署指南

## 📋 部署前准备

### 1. 确保文件结构正确

Streamlit Cloud 需要：
- 主应用文件：`jubianai/frontend/app.py`
- 依赖文件：根目录 `requirements.txt` 或 `jubianai/requirements.txt`
- 配置文件：`.streamlit/config.toml`（已创建）

**已完成的配置**：
- ✅ 创建了 `.streamlit/config.toml` 配置文件
- ✅ 创建了根目录 `requirements.txt`（Streamlit 前端依赖）
- ✅ 创建了 `.streamlit/secrets.toml.example` 示例文件

### 2. 在 Streamlit Cloud 配置

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击 "New app"
3. 连接 GitHub 仓库
4. 配置应用设置：
   - **Main file path**: `jubianai/frontend/app.py`
   - **Python version**: 3.11（推荐）

### 3. 配置环境变量

在 Streamlit Cloud Dashboard 的 "Secrets" 部分添加以下环境变量：

```toml
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
BACKEND_URL=http://localhost:8000  # 如果后端也在 Streamlit Cloud，需要调整
```

### 4. 后端服务配置

**选项 A：后端也在 Streamlit Cloud（不推荐）**
- Streamlit Cloud 主要用于前端，不适合运行后端 API 服务

**选项 B：后端部署到其他平台（推荐）**
- 将后端 API 部署到 Railway、Render 或其他平台
- 在 Streamlit Cloud 的 Secrets 中设置 `BACKEND_URL` 为后端服务的 URL

**选项 C：使用 Vercel Serverless Functions**
- 后端 API 可以通过 Vercel 的 Serverless Functions 提供
- 在 Streamlit Cloud 中设置 `BACKEND_URL` 为 Vercel API 地址

## 🔧 环境变量说明

### 必需的环境变量

- `VOLCENGINE_ACCESS_KEY_ID`: 火山引擎 Access Key ID（必需）
- `VOLCENGINE_SECRET_ACCESS_KEY`: 火山引擎 Secret Access Key（必需）
- `JIMENG_API_ENDPOINT`: 即梦 API 端点（默认：`https://visual.volcengineapi.com`）

### 重要的环境变量

- `BACKEND_URL`: 后端 API 地址（**必需**，Streamlit Cloud 部署时必须设置为实际的后端 URL）
  - 如果后端部署在 Railway: `https://your-app.railway.app`
  - 如果后端部署在 Render: `https://your-app.onrender.com`
  - 如果后端部署在 Vercel: `https://your-app.vercel.app/api`
  - **不能使用 `localhost` 或 `127.0.0.1`**

### 可选的环境变量

- `POSTGRES_URL`: 数据库连接（如果需要）

## 📝 注意事项

1. **后端服务**：Streamlit Cloud 只运行前端，后端需要单独部署
2. **环境变量**：敏感信息（AK/SK）必须在 Streamlit Cloud Dashboard 的 Secrets 中配置
3. **依赖安装**：确保 `jubianai/requirements.txt` 包含所有必需的依赖
4. **网络连接**：确保 Streamlit Cloud 可以访问后端 API 和即梦 API

## 🐛 调试技巧

1. **查看日志**：在 Streamlit Cloud Dashboard 查看应用日志
2. **测试连接**：在应用中测试后端 API 连接
3. **检查环境变量**：确保所有环境变量都已正确配置
4. **检查依赖**：确保所有 Python 包都能正常安装
5. **检查后端 URL**：确保 `BACKEND_URL` 指向正确且可访问的后端服务
6. **测试后端健康检查**：访问 `{BACKEND_URL}/health` 确认后端服务正常

## ⚠️ 常见问题

### 1. "Failed to fetch" 错误

**原因**：Streamlit Cloud 无法连接到后端服务

**解决方案**：
- 检查 `BACKEND_URL` 是否正确
- 确保后端服务已部署并运行
- 检查后端服务的 CORS 配置
- 测试后端健康检查端点

### 2. "即梦 API 认证信息未配置" 错误

**原因**：环境变量未正确配置

**解决方案**：
- 在 Streamlit Cloud Dashboard 的 Secrets 中添加 `VOLCENGINE_ACCESS_KEY_ID` 和 `VOLCENGINE_SECRET_ACCESS_KEY`
- 确保密钥格式正确（不要有多余的空格或引号）

### 3. 依赖安装失败

**原因**：某些依赖包在 Streamlit Cloud 上无法安装

**解决方案**：
- 检查 `requirements.txt` 中的依赖版本
- 移除不必要的依赖（如 RAG 相关依赖，如果不需要）
- 确保所有依赖都支持 Streamlit Cloud 的环境

## 🔗 相关链接

- Streamlit Cloud 文档：https://docs.streamlit.io/streamlit-cloud
- 应用地址：https://jubianai.streamlit.app/

