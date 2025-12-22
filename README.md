# 剧变时代 - AI 视频生成平台

一个基于即梦 AI 的视频生成平台，支持 RAG 增强提示词、首尾帧控制等功能。

## ✨ 功能特性

- 🎬 **视频生成**：基于即梦 AI 视频生成 3.0 720P
- 🖼️ **首尾帧控制**：支持上传首帧和尾帧图片，精确控制视频起止画面
- 🧠 **RAG 增强**：自动检索相似视频帧，增强生成提示词
- 🎨 **Streamlit 前端**：友好的 Web 界面
- 🔐 **安全认证**：火山引擎 AK/SK 签名认证

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
3. **调整参数**：设置视频尺寸、时长、帧率等
4. **生成视频**：点击"生成视频"按钮

### RAG 增强提示词

系统会自动：
1. 根据提示词检索相似视频帧
2. 分析帧的特征和风格
3. 增强原始提示词，提高生成质量

## 🔧 API 集成

### 即梦 AI API

本项目集成了即梦 AI 视频生成 3.0 720P API，支持：

- ✅ 图生视频-首帧接口
- ✅ 图生视频-首尾帧接口
- ✅ 火山引擎 AK/SK 签名认证
- ✅ HMAC-SHA256 签名算法

**官方文档**：
- [图生视频-首帧接口](https://www.volcengine.com/docs/85621/1785204?lang=zh)
- [图生视频-首尾帧接口](https://www.volcengine.com/docs/85621/1791184?lang=zh)

### API 请求格式

```json
{
  "req_key": "video_generation_720p",
  "prompt": "视频描述",
  "width": 1024,
  "height": 576,
  "duration": 5,
  "fps": 24,
  "first_frame": "base64_encoded_image",
  "last_frame": "base64_encoded_image",
  "negative_prompt": "负面提示词（可选）",
  "seed": 12345
}
```

## 📁 项目结构

```
AIGC-jubianage/
├── jubianai/              # 主应用
│   ├── backend/          # 后端 API
│   │   ├── api.py        # FastAPI 应用
│   │   ├── volcengine_auth.py  # 火山引擎认证
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
- 使用 HMAC-SHA256 签名算法
- 自动生成签名并添加到请求头
- 支持标准签名和简化签名（备用）

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
    "width": 1024,
    "height": 576,
    "duration": 5,
    "fps": 24
  }'
```

## 📚 相关文档

- [RAG 系统文档](./doubao-rag/README.md) - 视频 RAG 系统使用指南
- [数据库设置](./jubianai/DATABASE_SETUP.md) - PostgreSQL 数据库配置
- [部署指南](./DEPLOYMENT.md) - 部署到 Vercel、Railway、Render 等平台

## 🛠️ 开发

### 代码结构

- **后端**：FastAPI + 火山引擎认证
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
