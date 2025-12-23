# 部署到 jubianai.cn 完整指南

## 📋 部署步骤概览

1. ✅ 推送到 GitHub
2. ✅ 在 Vercel 上部署项目
3. ✅ 配置自定义域名 `jubianai.cn`
4. ✅ 配置 DNS 解析

---

## 第一步：推送到 GitHub

### 1.1 在本地终端执行

```bash
cd /workspaces/AIGC-jubianage

# 检查状态
git status

# 推送到 GitHub
git push origin main
```

**如果提示输入凭据：**
- **用户名**: 你的 GitHub 用户名
- **密码**: 使用 Personal Access Token（不是 GitHub 密码）
  - 生成 Token: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
  - 权限: 至少需要 `repo` 权限

---

## 第二步：在 Vercel 上部署

### 2.1 登录 Vercel Dashboard

1. 访问 https://vercel.com/dashboard
2. 使用 GitHub 账号登录（确保是会员账号）

### 2.2 导入项目

1. 点击 **"Add New..."** → **"Project"**
2. 在项目列表中找到 `ZhehuanUnique/AIGC-jubianage`
3. 点击 **"Import"**

### 2.3 配置项目设置 ⚠️ **非常重要**

在 "Configure Project" 页面：

1. **Root Directory** ⚠️ **必须设置**
   - 找到 "Root Directory" 选项
   - 点击 **"Edit"**
   - 输入：`frontend-nuxt`
   - 点击 **"Save"**
   - **如果不设置这个，Vercel 会在根目录查找项目，导致部署失败**

2. **Framework Preset**
   - 应该自动检测为 **Nuxt.js**
   - 如果没有，手动选择 **Nuxt.js**

3. **Build Command**
   - 自动填充：`npm run build`
   - 确认正确

4. **Output Directory**
   - 自动填充：`.output/public`
   - 确认正确

5. **Install Command**
   - 自动填充：`npm install`
   - 确认正确

### 2.4 环境变量（可选）

如果需要自定义后端地址：

1. 在 "Environment Variables" 部分
2. 添加新变量：
   - **Key**: `BACKEND_URL`
   - **Value**: `https://jubianai-backend.onrender.com`
   - **Environment**: Production, Preview, Development（全选）

### 2.5 开始部署

1. 点击 **"Deploy"** 按钮
2. 等待构建完成（通常 2-5 分钟）
3. 部署成功后，Vercel 会提供一个 URL，如：`https://aigc-jubianage-xxx.vercel.app`

---

## 第三步：配置自定义域名 jubianai.cn

### 3.1 在 Vercel Dashboard 中添加域名

1. 进入项目页面
2. 点击顶部菜单 **"Settings"**
3. 在左侧菜单中找到 **"Domains"**
4. 在 "Domains" 页面，输入你的域名：`jubianai.cn`
5. 点击 **"Add"**

### 3.2 获取 DNS 配置信息

添加域名后，Vercel 会显示需要配置的 DNS 记录：

**通常有两种配置方式：**

#### 方式 A：使用 CNAME（推荐）

```
类型: CNAME
名称: @ 或 jubianai.cn
值: cname.vercel-dns.com
```

#### 方式 B：使用 A 记录

```
类型: A
名称: @ 或 jubianai.cn
值: 76.76.21.21（Vercel 提供的 IP）
```

**Vercel 会显示具体的配置信息，请按照 Vercel 显示的配置**

---

## 第四步：配置 DNS 解析

### 4.1 登录域名注册商

1. 登录你注册 `jubianai.cn` 的域名服务商（如：阿里云、腾讯云、GoDaddy 等）
2. 找到 **"域名管理"** 或 **"DNS 解析"** 功能

### 4.2 添加 DNS 记录

根据 Vercel 提供的配置信息，添加相应的 DNS 记录：

**示例（以阿里云为例）：**

