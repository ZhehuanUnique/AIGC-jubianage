# 剧变时代 - AI 视频生成平台

一个基于即梦 AI 的视频生成平台，支持 RAG 增强提示词、首尾帧控制等功能。

## ✨ 功能特性

- 🎬 **视频生成**：基于即梦 AI 视频生成 3.0，支持 720P 和 1080P 分辨率
- 🖼️ **首尾帧控制**：支持上传首帧和尾帧图片，精确控制视频起止画面
- 🎨 **现代前端**：基于 Nuxt 3 + Vue 3 + TypeScript + Tailwind CSS
- 📱 **响应式设计**：支持桌面和移动设备
- 📊 **历史记录**：自动保存视频生成历史，支持筛选和搜索
- ⭐ **收藏和点赞**：支持收藏和点赞视频
- 🗑️ **删除功能**：支持删除不需要的视频
- 🚀 **视频增强**：
  - **超分辨率**：Real-ESRGAN / Waifu2x（1080P → 4K）
  - **帧率提升**：RIFE / FILM（24fps → 60fps）
  - **智能切换**：自动检测大运动并切换到 FILM
- 🧠 **RAG 增强**：自动检索相似视频帧，增强生成提示词（可选）
- 🔐 **安全认证**：火山引擎 AK/SK 签名认证
- 📦 **资产管理**：支持图片资产上传、分类和管理
- 💾 **数据库支持**：Supabase PostgreSQL，自动保存历史记录

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
cd jubianai
python -m uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

#### Nuxt 3 前端

```bash
cd frontend-nuxt
npm install
npm run dev
```

访问 `http://localhost:3001` 查看应用。

#### RAG 服务（可选）

```bash
python -m uvicorn doubao-rag.backend.api:app --host 0.0.0.0 --port 8001
```

## 📖 使用指南

### 视频生成

1. **输入提示词**：描述想要生成的视频内容
2. **选择分辨率**：720P 或 1080P
3. **选择时长**：5秒 或 10秒
4. **上传首尾帧**（可选）：
   - 上传首帧图片控制视频起始画面
   - 上传尾帧图片控制视频结束画面
5. **生成视频**：点击"生成视频"按钮
6. **查看历史**：在历史记录中查看生成的视频

### 视频增强

#### 提升分辨率
1. 在历史记录页面，鼠标悬停在视频上
2. 点击右下角的蓝色分辨率按钮
3. 选择 Real-ESRGAN 或 Waifu2x
4. 等待处理完成（通常需要几分钟）

#### 提升帧率
1. 在历史记录页面，鼠标悬停在视频上
2. 点击右下角的绿色帧率按钮
3. 选择 RIFE（快速）或 FILM（大运动）
4. 系统会自动检测大运动并切换到 FILM（如果启用）

### 历史记录管理

- **查看历史**：自动显示所有生成的视频
- **筛选功能**：按时间、状态、操作类型筛选
- **收藏视频**：点击五角星按钮收藏
- **点赞视频**：点击爱心按钮点赞
- **删除视频**：点击右上角红色删除按钮

### RAG 增强提示词（可选）

如果启用了 RAG 服务，系统会自动：
1. 根据提示词检索相似视频帧
2. 分析帧的特征和风格
3. 增强原始提示词，提高生成质量

### 资产管理

1. **上传资产**：准备图片文件，文件名格式：`人物名-视图类型.扩展名`
   - 例如：`小明-正视图.jpg`、`小美-侧视图.png`
2. **自动分类**：系统会自动提取人物名称和视图类型
3. **查看资产**：在"资产管理"页面按人物分组查看

## 🔧 API 集成

### 即梦 AI API

本项目集成了即梦 AI 视频生成 3.0 API，支持：

- ✅ **720P 视频生成**：
  - 图生视频-首帧接口：`jimeng_i2v_first_v30`
  - 图生视频-首尾帧接口：`i2v_first_tail_v30_jimeng`
- ✅ **1080P 视频生成**：
  - 图生视频-首帧接口：`jimeng_i2v_first_v30_1080`
  - 图生视频-首尾帧接口：`i2v_first_tail_v30_1080_jimeng`
- ✅ 火山引擎 AK/SK 签名认证
- ✅ HMAC-SHA256 签名算法（使用官方 SDK）

