# Vercel 自动部署问题排查

## 可能的原因

### 1. GitHub 集成断开
- Vercel 可能失去了与 GitHub 的连接
- 需要重新连接仓库

### 2. 自动部署被关闭
- 项目设置中可能关闭了自动部署
- 需要检查并启用

### 3. 分支设置问题
- Production Branch 可能设置错误
- 需要确认是 `main` 分支

### 4. Webhook 问题
- GitHub Webhook 可能失效
- 需要重新配置

## 解决方案

### 方法一：检查并重新连接 GitHub（推荐）

1. **进入 Vercel 项目设置**
   - 访问 https://vercel.com
   - 进入 `AIGC-jubianage` 项目
   - 点击 "Settings" → "Git"

2. **检查 GitHub 连接**
   - 查看 "Git Repository" 部分
   - 确认显示 `ZhehuanUnique/AIGC-jubianage`
   - 如果显示 "Disconnected" 或有问题，点击 "Disconnect"
   - 然后点击 "Connect Git Repository"
   - 重新选择 `ZhehuanUnique/AIGC-jubianage` 仓库

3. **检查自动部署设置**
   - 确认 "Auto-deploy" 已启用
   - 确认 "Production Branch" 设置为 `main`

### 方法二：手动触发部署

如果自动部署不工作，可以手动触发：

1. **在 Vercel 中**
   - 进入项目 → "Deployments"
   - 选择一个 "Ready" 状态的部署
   - 点击 "Redeploy"

2. **或者使用 Vercel CLI**
   ```bash
   vercel --prod
   ```

### 方法三：检查 GitHub Webhook

1. **在 GitHub 仓库中**
   - 访问 https://github.com/ZhehuanUnique/AIGC-jubianage/settings/hooks
   - 查看是否有 Vercel 的 Webhook
   - 如果不存在或失效，Vercel 重新连接时会自动创建

### 方法四：重新授权 Vercel

1. **在 Vercel 中**
   - 进入 Account Settings → "Connected Accounts"
   - 检查 GitHub 连接状态
   - 如果有问题，断开并重新连接

## 快速检查清单

- [ ] GitHub 仓库连接正常
- [ ] Auto-deploy 已启用
- [ ] Production Branch 是 `main`
- [ ] 最近有推送到 `main` 分支
- [ ] GitHub Webhook 存在且有效

## 推荐操作步骤

1. **立即执行**：
   - 进入 Vercel 项目 → Settings → Git
   - 检查所有设置
   - 如果有问题，断开并重新连接 GitHub

2. **验证**：
   - 创建一个小的测试提交
   - 推送到 GitHub
   - 观察 Vercel 是否自动部署

3. **如果还是不行**：
   - 手动触发一次部署
   - 然后观察后续推送是否自动部署

## 常见问题

### Q: 为什么之前可以自动部署，现在不行？
A: 可能是：
- GitHub token 过期
- Vercel 权限被撤销
- Webhook 被删除
- 需要重新授权

### Q: 如何确认自动部署已恢复？
A: 
- 推送一个小的更改到 GitHub
- 在 Vercel 中观察是否自动创建新部署
- 通常 1-2 分钟内会开始部署

