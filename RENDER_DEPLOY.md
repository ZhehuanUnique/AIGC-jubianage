# Render 部署指南

## 概述

项目已从 Vercel 迁移到 Render。Render 使用 FastAPI 同时处理 API 路由和静态文件服务。

## 部署步骤

### 1. 在 Render 创建 Web Service

1. 登录 [Render Dashboard](https://dashboard.render.com/)
2. 点击 "New +" → "Web Service"
3. 连接你的 Git 仓库
4. 配置如下：

**基本信息：**
- **Name**: `jubianai` (或你喜欢的名称)
- **Region**: 选择离你最近的区域
- **Branch**: `main` (或你的主分支)
- **Root Directory**: 留空（项目在根目录）

**构建和启动：**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r jubianai/requirements.txt`
- **Start Command**: `python jubianai/render_server.py`

**环境变量（可选）：**
- `PORT`: Render 会自动设置，无需手动配置
- `API_KEY`: 你的 API Key（如果需要）
- `SEEDANCE_API_ENDPOINT`: API 端点（如果需要）

### 2. 使用 render.yaml（推荐）

如果你使用 `render.yaml` 文件：

1. 在 Render Dashboard 中，选择 "New +" → "Blueprint"
2. 连接你的 Git 仓库
3. Render 会自动读取 `render.yaml` 并创建服务

### 3. 自定义域名

1. 在 Render Dashboard 中，进入你的 Web Service
2. 点击 "Settings" → "Custom Domains"
3. 添加你的域名 `jubianai.cn`
4. 按照提示配置 DNS 记录

## 项目结构

```
.
├── render.yaml              # Render 配置文件
├── jubianai/
│   ├── render_server.py    # Render 服务器入口
│   ├── backend/
│   │   └── api.py          # FastAPI 后端 API
│   └── requirements.txt    # Python 依赖
├── index.html              # 前端页面
├── styles.css              # 样式文件
├── main.js                 # JavaScript 文件
└── ...                     # 其他静态文件
```

## 路由说明

- `/` - 返回 `index.html`（前端页面）
- `/api/*` - API 路由（由 FastAPI 处理）
- `/styles.css` - CSS 文件
- `/main.js` - JavaScript 文件
- `/logo/*` - Logo 图片
- `/封面/*` - 封面图片
- `/health` - 健康检查

## 与 Vercel 的区别

1. **部署方式**：
   - Vercel: Serverless Functions
   - Render: Web Service（持续运行）

2. **静态文件**：
   - Vercel: 自动部署静态文件
   - Render: 通过 FastAPI 服务静态文件

3. **配置**：
   - Vercel: `vercel.json`
   - Render: `render.yaml` 或 Dashboard 配置

## 故障排查

### 1. 构建失败

检查：
- Python 版本是否正确（3.11.0）
- 依赖是否完整（`jubianai/requirements.txt`）
- 构建日志中的错误信息

### 2. 静态文件 404

检查：
- 文件是否在项目根目录
- `render_server.py` 中的路径是否正确
- 文件是否已提交到 Git

### 3. API 路由不工作

检查：
- 后端 API 是否正确导入
- 路由路径是否正确（`/api/v1/...`）
- 查看 Render 日志中的错误信息

## 环境变量

在 Render Dashboard → Environment 中设置：

- `API_KEY`: API 密钥
- `SEEDANCE_API_ENDPOINT`: API 端点 URL
- `PORT`: Render 自动设置，无需手动配置

## 监控和日志

- 在 Render Dashboard 中查看实时日志
- 设置健康检查路径：`/health`
- 查看 Metrics 了解服务性能

## 免费计划限制

Render 免费计划：
- 服务在 15 分钟无活动后休眠
- 首次访问需要几秒钟唤醒
- 每月 750 小时运行时间

如果需要避免休眠，可以升级到付费计划。

