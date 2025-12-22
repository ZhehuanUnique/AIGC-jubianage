# Render 手动部署指南（不使用 Blueprint）

## 为什么手动部署？

- ✅ 可以创建**多个服务**（没有数量限制）
- ✅ 每个项目独立配置
- ✅ 共享每月 750 小时免费额度
- ✅ 更灵活的控制

## 部署步骤

### 1. 在 Render 创建 Web Service

1. 登录 [Render Dashboard](https://dashboard.render.com/)
2. 点击 **"New +"** → **"Web Service"**（不是 Blueprint）
3. 连接你的 Git 仓库

### 2. 配置服务

**基本信息：**
- **Name**: `jubianai`（或你的项目名）
- **Region**: 选择离你最近的区域
- **Branch**: `main`（或你的主分支）
- **Root Directory**: 留空

**构建和启动：**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r jubianai/requirements.txt`
- **Start Command**: `python jubianai/render_server.py`

**环境变量（可选）：**
- `API_KEY`: 你的 API Key
- `SEEDANCE_API_ENDPOINT`: API 端点

### 3. 创建服务

点击 **"Create Web Service"**，Render 会自动开始部署。

### 4. 添加其他项目

重复上述步骤，为每个项目创建独立的 Web Service。

**注意**：
- 每个服务都有独立的 URL
- 所有服务共享 750 小时/月的免费额度
- 每个服务在 15 分钟无活动后会休眠

## 多个项目的管理

### 项目命名建议

- `jubianai` - 主项目
- `project-2` - 第二个项目
- `project-3` - 第三个项目

### 监控使用情况

在 Render Dashboard 的 **"Usage"** 页面查看：
- 当前使用的运行时间
- 剩余免费额度
- 各服务的资源使用情况

## 避免休眠的方法

### 方法 1：使用 Uptime Robot（免费）

1. 注册 [Uptime Robot](https://uptimerobot.com/)
2. 添加监控，每 5 分钟访问你的服务
3. 保持服务活跃，避免休眠

### 方法 2：升级到付费计划

- **Starter**: $7/月，服务不休眠
- **Standard**: $25/月，更多资源

## 与 Blueprint 的区别

| 特性 | Blueprint | 手动创建 |
|------|-----------|---------|
| 服务数量 | 1 个 Blueprint | 多个服务 |
| 配置方式 | YAML 文件 | Dashboard |
| 灵活性 | 较低 | 较高 |
| 适用场景 | 单项目 | 多项目 |

## 总结

**手动创建 Web Service 的优势：**
- ✅ 可以创建多个服务
- ✅ 每个项目独立管理
- ✅ 配置更灵活
- ✅ 完全免费（在额度内）

**建议**：如果你的项目不多（1-3 个），使用 Render 手动创建服务就足够了。


