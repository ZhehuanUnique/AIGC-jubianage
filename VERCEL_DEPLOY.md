# Vercel 部署问题排查指南

## 问题：静态文件返回 404

如果访问 `https://jubianai.cn/index.html`、`/styles.css`、`/main.js` 都返回 404，说明静态文件没有被部署。

## 解决方案

### 1. 检查 Vercel 项目 Root Directory 设置

**这是最可能的原因！**

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 进入你的项目（jubianai 或 AIGC-jubianage）
3. 点击 **Settings**（设置）
4. 找到 **Root Directory** 设置
5. **必须设置为 `./` 或留空**（不能是 `jubianai` 或其他子目录）

如果 Root Directory 设置为 `jubianai`，Vercel 只会部署 `jubianai/` 目录下的文件，不会部署根目录的 `index.html`、`styles.css`、`main.js` 等文件。

### 2. 确认文件已提交到 Git

确保以下文件已提交到 Git 仓库：
- `index.html`
- `styles.css`
- `main.js`
- `index.mp4`
- `logo/` 目录
- `封面/` 目录
- `vercel.json`

### 3. 重新部署

修改 Root Directory 后，在 Vercel 控制台：
1. 点击 **Deployments**
2. 找到最新的部署
3. 点击 **Redeploy**（重新部署）

### 4. 验证部署

部署完成后，访问：
- `https://jubianai.cn/` - 应该显示页面
- `https://jubianai.cn/index.html` - 应该返回 HTML
- `https://jubianai.cn/styles.css` - 应该返回 CSS
- `https://jubianai.cn/main.js` - 应该返回 JavaScript

## 如果 Root Directory 必须指向子目录

如果你的项目结构要求 Root Directory 必须是 `jubianai`，那么需要：

1. 将静态文件移动到 `jubianai/public/` 目录
2. 修改 `vercel.json` 配置
3. 或者创建符号链接

但这不推荐，建议将 Root Directory 设置为根目录。