**官方文档**：
- [720P-首帧接口](https://www.volcengine.com/docs/85621/1785204?lang=zh)
- [720P-首尾帧接口](https://www.volcengine.com/docs/85621/1791184?lang=zh)
- [1080P-首帧接口](https://www.volcengine.com/docs/85621/1798092?lang=zh)
- [1080P-首尾帧接口](https://www.volcengine.com/docs/85621/1802721?lang=zh)

### API 请求格式

```json
{
  "prompt": "视频描述",
  "duration": 5,
  "fps": 24,
  "width": 1280,
  "height": 720,
  "resolution": "720p",
  "first_frame": "base64_image_data",
  "last_frame": "base64_image_data"
}
```

## 📁 项目结构

```
AIGC-jubianage/
├── jubianai/              # 后端服务
│   ├── backend/           # FastAPI 后端
│   │   ├── api.py         # 主 API 文件
│   │   ├── api_history.py # 历史记录 API
│   │   ├── video_processing.py  # 视频增强服务
│   │   ├── video_history.py     # 历史记录服务
│   │   └── ...
│   ├── frontend/         # Streamlit 前端（旧版，可选）
│   └── README.md          # 后端详细文档
├── frontend-nuxt/         # Nuxt 3 前端（当前使用）
│   ├── pages/             # 页面
│   ├── stores/            # Pinia 状态管理
│   ├── layouts/           # 布局
│   └── README.md          # 前端文档
├── doubao-rag/            # RAG 系统（可选）
│   └── README.md          # RAG 文档
└── README.md              # 本文件
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

### 前端部署（Vercel）

#### 1. 配置项目

1. **登录 Vercel Dashboard**
   - 访问 https://vercel.com/dashboard
   - 使用 GitHub 账号登录

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择 `ZhehuanUnique/AIGC-jubianage` 仓库
   - 点击 "Import"

3. **⚠️ 重要配置**
   - **Root Directory**: 设置为 `frontend-nuxt`（必须设置！）
   - **Framework Preset**: Nuxt.js（自动检测）
   - **Build Command**: `npm run build`（自动）
   - **Output Directory**: `.output/public`（自动）
   - **Install Command**: `npm install`（自动）

4. **环境变量**（可选）
   - Key: `BACKEND_URL`
   - Value: `https://jubianai-backend.onrender.com`

5. **部署**
   - 点击 "Deploy"
   - 等待构建完成（通常 2-5 分钟）

#### 2. 配置自定义域名（jubianai.cn）

1. **在 Vercel 中添加域名**
   - 项目设置 → **Settings** → **Domains**
   - 点击 **Add Domain**
   - 输入：`jubianai.cn`
   - 点击 **Add**

2. **配置 DNS 记录**
   - 在域名注册商（阿里云、腾讯云等）的 DNS 管理中
   - 添加 CNAME 记录：
     - **类型**: CNAME
     - **主机记录**: `@`（或留空）
     - **记录值**: `cname.vercel-dns.com`（Vercel 会显示具体值）
     - **TTL**: 3600

3. **等待 DNS 生效**
   - 通常 10-30 分钟生效
   - 最长可能需要 24-48 小时
   - 使用 `nslookup jubianai.cn` 检查 DNS 解析

4. **SSL 证书**
   - Vercel 会自动配置 SSL 证书
   - DNS 生效后几分钟内完成

#### 3. 验证部署

- 访问 `https://jubianai.cn` 应该显示应用
- 检查所有功能是否正常

### 后端部署（Render）

#### 1. 创建 Web Service

1. 登录 [Render Dashboard](https://dashboard.render.com/)
2. 点击 "New +" → "Web Service"
3. 连接 GitHub 仓库：`ZhehuanUnique/AIGC-jubianage`
4. 配置服务：
   - **Name**: `jubianai-backend`
   - **Region**: 选择最近的区域（如 `Singapore`）
   - **Branch**: `main`
   - **Root Directory**: 留空（使用根目录）
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r jubianai/requirements.txt`
   - **Start Command**: `python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

#### 2. 配置环境变量

在 Render Dashboard 的 "Environment" 部分添加：

```env
# 即梦 API（必需）
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com

# Supabase 数据库（可选，用于历史记录）
SUPABASE_DB_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# 对象存储（可选）
STORAGE_TYPE=aliyun_oss
ALIYUN_OSS_ACCESS_KEY_ID=your_key
ALIYUN_OSS_ACCESS_KEY_SECRET=your_secret
ALIYUN_OSS_BUCKET_NAME=your_bucket
ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
```

#### 3. 部署和验证

1. 点击 "Create Web Service"
2. 等待部署完成（通常 2-5 分钟）
3. 获取后端 URL：`https://jubianai-backend.onrender.com`
4. 验证健康检查：访问 `https://jubianai-backend.onrender.com/health`

**⚠️ 注意**：
- 免费计划的 Render 服务在 15 分钟无活动后会休眠
- 首次访问需要几秒钟唤醒
- 这是正常现象，不是错误

### 数据库配置（Supabase）

#### 1. 创建 Supabase 项目

1. 访问 https://supabase.com
2. 使用 GitHub 账号登录
3. 创建新项目：
   - **Name**: jubianai
   - **Database Password**: 设置强密码（**记住这个密码！**）
   - **Region**: 选择最近的区域

#### 2. 初始化数据库表

1. **打开 SQL Editor**
   - 在 Supabase Dashboard 中
   - 点击左侧菜单的 **"SQL Editor"**

2. **执行初始化脚本**
   - 打开项目中的 `jubianai/supabase_init.sql` 文件
   - 复制所有 SQL 代码
   - 粘贴到 Supabase SQL Editor 中
   - 点击 **"Run"** 执行

3. **验证表创建**
   - 在 **"Table Editor"** 中
   - 应该能看到以下表：
     - ✅ `users`
     - ✅ `video_generations`
     - ✅ `assets`（可选）
     - ✅ `knowledge_base`（可选）

#### 3. 获取连接字符串

1. **进入 Database 设置**
   - Settings → **Database**

2. **获取 Connection Pooling URL**（推荐）
   - 找到 **Connection Pooling** 部分
   - 选择 **Session mode**（推荐）或 **Transaction mode**
   - 复制连接字符串
   - 格式：`postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`

3. **配置到 Render**
   - 在 Render Dashboard 中
   - 添加环境变量：`SUPABASE_DB_URL`
   - 值：使用 Connection Pooling URL（端口 6543）

**⚠️ 重要**：
- 使用 Connection Pooling（端口 6543）而不是直接连接（端口 5432）
- Connection Pooling 使用 IPv4，避免 IPv6 连接问题
- 用户名格式：`postgres.[PROJECT-REF]`（不是 `postgres`）

#### 4. 对象存储配置（可选）

**阿里云 OSS：**

1. **创建 OSS Bucket**
   - 登录阿里云控制台
   - 进入对象存储 OSS
   - 创建 Bucket

2. **获取 AccessKey**
   - 进入 AccessKey 管理
   - 创建 AccessKey
   - 记录 AccessKey ID 和 Secret

3. **配置环境变量**
   ```env
   STORAGE_TYPE=aliyun_oss
   ALIYUN_OSS_ACCESS_KEY_ID=your_key
   ALIYUN_OSS_ACCESS_KEY_SECRET=your_secret
   ALIYUN_OSS_BUCKET_NAME=your_bucket
   ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
   ALIYUN_OSS_BUCKET_DOMAIN=your-cdn-domain.com  # 可选，CDN域名
   ```

### 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] Vercel 项目已创建，Root Directory 设置为 `frontend-nuxt`
- [ ] Render 后端服务已创建并配置环境变量
- [ ] Supabase 项目已创建，数据库表已初始化
- [ ] Connection Pooling URL 已配置到 Render
- [ ] 自定义域名 `jubianai.cn` 已配置（如需要）
- [ ] DNS 记录已配置并生效
- [ ] 所有功能测试通过

## 💾 数据库设置

### Supabase 数据库配置

#### 为什么选择 Supabase？

1. **免费额度充足**：500MB 数据库空间
2. **易于使用**：提供 Web 界面和 REST API
3. **连接池支持**：解决 IPv6 连接问题
4. **自动备份**：数据安全有保障

#### 初始化步骤

1. **创建 Supabase 项目**
   - 访问 https://supabase.com
   - 使用 GitHub 账号登录
   - 创建新项目，设置数据库密码

2. **执行初始化 SQL**
   - 在 Supabase Dashboard → SQL Editor
   - 打开 `jubianai/supabase_init.sql`
   - 复制所有 SQL 代码并执行

3. **获取连接字符串**
   - Settings → Database → Connection Pooling
   - 选择 **Session mode**（推荐）
   - 复制连接字符串（端口 6543）

4. **配置到 Render**
   - 在 Render Dashboard 中添加环境变量
   - Key: `SUPABASE_DB_URL`
   - Value: Connection Pooling URL

**⚠️ 重要**：
- 使用 Connection Pooling（端口 6543）避免 IPv6 问题
- 用户名格式：`postgres.[PROJECT-REF]`
- 主机名：`pooler.supabase.com`

#### 数据库表结构

**video_generations 表**（视频生成历史）：
- `id`: 主键
- `task_id`: 即梦 API 任务ID
- `prompt`: 提示词
- `duration`, `fps`, `width`, `height`: 视频参数
- `video_url`: 生成的视频URL
- `status`: 状态（pending/processing/completed/failed）
- `created_at`, `completed_at`: 时间戳
- `is_favorite`, `is_liked`: 用户操作标记

**users 表**（用户）：
- `id`: 主键
- `username`: 用户名
- `api_key`: API密钥
- `is_active`: 是否激活

详细表结构请参考 `jubianai/supabase_init.sql`。

### 对象存储配置

#### 阿里云 OSS（推荐）

1. **创建 OSS Bucket**
   - 登录阿里云控制台
   - 进入对象存储 OSS
   - 创建 Bucket（选择区域、读写权限等）

2. **获取 AccessKey**
   - 进入 AccessKey 管理
   - 创建 AccessKey
   - 记录 AccessKey ID 和 Secret

3. **配置环境变量**
   ```env
   STORAGE_TYPE=aliyun_oss
   ALIYUN_OSS_ACCESS_KEY_ID=your_key
   ALIYUN_OSS_ACCESS_KEY_SECRET=your_secret
   ALIYUN_OSS_BUCKET_NAME=your_bucket
   ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
   ALIYUN_OSS_BUCKET_DOMAIN=your-cdn-domain.com  # 可选
```

#### AWS S3（备选）

```env
STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET_NAME=your_bucket
AWS_S3_REGION=us-east-1
```

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

1. **启动后端服务**
   ```bash
   python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port 8000
   ```

2. **启动前端服务**
   ```bash
   cd frontend-nuxt
   npm install
   npm run dev
   ```
   访问 `http://localhost:3001`

3. **测试 API**
```bash
curl -X POST http://localhost:8000/api/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只可爱的小猫在花园里玩耍",
    "duration": 5,
       "fps": 24,
       "resolution": "720p"
  }'
```

### 功能测试清单

#### 视频生成功能
- [ ] 可以输入提示词
- [ ] 可以上传首帧和尾帧图片
- [ ] 可以切换分辨率（720P/1080P）
- [ ] 可以选择视频时长（5秒/10秒）
- [ ] 视频生成任务可以成功提交
- [ ] 任务状态可以正常更新

#### 历史记录功能
- [ ] 历史记录页面可以正常加载
- [ ] 新生成的视频自动出现在历史记录中
- [ ] 视频状态实时更新（等待中 → 生成中 → 已完成）
- [ ] 可以播放已完成的视频
- [ ] 可以收藏和点赞视频
- [ ] 可以删除视频

#### 视频增强功能
- [ ] 分辨率提升按钮可以正常显示
- [ ] 可以选择超分辨率方法（Real-ESRGAN/Waifu2x）
- [ ] 帧率提升按钮可以正常显示
- [ ] 可以选择插帧方法（RIFE/FILM）
- [ ] 处理完成后视频可以正常显示

### 清除浏览器缓存

测试前建议清除浏览器缓存，确保加载最新代码：
- **Windows/Linux**: `Ctrl + Shift + R` 或 `Ctrl + F5`
- **Mac**: `Cmd + Shift + R`

## 🛠️ 开发

### 代码结构

- **后端**：FastAPI + 火山引擎认证（官方 SDK）
- **前端**：Nuxt 3 + Vue 3 + TypeScript + Tailwind CSS
- **RAG**：LangGraph + Chroma + CLIP（可选）

### 项目结构

```
AIGC-jubianage/
├── jubianai/              # 后端服务
│   ├── backend/           # FastAPI 后端
│   │   ├── api.py         # 主 API 文件
│   │   ├── api_history.py # 历史记录 API
│   │   ├── video_processing.py  # 视频增强服务
│   │   └── ...
│   ├── frontend/          # Streamlit 前端（旧版）
│   └── README.md          # 后端详细文档
├── frontend-nuxt/         # Nuxt 3 前端（当前使用）
│   ├── pages/             # 页面
│   ├── stores/            # Pinia 状态管理
│   ├── layouts/           # 布局
│   └── README.md          # 前端文档
├── doubao-rag/            # RAG 系统（可选）
│   └── README.md          # RAG 文档
└── README.md              # 本文件
```

### 贡献

欢迎提交 Issue 和 Pull Request！

## 🐛 故障排除

### 常见问题

#### 1. 视频生成失败 - Access Denied (50400)

**原因**：API 密钥未配置或配置错误

**解决**：
1. 检查 Render 环境变量 `VOLCENGINE_ACCESS_KEY_ID` 和 `VOLCENGINE_SECRET_ACCESS_KEY`
2. 确认密钥格式正确（无多余空格）
3. 确认密钥有权限访问即梦 API
4. 重启 Render 服务

详细排查请参考 `jubianai/README.md` 中的"API 配置"章节。

#### 2. 数据库连接失败 - Network is unreachable (IPv6)

**原因**：Supabase 直接连接使用 IPv6，Render 无法访问

**解决**：
1. 使用 Supabase Connection Pooling（端口 6543）
2. 在 Supabase Dashboard → Settings → Database → Connection Pooling
3. 复制 Session mode 连接字符串
4. 更新 Render 环境变量 `SUPABASE_DB_URL`

**连接字符串格式**：
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

#### 3. 视频生成超时

**问题**：视频长时间显示"生成中"（超过10分钟）

**解决**：
- 系统会自动检测超时任务（超过10分钟）并标记为失败
- 可以重新生成视频
- 检查即梦 API 服务状态

#### 4. 历史记录不显示

**原因**：数据库未配置或连接失败

**解决**：
1. 检查 Supabase 数据库是否已初始化
2. 检查 Render 环境变量 `SUPABASE_DB_URL` 是否正确
3. 查看 Render 日志，确认数据库连接成功
4. 确认已执行 `supabase_init.sql` 脚本

#### 5. Vercel 部署失败

**原因**：Root Directory 未设置或构建错误

**解决**：
1. 在 Vercel Dashboard 中设置 Root Directory 为 `frontend-nuxt`
2. 检查构建日志中的错误信息
3. 确认 `frontend-nuxt/package.json` 存在

#### 6. DNS 解析不生效

**原因**：DNS 记录配置错误或未生效

**解决**：
1. 检查 DNS 记录是否正确
2. 清除本地 DNS 缓存：
   ```bash
   # Windows
   ipconfig /flushdns
   
   # macOS
   sudo dscacheutil -flushcache
   
   # Linux
   sudo systemd-resolve --flush-caches
   ```
3. 使用在线工具检查：https://dnschecker.org/
4. 等待 DNS 生效（最长 48 小时）

#### 7. API 并发限制 (50430)

**原因**：即梦 API 有并发请求限制

**解决**：
1. 等待其他任务完成
2. 减少同时提交的任务数量
3. 实现任务队列机制（未来优化）

#### 8. 配额耗尽

**原因**：即梦 API 免费额度已用完

**解决**：
1. 登录火山引擎控制台检查配额
2. 充值或升级套餐
3. 等待配额重置（如果按月重置）

### 调试技巧

1. **查看后端日志**
   - Render Dashboard → Logs
   - 查看错误信息和调试输出

2. **查看前端控制台**
   - 浏览器 F12 → Console
   - 查看 JavaScript 错误和网络请求

3. **测试 API 端点**
   - 健康检查：`https://jubianai-backend.onrender.com/health`
   - API 文档：`https://jubianai-backend.onrender.com/docs`

4. **检查数据库**
   - Supabase Dashboard → Table Editor
   - 查看数据是否正确保存

## 📄 许可证

MIT License

## 🔗 相关链接

- [即梦 AI 官方文档](https://www.volcengine.com/docs/85621?lang=zh)
- [Nuxt 3 文档](https://nuxt.com/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Supabase 文档](https://supabase.com/docs)
- [Render 文档](https://render.com/docs)
- [Vercel 文档](https://vercel.com/docs)
- [后端详细文档](./jubianai/README.md) - 后端配置和 API 文档
- [前端文档](./frontend-nuxt/README.md) - 前端开发指南
- [RAG 系统文档](./doubao-rag/README.md) - 视频 RAG 系统使用指南
