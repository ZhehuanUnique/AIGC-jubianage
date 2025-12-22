# 本地测试指南

## 前置要求

1. **安装 Node.js**
   - 访问 [Node.js 官网](https://nodejs.org/) 下载并安装 LTS 版本（推荐 v18 或 v20）
   - 验证安装：
     ```bash
     node --version
     npm --version
     ```

## 安装依赖

```bash
cd frontend-nuxt
npm install
```

## 配置环境变量

创建 `.env` 文件（如果还没有）：

```env
BACKEND_URL=https://jubianai-backend.onrender.com
```

或者使用本地后端（如果本地运行）：

```env
BACKEND_URL=http://localhost:8000
```

## 启动开发服务器

```bash
npm run dev
```

开发服务器将在 `http://localhost:3001` 启动。

## 测试功能

1. **打开浏览器**
   - 访问 `http://localhost:3001`
   - 应该看到"开启你的视频生成 剧变时代!"标题

2. **测试视频生成**
   - 在输入框中输入视频描述（例如："一个3D形象的小男孩，在公园滑滑板"）
   - 选择视频时长（5秒或10秒）
   - （可选）上传首帧和尾帧图片
   - 点击"生成视频"按钮

3. **检查功能**
   - ✅ 输入框正常显示
   - ✅ 首尾帧上传和预览
   - ✅ 生成按钮点击响应
   - ✅ 状态轮询（生成中、完成）
   - ✅ 视频播放和下载

## 常见问题

### 1. 端口被占用

如果 3000 端口被占用，Nuxt 会自动使用下一个可用端口（如 3001）。

### 2. 后端连接失败

- 检查 `.env` 文件中的 `BACKEND_URL` 是否正确
- 确认后端服务正在运行（Render 后端可能需要几秒钟启动）
- 检查浏览器控制台的网络请求

### 3. CORS 错误

如果遇到 CORS 错误，需要确保后端 API 允许来自 `http://localhost:3001` 的请求。

### 4. 依赖安装失败

```bash
# 清除缓存并重新安装
rm -rf node_modules package-lock.json
npm install
```

## 构建生产版本

```bash
npm run build
npm run preview
```

## 下一步

测试完成后，可以：
1. 部署到 Vercel（推荐）
2. 部署到 Netlify
3. 部署到其他支持 Node.js 的平台

