# 剧变时代 - 前端应用

基于 Vue 3 + Nuxt 3 + TypeScript + Tailwind CSS + Pinia 的视频生成前端应用。

## 技术栈

- **Vue 3**: 渐进式 JavaScript 框架
- **Nuxt 3**: Vue 3 的全栈框架
- **TypeScript**: 类型安全的 JavaScript
- **Tailwind CSS**: 实用优先的 CSS 框架
- **Pinia**: Vue 的状态管理库

## 快速开始

### 方式一：使用启动脚本（推荐）

```bash
cd frontend-nuxt
./start.sh
```

### 方式二：手动启动

```bash
# 1. 安装依赖
npm install

# 2. 配置环境变量（可选）
# 创建 .env 文件，设置 BACKEND_URL
echo "BACKEND_URL=https://jubianai-backend.onrender.com" > .env

# 3. 启动开发服务器
npm run dev
```

访问 `http://localhost:3001` 查看应用。

## 开发命令

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 环境变量

创建 `.env` 文件：

```env
BACKEND_URL=https://jubianai-backend.onrender.com
```

## 部署

### Vercel

1. 连接 GitHub 仓库
2. 设置构建命令：`npm run build`
3. 设置输出目录：`.output/public`
4. 配置环境变量：`BACKEND_URL`

### Netlify

1. 连接 GitHub 仓库
2. 构建命令：`npm run build`
3. 发布目录：`.output/public`

