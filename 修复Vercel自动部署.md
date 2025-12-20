# 修复 Vercel 自动部署

## 问题确认

从部署记录看：
- ✅ 手动部署可以工作（"Redeploy of..."）
- ❌ 自动部署不工作（没有从 GitHub 推送自动触发的部署）

## 修复步骤

### 方法一：重新连接 GitHub 仓库（推荐）

1. **在 Vercel 中**
   - 进入项目 → **Settings** → **Git**
   - 点击 **"Disconnect"** 按钮
   - 等待几秒，确认已断开

2. **重新连接**
   - 点击 **"Connect Git Repository"**
   - 选择 **GitHub**
   - 找到并选择 `ZhehuanUnique/AIGC-jubianage`
   - 确认连接

3. **检查设置**
   - Production Branch: 应该是 `main`
   - Auto-deploy: 应该已启用
   - 确认所有设置正确

4. **这会重新创建 Webhook**
   - Vercel 会自动在 GitHub 中创建新的 Webhook
   - 自动部署应该会恢复

### 方法二：检查 GitHub Webhook

1. **在 GitHub 中**
   - 访问：https://github.com/ZhehuanUnique/AIGC-jubianage/settings/hooks
   - 查看是否有 Vercel 的 Webhook
   - 检查 Webhook 状态是否正常

2. **如果 Webhook 不存在或失效**
   - 在 Vercel 中重新连接 GitHub（方法一）
   - 这会自动创建新的 Webhook

### 方法三：手动创建 Webhook（如果方法一不行）

1. **在 GitHub 中**
   - 进入仓库 → Settings → Webhooks
   - 点击 "Add webhook"
   - Payload URL: `https://api.vercel.com/v1/integrations/github`
   - Content type: `application/json`
   - Events: 选择 "Just the push event"
   - 但这个方法比较复杂，建议使用方法一

## 验证自动部署是否修复

重新连接后：

1. **创建一个测试提交**
   ```bash
   echo "test" >> test-auto-deploy.txt
   git add test-auto-deploy.txt
   git commit -m "Test: Verify auto-deploy after reconnect"
   git push origin main
   ```

2. **观察 Vercel**
   - 1-2 分钟内应该自动创建新部署
   - 部署应该显示 "main [commit-hash] Test: Verify..."
   - 而不是 "Redeploy of..."

## 推荐操作

**立即执行**：

1. **在 Vercel 中重新连接 GitHub**
   - Settings → Git → Disconnect
   - 然后 Connect Git Repository
   - 重新选择仓库

2. **等待连接完成**

3. **创建测试提交验证**
   - 推送一个小的更改
   - 观察是否自动部署

## 如果重新连接后还是不工作

可能需要：
1. 检查 Vercel 账号权限
2. 检查 GitHub 仓库权限
3. 联系 Vercel 支持

