# 剧变时代 - AI 视频生成平台

一个基于即梦 AI 的视频生成平台，支持 RAG 增强提示词、首尾帧控制等功能。

## ✨ 功能特性

- 🎬 **视频生成**：基于即梦 AI 视频生成 3.0 720P
- 🖼️ **首尾帧控制**：支持上传首帧和尾帧图片，精确控制视频起止画面
- 🧠 **RAG 增强**：自动检索相似视频帧，增强生成提示词
- 🎨 **Streamlit 前端**：友好的 Web 界面
- 🔐 **安全认证**：火山引擎 AK/SK 签名认证
- 📦 **资产管理**：支持图片资产上传、分类和管理

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- PostgreSQL（可选，用于数据存储）
- FFmpeg（用于视频处理）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```env
# 即梦 AI (火山引擎) API 配置
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置（可选）
POSTGRES_URL=your_postgres_url_here
```

### 4. 启动服务

#### 后端 API 服务

```bash
python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port 8000
```

#### Streamlit 前端

```bash
streamlit run jubianai/frontend/app.py
```

#### RAG 服务（可选）

```bash
python -m uvicorn doubao-rag.backend.api:app --host 0.0.0.0 --port 8001
```

## 📖 使用指南

### 视频生成

1. **输入提示词**：描述想要生成的视频内容
2. **上传首尾帧**（可选）：
   - 上传首帧图片控制视频起始画面
   - 上传尾帧图片控制视频结束画面
3. **调整参数**：设置视频时长（5s/10s）
4. **生成视频**：点击"生成视频"按钮

### RAG 增强提示词

系统会自动：
1. 根据提示词检索相似视频帧
2. 分析帧的特征和风格
3. 增强原始提示词，提高生成质量

### 资产管理

1. **上传资产**：准备图片文件，文件名格式：`人物名-视图类型.扩展名`
   - 例如：`小明-正视图.jpg`、`小美-侧视图.png`
2. **自动分类**：系统会自动提取人物名称和视图类型
3. **查看资产**：在"资产管理"标签页按人物分组查看

## 🔧 API 集成

### 即梦 AI API

本项目集成了即梦 AI 视频生成 3.0 720P API，支持：

- ✅ 图生视频-首帧接口
- ✅ 图生视频-首尾帧接口
- ✅ 火山引擎 AK/SK 签名认证
- ✅ HMAC-SHA256 签名算法（使用官方 SDK）

