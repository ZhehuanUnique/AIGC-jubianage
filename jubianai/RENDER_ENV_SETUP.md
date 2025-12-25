# Render 环境变量配置指南（即梦 API）

## ⚠️ 当前问题

错误信息显示：
```
即梦API认证失败:请检查 API 密钥配置
```

这说明 Render 上的环境变量 `VOLCENGINE_ACCESS_KEY_ID` 和 `VOLCENGINE_SECRET_ACCESS_KEY` 未配置或配置不正确。

## 🔧 配置步骤

### 步骤 1: 登录 Render Dashboard

1. 访问 https://dashboard.render.com
2. 登录你的账号

### 步骤 2: 进入服务设置

1. 在 Dashboard 中找到 `jubianai-backend` 服务
2. 点击进入服务详情页

### 步骤 3: 配置环境变量

1. 点击左侧菜单的 **"Environment"**（环境变量）
2. 点击 **"Add Environment Variable"**（添加环境变量）

### 步骤 4: 添加即梦 API 密钥

添加以下两个环境变量：

#### 环境变量 1: Access Key ID

- **Key**: `VOLCENGINE_ACCESS_KEY_ID`
- **Value**: `你的AccessKeyID`（从即梦控制台获取）
- **Sync**: ✅ 勾选（同步到所有环境）

#### 环境变量 2: Secret Access Key

- **Key**: `VOLCENGINE_SECRET_ACCESS_KEY`
- **Value**: `你的SecretAccessKey`（从即梦控制台获取）
- **Sync**: ✅ 勾选（同步到所有环境）

### 步骤 5: 保存并重新部署

1. 点击 **"Save Changes"**（保存更改）
2. Render 会自动触发重新部署
3. 等待部署完成（通常 2-5 分钟）

### 步骤 6: 验证配置

部署完成后：

1. 查看 **"Logs"** 标签
2. 检查是否有以下信息：
   - ✅ 服务正常启动
   - ✅ 没有 "Access Denied" 错误
   - ✅ 没有 "API 密钥未配置" 警告

3. 测试视频生成：
   - 访问 `https://jubianai.cn`
   - 尝试生成一个视频
   - 应该不再出现认证失败错误

## 📋 完整环境变量清单

除了即梦 API 密钥，如果已配置 Supabase 数据库，还需要：

- **Key**: `SUPABASE_DB_URL`
- **Value**: `postgresql://postgres:你的密码@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres`

## 🔍 验证环境变量

### 方法 1: 查看 Render 日志

在 Render Dashboard → Logs 中，启动时应该能看到环境变量加载的信息（如果代码中有打印）。

### 方法 2: 测试 API

访问健康检查端点：
```
https://jubianai-backend.onrender.com/health
```

应该返回：
```json
{"status": "healthy"}
```

### 方法 3: 测试视频生成

在 `jubianai.cn` 上尝试生成视频，如果配置正确，应该不再出现认证失败错误。

## 🆘 常见问题

### 问题 1: 环境变量已设置但仍报错

**解决**:
- 确认环境变量名称完全正确（区分大小写）
- 确认没有多余空格
- 确认已重新部署（环境变量更改后需要重新部署）

### 问题 2: 不知道如何找到环境变量设置

**解决**:
- Render Dashboard → 选择服务 → 左侧菜单 → "Environment"
- 或者直接访问：`https://dashboard.render.com/web/[你的服务ID]/environment`

### 问题 3: 部署后仍然报错

**解决**:
1. 等待部署完全完成（查看部署状态）
2. 检查日志中是否有其他错误
3. 确认环境变量已保存（刷新页面检查）

## ✅ 配置检查清单

- [ ] 已在 Render Dashboard 中进入 `jubianai-backend` 服务
- [ ] 已添加 `VOLCENGINE_ACCESS_KEY_ID` 环境变量
- [ ] 已添加 `VOLCENGINE_SECRET_ACCESS_KEY` 环境变量
- [ ] 环境变量值正确（无多余空格）
- [ ] 已点击 "Save Changes"
- [ ] 已等待重新部署完成
- [ ] 已测试视频生成功能

## 📝 重要提示

1. **环境变量是敏感信息**，不要提交到 Git
2. **`.env` 文件不会推送到 GitHub**（已在 `.gitignore` 中）
3. **必须在 Render Dashboard 中手动配置**环境变量
4. **环境变量更改后需要重新部署**才能生效

## 🔗 相关文档

- API 密钥配置指南: `jubianai/SETUP_API_KEYS.md`
- Access Denied 错误修复: `jubianai/ACCESS_DENIED_FIX.md`
- Render 数据库配置: `jubianai/RENDER_DB_SETUP.md`


