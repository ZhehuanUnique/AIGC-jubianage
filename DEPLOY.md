# Vercel 部署说明

## 项目结构

```
AIGC-jubianage/
├── index.html          # 主页（横向流动展示）
├── main.js            # 主页 JavaScript
├── styles.css         # 主页样式
├── index.mp4          # 背景视频
├── logo/              # Logo 文件
├── 封面/              # 封面图片
├── vercel.json        # Vercel 配置
└── jubianai/          # API 后端
    └── api/
        └── index.py   # Vercel Serverless Function
```

## 部署步骤

### 1. 确保所有文件已提交到 Git

```bash
git add .
git commit -m "Update homepage and API"
git push
```

### 2. Vercel 自动部署

如果已经连接到 Vercel，推送代码后会自动触发部署。

### 3. 手动触发部署

在 Vercel Dashboard 中点击 "Redeploy"

## 路由说明

根据 `vercel.json` 配置：

- `/` → `/index.html` （主页）
- `/api/*` → `jubianai/api/index.py` （API 接口）
- 其他静态文件（`.html`, `.js`, `.css`, 图片, 视频等）直接返回

## 注意事项

1. **确保所有静态资源都在根目录或子目录中**
   - `index.html`, `main.js`, `styles.css` 应在根目录
   - `logo/` 和 `封面/` 目录应包含所有图片文件

2. **视频文件大小**
   - `index.mp4` 如果很大，可能需要较长的部署时间
   - 确保视频文件已提交到 Git

3. **检查部署日志**
   - 在 Vercel Dashboard 中查看部署日志
   - 确认所有文件都被正确上传

## 验证部署

部署成功后：

1. 访问 `https://jubianai.cn/` 应该看到主页
2. 检查浏览器控制台是否有资源加载错误
3. 确认背景视频是否正常播放
4. 确认横向滚动是否正常工作

## 常见问题

### 主页不显示

1. **检查文件是否存在**
   - 确认 `index.html` 在根目录
   - 确认所有引用的资源文件都存在

2. **检查路由配置**
   - 确认 `vercel.json` 中的路由配置正确
   - 根路径 `/` 应该指向 `/index.html`

3. **清除缓存**
   - Vercel 可能有缓存，尝试强制刷新（Ctrl+F5）
   - 或在 Vercel Dashboard 中清除缓存

### 静态资源 404

1. **检查文件路径**
   - 确认文件在正确的位置
   - 相对路径应该从项目根目录开始

2. **检查文件名大小写**
   - Linux 服务器区分大小写
   - 确保文件名大小写与 HTML 中的引用一致

### API 不工作

1. **检查 Serverless Function**
   - 在 Vercel Dashboard 的 Functions 标签中查看
   - 检查日志是否有错误

2. **检查路径**
   - API 路径应该是 `/api/*`
   - 确认 `jubianai/api/index.py` 文件存在