**官方文档**：
- [图生视频-首帧接口](https://www.volcengine.com/docs/85621/1785204?lang=zh)
- [图生视频-首尾帧接口](https://www.volcengine.com/docs/85621/1791184?lang=zh)

### API 请求格式

```json
{
  "req_key": "jimeng_i2v_first_v30",
  "image_urls": ["https://xxx"],
  "prompt": "视频描述",
  "frames": 121,
  "seed": -1
}
```

## 📁 项目结构

```
AIGC-jubianage/
├── jubianai/              # 主应用
│   ├── backend/          # 后端 API
│   │   ├── api.py        # FastAPI 应用
│   │   ├── volcengine_auth.py  # 火山引擎认证
│   │   ├── volcengine_sdk_helper.py  # 官方 SDK 封装
│   │   └── models.py     # 数据模型
│   ├── frontend/         # Streamlit 前端
│   │   └── app.py       # Streamlit 应用
│   └── config.py         # 配置文件
├── doubao-rag/          # RAG 系统
│   ├── backend/         # RAG 后端
│   │   ├── rag_service.py
│   │   ├── video_processor.py
│   │   └── vector_db.py
│   └── README.md        # RAG 系统文档
├── api/                 # Vercel Serverless Functions
├── .streamlit/          # Streamlit 配置
│   ├── config.toml      # Streamlit 应用配置
│   └── secrets.toml.example  # 环境变量示例
├── index.html           # 主页
└── README.md            # 本文件
```

## 🔐 安全配置

### 环境变量

**⚠️ 重要**：敏感信息（如 AK/SK）必须通过环境变量配置，不要硬编码在代码中。

1. 创建 `.env` 文件（已添加到 `.gitignore`）
2. 参考 `jubianai/env.example` 配置模板
3. 在部署平台（Vercel、Railway 等）设置环境变量

### 认证方式

即梦 API 使用火山引擎的 AK/SK 签名认证：
- 使用官方 `volcengine` Python SDK
- 自动生成 HMAC-SHA256 签名
- 支持同步和异步调用

## 🚀 部署指南

### Streamlit Cloud 部署

#### 1. 配置应用

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击 "New app"
3. 连接 GitHub 仓库
4. 配置应用设置：
   - **Main file path**: `jubianai/frontend/app.py`
   - **Python version**: 3.11（推荐）

#### 2. 配置环境变量

在 Streamlit Cloud Dashboard 的 "Secrets" 部分添加：

```toml
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
BACKEND_URL=https://your-backend-url.com  # 后端服务地址
```

**⚠️ 重要**：
- `BACKEND_URL` 必须设置为实际的后端服务 URL
- 不能使用 `localhost` 或 `127.0.0.1`
- 如果后端部署在 Vercel: `https://your-app.vercel.app`
- 如果后端部署在 Railway: `https://your-app.railway.app`
- 如果后端部署在 Render: `https://your-app.onrender.com`

#### 3. 后端服务配置

**选项 A：使用 Vercel Serverless Functions（推荐）**
- 后端 API 通过 Vercel 的 Serverless Functions 提供
- 在 Streamlit Cloud 中设置 `BACKEND_URL` 为 Vercel API 地址

**选项 B：部署到其他平台**
- 将后端 API 部署到 Railway、Render 或其他平台
- 在 Streamlit Cloud 的 Secrets 中设置 `BACKEND_URL`

#### 4. 常见问题

**"Failed to fetch" 错误**：
- 检查 `BACKEND_URL` 是否正确
- 确保后端服务已部署并运行
- 检查后端服务的 CORS 配置

**"即梦 API 认证信息未配置" 错误**：
- 在 Streamlit Cloud Dashboard 的 Secrets 中添加 `VOLCENGINE_ACCESS_KEY_ID` 和 `VOLCENGINE_SECRET_ACCESS_KEY`
- 确保密钥格式正确（不要有多余的空格或引号）

### Vercel 部署

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

### Railway 部署

#### 部署步骤

1. 在 Railway 创建新项目
2. 连接 GitHub 仓库
3. 配置环境变量
4. 设置启动命令：
   ```bash
   python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT
   ```

### Render 部署

#### 部署步骤

1. 在 Render 创建 Web Service
2. 连接 GitHub 仓库
3. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT`
4. 设置环境变量

## 💾 数据库设置

### PostgreSQL 数据库

#### 为什么选择 PostgreSQL？

1. **功能更强大**：
   - 支持 JSON/JSONB 数据类型（非常适合存储元数据）
   - 支持全文搜索
   - 支持数组、范围等高级数据类型
   - 更好的并发控制

2. **更适合现代应用**：
   - 更好的 JSON 支持（适合 API 开发）
   - 更强大的查询功能
   - 更好的扩展性

3. **Vercel 集成**：
   - Vercel Postgres 基于 PostgreSQL
   - 无缝集成，自动配置连接
   - 免费层提供 256MB 存储

### 在 Vercel 中创建 Postgres 数据库

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 进入你的项目
3. 点击 "Storage" 标签
4. 点击 "Create Database"
5. 选择 "Postgres"
6. 选择免费计划（Hobby）
7. 创建数据库

Vercel 会自动创建 `POSTGRES_URL` 环境变量。

### 初始化数据库表

有两种方式初始化数据库：

#### 方式 1：通过 API 自动初始化（推荐）

应用启动时会自动创建表（如果不存在）。

#### 方式 2：手动运行初始化脚本

```bash
cd jubianai
python init_db.py
```

### 数据库表结构

#### assets 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| filename | VARCHAR(255) | 原始文件名 |
| character_name | VARCHAR(100) | 人物名称 |
| view_type | VARCHAR(50) | 视图类型（正视图、侧视图等） |
| file_path | VARCHAR(500) | 文件路径或 URL |
| file_url | VARCHAR(500) | 完整文件 URL（如果使用云存储） |
| upload_time | TIMESTAMP | 上传时间 |
| file_size | INTEGER | 文件大小（字节） |
| file_type | VARCHAR(20) | 文件类型（image, video 等） |
| metadata | TEXT | JSON 格式的额外元数据 |

### 本地开发

#### 安装 PostgreSQL

**Windows:**
1. 下载 [PostgreSQL for Windows](https://www.postgresql.org/download/windows/)
2. 安装并记住密码

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

#### 创建本地数据库

```bash
# 登录 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE jubianai;

# 退出
\q
```

#### 配置本地环境变量

创建 `.env` 文件：

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/jubianai
```

### 文件存储说明

⚠️ **重要**：在 Vercel Serverless 环境中，文件系统是只读的。

**当前方案**：
- **元数据**：存储在 PostgreSQL 数据库中 ✅
- **文件本身**：需要上传到云存储服务

**推荐的文件存储方案**：

1. **Vercel Blob Storage**（推荐）
   - 与 Vercel 无缝集成
   - 免费层：256MB 存储
   - 简单易用

2. **AWS S3**
   - 功能强大
   - 按使用量付费
   - 需要额外配置

3. **Cloudinary**
   - 专为图片/视频优化
   - 提供图片处理功能
   - 有免费层

## 📦 RAG 数据库导出

RAG 数据库是**完全独立**的，与 jubianai 项目的 PostgreSQL 数据库分开存储：

- **RAG 数据库**：Chroma 向量数据库（`doubao-rag/vector_db/`）
- **jubianai 数据库**：PostgreSQL（用于资产元数据）

两者互不干扰，可以单独使用。

### 导出数据库

#### 使用导出脚本（推荐）

```bash
cd doubao-rag/backend
python db_export.py ./rag_export
```

这会创建一个包含以下内容的导出目录：
- `vector_db/` - 向量数据库
- `frames/` - 关键帧图片
- `rag_config.json` - 配置信息
- `database_stats.json` - 统计信息
- `rag_package/` - 独立使用的代码包

#### 在其他地方使用导出的数据库

1. **复制文件**：将导出的目录复制到新位置
2. **使用独立包**：导出的 `rag_package/` 目录包含所有必要的代码
3. **配置路径**：使用环境变量或配置文件指定数据库路径

详细使用方法请参考 [doubao-rag/README.md](./doubao-rag/README.md)。

## 🧪 测试

### 本地测试

1. 启动后端服务：
   ```bash
   python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port 8000
   ```

2. 打开测试页面：
   ```bash
   python -m http.server 8888
   # 访问 http://localhost:8888/test_jimeng_api.html
   ```

### API 测试

```bash
curl -X POST http://localhost:8000/api/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只可爱的小猫在花园里玩耍",
    "duration": 5,
    "fps": 24
  }'
```

## 🛠️ 开发

### 代码结构

- **后端**：FastAPI + 火山引擎认证（官方 SDK）
- **前端**：Streamlit
- **RAG**：LangGraph + Chroma + CLIP

### 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [即梦 AI 官方文档](https://www.volcengine.com/docs/85621?lang=zh)
- [Streamlit 文档](https://docs.streamlit.io/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [RAG 系统文档](./doubao-rag/README.md) - 视频 RAG 系统使用指南
- [Streamlit Cloud 应用](https://jubianai.streamlit.app/)
