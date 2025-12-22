# Railway 快速部署指南

## 🚀 5 分钟快速部署

### 步骤 1：准备代码

确保以下文件已提交到 Git：
- ✅ `railway.json` - Railway 配置
- ✅ `jubianai/render_server.py` - 服务器入口
- ✅ `jubianai/requirements.txt` - Python 依赖
- ✅ `runtime.txt` - Python 版本（可选）
- ✅ `Procfile` - 启动命令（可选，Railway 会优先使用 railway.json）

### 步骤 2：在 Railway 创建项目

#### 方法 A：使用 Web Dashboard（推荐，最简单）

1. **登录 Railway**
   - 访问 [railway.app](https://railway.app/)
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 **"New Project"**
   - 选择 **"Deploy from GitHub repo"**
   - 选择你的仓库 `AIGC-jubianage`

3. **Railway 会自动检测配置**
   - 自动读取 `railway.json`
   - 自动安装依赖
   - 自动启动服务

4. **等待部署完成**
   - 查看部署日志
   - 部署成功后，Railway 会提供一个 URL（如：`xxx.railway.app`）

#### 方法 B：使用 Railway CLI

```bash
# 1. 安装 Railway CLI
# Windows (PowerShell)
iwr https://railway.app/install.sh | iex

# Mac/Linux
curl -fsSL https://railway.app/install.sh | sh

# 2. 登录
railway login

# 3. 初始化项目
railway init

# 4. 部署
railway up
```

### 步骤 3：配置环境变量（可选）

如果需要配置环境变量：

1. 在 Railway Dashboard 中，进入你的服务
2. 点击 **"Variables"** 标签
3. 添加环境变量：
   - `API_KEY`: 你的 API Key（如果需要）
   - `SEEDANCE_API_ENDPOINT`: API 端点（如果需要）

**注意**：`PORT` 环境变量由 Railway 自动设置，无需手动配置。

### 步骤 4：配置自定义域名

1. 在 Railway Dashboard 中，进入你的服务
2. 点击 **"Settings"** → **"Domains"**
3. 点击 **"Generate Domain"** 或 **"Custom Domain"**
4. 如果使用自定义域名（如 `jubianai.cn`）：
   - 添加域名
   - 按照提示配置 DNS 记录
   - 等待 DNS 生效（通常几分钟）

## 📋 验证部署

部署完成后，访问你的 Railway URL，检查：

- ✅ `/` - 应该显示前端页面
- ✅ `/health` - 应该返回 `{"status": "ok", "message": "服务运行正常"}`
- ✅ `/api/health` - 应该返回 API 健康检查
- ✅ `/styles.css` - 应该返回 CSS 文件
- ✅ `/main.js` - 应该返回 JavaScript 文件

## 🔧 故障排查

### 问题 1：构建失败

**检查**：
- 查看 Railway 部署日志
- 确认 `jubianai/requirements.txt` 存在且正确
- 确认 Python 版本兼容（3.11.0）

**解决**：
```bash
# 本地测试构建
pip install -r jubianai/requirements.txt
python jubianai/render_server.py
```

### 问题 2：服务无法启动

**检查**：
- 查看 Railway 日志
- 确认 `render_server.py` 路径正确
- 确认端口配置正确（Railway 自动设置 PORT）

**解决**：
- 检查 `railway.json` 中的 `startCommand`
- 确认所有依赖已安装

### 问题 3：静态文件 404

**检查**：
- 确认静态文件在项目根目录
- 确认 `render_server.py` 中的路径正确
- 查看 Railway 日志中的错误信息

**解决**：
- 检查文件是否已提交到 Git
- 确认文件路径在 `render_server.py` 中正确

### 问题 4：API 路由不工作

**检查**：
- 确认后端 API 正确导入
- 查看 Railway 日志
- 测试 `/api/health` 端点

**解决**：
- 检查 `jubianai/backend/api.py` 是否存在
- 确认所有依赖已安装

## 📊 监控和管理

### 查看日志

在 Railway Dashboard 中：
- 点击你的服务
- 查看 **"Deployments"** 标签
- 点击部署查看实时日志

### 查看使用情况

在 Railway Dashboard 的 **"Usage"** 页面：
- 查看当前使用的额度
- 查看剩余免费额度
- 查看各服务的资源使用

### 重启服务

在 Railway Dashboard 中：
- 点击你的服务
- 点击 **"Deployments"**
- 点击 **"Redeploy"**

## 💰 免费额度说明

**Railway 免费计划**：
- 每月 $5 免费额度
- 通常足够 2-3 个小项目使用
- 超出后可以升级到付费计划

**监控使用情况**：
- 在 Dashboard 的 **"Usage"** 页面查看
- 设置使用提醒（在设置中配置）

## 🎉 完成！

部署成功后，你的网站应该可以正常访问了！

**下一步**：
- 配置自定义域名
- 设置环境变量（如果需要）
- 监控服务运行状态

## 📚 相关文档

- [Railway 官方文档](https://docs.railway.app/)
- [Railway 定价](https://railway.app/pricing)
- `RAILWAY_DEPLOY.md` - 详细部署文档


