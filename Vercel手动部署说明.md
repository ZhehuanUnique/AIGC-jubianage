# Vercel 手动部署说明

## 问题
代码已推送到 GitHub，但 Vercel 没有自动重新部署。

## 解决方案

### 方法一：在 Vercel 网页中手动触发（推荐）

1. **登录 Vercel**
   - 访问 https://vercel.com
   - 登录你的账号

2. **进入项目**
   - 找到 `AIGC-jubianage` 项目
   - 点击进入项目详情页

3. **手动触发部署**
   - 点击 "Deployments" 标签
   - 找到最新的部署记录
   - 点击右侧的 "..." 菜单
   - 选择 "Redeploy"
   - 或者点击顶部的 "Redeploy" 按钮

### 方法二：使用 Vercel CLI

```bash
# 1. 安装 Vercel CLI（如果还没有）
npm i -g vercel

# 2. 登录 Vercel
vercel login

# 3. 在项目根目录部署
cd C:\Users\Administrator\Desktop\AIGC-jubianage
vercel --prod
```

### 方法三：检查自动部署设置

1. **在 Vercel 项目设置中**
   - 进入项目 → Settings → Git
   - 确认 "Production Branch" 设置为 `main`
   - 确认 "Auto-deploy" 已启用

2. **检查 GitHub 集成**
   - 确认 Vercel 已连接 GitHub 仓库
   - 确认仓库权限正确

### 方法四：通过 GitHub 触发

如果 Vercel 已连接 GitHub，可以：

1. **创建一个空提交触发部署**
   ```bash
   git commit --allow-empty -m "Trigger Vercel deployment"
   git push origin main
   ```

2. **或者修改一个小文件**
   - 修改 README.md 添加一个空格
   - 提交并推送

## 验证部署

部署完成后：

1. **检查部署状态**
   - 在 Vercel 项目页面查看部署状态
   - 确认部署成功（绿色勾号）

2. **清除浏览器缓存**
   - 按 `Ctrl + Shift + R`（Windows）或 `Cmd + Shift + R`（Mac）
   - 强制刷新页面查看最新样式

3. **在移动端测试**
   - 使用手机访问 `https://jubianai.cn`
   - 检查卡片是否变小
   - 检查视频是否居中

## 如果还是不行

如果 Vercel 没有自动部署，可能是：

1. **GitHub 集成问题**
   - 检查 Vercel 是否已连接 GitHub
   - 重新连接 GitHub 仓库

2. **分支设置问题**
   - 确认 Production Branch 是 `main`
   - 确认推送到了正确的分支

3. **权限问题**
   - 确认 Vercel 有访问仓库的权限

## 快速操作

最简单的办法：

1. 访问 https://vercel.com
2. 进入 `AIGC-jubianage` 项目
3. 点击 "Redeploy" 按钮
4. 等待部署完成（通常 1-2 分钟）