1. 进入域名解析设置
2. 点击 **"添加记录"**
3. 填写信息：
   - **记录类型**: CNAME（或 A 记录，根据 Vercel 提示）
   - **主机记录**: `@`（表示根域名）或留空
   - **记录值**: Vercel 提供的值（如 `cname.vercel-dns.com`）
   - **TTL**: 600（或默认值）
4. 点击 **"确认"**

**如果需要同时支持 www 子域名：**

添加第二条记录：
- **记录类型**: CNAME
- **主机记录**: `www`
- **记录值**: `cname.vercel-dns.com`

### 4.3 等待 DNS 生效

- DNS 解析通常需要 **5 分钟到 48 小时** 生效
- 大多数情况下，**10-30 分钟** 内生效
- 可以使用以下命令检查 DNS 是否生效：

```bash
# 检查 DNS 解析
nslookup jubianai.cn
# 或
dig jubianai.cn
```

---

## 第五步：验证部署

### 5.1 检查域名状态

1. 回到 Vercel Dashboard
2. 在 "Domains" 页面查看域名状态
3. 如果显示 **"Valid Configuration"** 或 **"Valid"**，说明配置成功

### 5.2 访问网站

1. 在浏览器中访问：`https://jubianai.cn`
2. 如果看到你的应用界面，说明部署成功！

### 5.3 测试功能

- ✅ 首页加载正常
- ✅ 导航栏显示正确（视频生成、资产管理、知识库）
- ✅ 可以输入提示词
- ✅ 可以上传首帧图片
- ✅ 可以点击"生成视频"按钮
- ✅ 视频生成功能正常

---

## 🔧 常见问题

### 问题 1: DNS 解析不生效

**原因**: DNS 缓存或配置错误

**解决**:
1. 检查 DNS 记录是否正确
2. 清除本地 DNS 缓存：
   ```bash
   # Windows
   ipconfig /flushdns
   
   # macOS
   sudo dscacheutil -flushcache
   
   # Linux
   sudo systemd-resolve --flush-caches
   ```
3. 使用在线 DNS 检查工具：https://dnschecker.org/

### 问题 2: Vercel 显示域名配置无效

**原因**: DNS 记录未正确配置或未生效

**解决**:
1. 确认 DNS 记录已添加
2. 等待 DNS 生效（最多 48 小时）
3. 检查 DNS 记录值是否正确

### 问题 3: 网站显示 404 或无法访问

**原因**: Root Directory 未设置或构建失败

**解决**:
1. 检查 Vercel 项目设置中的 Root Directory 是否为 `frontend-nuxt`
2. 查看 Vercel 构建日志，确认构建成功
3. 检查 `vercel.json` 配置是否正确

### 问题 4: HTTPS 证书问题

**解决**:
- Vercel 会自动为自定义域名配置 SSL 证书
- 通常需要等待几分钟到几小时
- 如果长时间未生效，联系 Vercel 支持

---

## 📝 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] Vercel 项目已创建
- [ ] Root Directory 设置为 `frontend-nuxt`
- [ ] 首次部署成功
- [ ] 自定义域名 `jubianai.cn` 已添加
- [ ] DNS 记录已配置
- [ ] DNS 解析已生效
- [ ] 可以通过 `https://jubianai.cn` 访问
- [ ] 所有功能测试通过

---

## 🎯 快速命令参考

```bash
# 1. 推送代码
cd /workspaces/AIGC-jubianage
git push origin main

# 2. 检查 DNS 解析
nslookup jubianai.cn
dig jubianai.cn

# 3. 清除本地 DNS 缓存（Windows）
ipconfig /flushdns
```

---

## 📞 需要帮助？

如果遇到问题，请提供：
- 错误信息截图
- Vercel 构建日志
- DNS 配置截图
- 域名注册商信息

---

## 🎉 部署成功后

部署成功后，你的应用将可以通过以下方式访问：
- **主域名**: https://jubianai.cn
- **Vercel 默认 URL**: https://aigc-jubianage-xxx.vercel.app（会自动重定向到自定义域名）

每次推送到 GitHub 的 `main` 分支，Vercel 会自动重新部署！

