# Railway 部署指南

## 为什么选择 Railway？

- ✅ **每月 $5 免费额度**（足够多个项目使用）
- ✅ **服务不会休眠**（有额度时）
- ✅ **可以创建多个项目**
- ✅ **自动部署，配置简单**
- ✅ **全球 CDN**

## 部署步骤

### 1. 安装 Railway CLI（可选）

```bash
# Windows (PowerShell)
iwr https://railway.app/install.sh | iex

# Mac/Linux
curl -fsSL https://railway.app/install.sh | sh
```

### 2. 在 Railway 创建项目

#### 方法 A：使用 Web Dashboard（推荐）

1. 登录 [Railway Dashboard](https://railway.app/)
2. 点击 **"New Project"**
3. 选择 **"Deploy from GitHub repo"**
4. 选择你的仓库
5. Railway 会自动检测并配置

#### 方法 B：使用 CLI

```bash
railway login
railway init
railway up
```

### 3. 配置服务

Railway 会自动读取 `railway.json` 配置文件。

**如果没有自动配置，手动设置：**

1. 在 Railway Dashboard 中，进入你的项目
2. 点击 **"Settings"** → **"Deploy"**
3. 设置：
   - **Build Command**: `pip install -r jubianai/requirements.txt`
   - **Start Command**: `python jubianai/render_server.py`

### 4. 环境变量

在 Railway Dashboard → **"Variables"** 中添加：

- `PORT`: Railway 自动设置，无需手动配置
- `API_KEY`: 你的 API Key（如果需要）
- `SEEDANCE_API_ENDPOINT`: API 端点（如果需要）

### 5. 自定义域名

1. 在 Railway Dashboard 中，进入你的服务
2. 点击 **"Settings"** → **"Domains"**
3. 添加自定义域名
4. 按照提示配置 DNS

## 多个项目的管理

### 创建多个项目

1. 在 Railway Dashboard 中，点击 **"New Project"**
2. 为每个项目创建独立的服务
3. 每个项目都有独立的 URL 和配置

### 监控使用情况

在 Railway Dashboard 的 **"Usage"** 页面查看：
- 当前使用的额度
- 剩余免费额度
- 各项目的资源使用情况

## 免费额度说明

**每月 $5 免费额度包括：**
- 计算资源（CPU/内存）
- 网络流量
- 存储空间

**对于小型项目**：
- 通常足够 2-3 个项目使用
- 如果超出，可以升级到付费计划

## 与 Render 的对比

| 特性 | Render | Railway |
|------|--------|---------|
| 免费额度 | 750小时/月 | $5/月 |
| 休眠 | 15分钟无活动 | 不休眠 |
| 多项目 | ✅ | ✅ |
| 配置难度 | 中等 | 简单 |
| 全球 CDN | ❌ | ✅ |

## 故障排查

### 构建失败

检查：
- Python 版本是否正确
- 依赖是否完整
- 查看 Railway 日志

### 服务无法启动

检查：
- `railway.json` 配置是否正确
- Start Command 是否正确
- 查看 Railway 日志

## 总结

**Railway 适合：**
- ✅ 需要多个项目的开发者
- ✅ 不希望服务休眠
- ✅ 需要全球 CDN
- ✅ 预算有限但需要稳定服务

**如果免费额度不够用**，可以考虑：
- 优化项目资源使用
- 升级到付费计划（$5/月起）
- 或使用 Render（750小时/月共享）


