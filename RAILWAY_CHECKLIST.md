# Railway 部署检查清单

## ✅ 已创建的配置文件

- [x] `railway.json` - Railway 主配置文件
- [x] `runtime.txt` - Python 版本指定（可选）
- [x] `Procfile` - 启动命令（备用，Railway 优先使用 railway.json）
- [x] `jubianai/render_server.py` - 服务器入口（已优化）
- [x] `RAILWAY_QUICK_START.md` - 快速部署指南
- [x] `RAILWAY_DEPLOY.md` - 详细部署文档

## 📝 部署前检查

### 1. 确认文件已提交到 Git

运行以下命令检查：

```bash
git status
```

确保以下文件已提交：
- ✅ `railway.json`
- ✅ `jubianai/render_server.py`
- ✅ `jubianai/requirements.txt`
- ✅ `jubianai/backend/api.py`
- ✅ `index.html`
- ✅ `styles.css`
- ✅ `main.js`
- ✅ 其他静态文件（logo、封面等）

### 2. 本地测试（可选但推荐）

```bash
# 安装依赖
pip install -r jubianai/requirements.txt

# 测试启动
python jubianai/render_server.py
```

访问 `http://localhost:8000` 确认服务正常。

### 3. 提交代码

```bash
git add .
git commit -m "Configure Railway deployment"
git push
```

## 🚀 部署步骤

### 方法 1：Web Dashboard（推荐）

1. 访问 [railway.app](https://railway.app/)
2. 使用 GitHub 登录
3. 点击 **"New Project"**
4. 选择 **"Deploy from GitHub repo"**
5. 选择你的仓库
6. Railway 会自动检测并部署

### 方法 2：Railway CLI

```bash
railway login
railway init
railway up
```

## ⚙️ 配置说明

### railway.json 配置

```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r jubianai/requirements.txt"
  },
  "deploy": {
    "startCommand": "python jubianai/render_server.py"
  }
}
```

### 环境变量（可选）

在 Railway Dashboard → Variables 中设置：
- `API_KEY`: API 密钥
- `SEEDANCE_API_ENDPOINT`: API 端点

**注意**：`PORT` 由 Railway 自动设置，无需配置。

## 🔍 验证部署

部署完成后，访问 Railway 提供的 URL：

- ✅ `https://your-app.railway.app/` - 前端页面
- ✅ `https://your-app.railway.app/health` - 健康检查
- ✅ `https://your-app.railway.app/api/health` - API 健康检查
- ✅ `https://your-app.railway.app/styles.css` - CSS 文件
- ✅ `https://your-app.railway.app/main.js` - JavaScript 文件

## 🐛 常见问题

### 构建失败

**原因**：依赖安装失败
**解决**：检查 `jubianai/requirements.txt` 是否正确

### 服务无法启动

**原因**：启动命令错误或路径问题
**解决**：检查 `railway.json` 中的 `startCommand`

### 静态文件 404

**原因**：文件路径不正确
**解决**：检查 `render_server.py` 中的路径配置

## 📚 相关文档

- `RAILWAY_QUICK_START.md` - 5分钟快速部署指南
- `RAILWAY_DEPLOY.md` - 详细部署文档
- [Railway 官方文档](https://docs.railway.app/)

## ✨ 完成！

部署成功后，你的网站就可以通过 Railway 访问了！


