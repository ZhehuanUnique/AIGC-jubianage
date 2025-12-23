# 配置 jubianai.cn 指向 Vercel 部署

## 当前状态

- Vercel 部署地址：`https://aigc-jubianage.vercel.app/`
- 目标域名：`jubianai.cn`
- 需要将 `jubianai.cn` 指向 Vercel 部署的页面

## 步骤 1: 在 Vercel 中添加自定义域名

1. **登录 Vercel Dashboard**
   - 访问 https://vercel.com/dashboard
   - 选择项目 `AIGC-jubianage`

2. **添加自定义域名**
   - 进入项目设置 → **Settings** → **Domains**
   - 点击 **Add Domain**
   - 输入域名：`jubianai.cn`
   - 点击 **Add**

3. **添加 www 子域名（可选）**
   - 再次点击 **Add Domain**
   - 输入：`www.jubianai.cn`
   - 点击 **Add**

## 步骤 2: 配置 DNS 记录

在域名注册商（如阿里云、腾讯云、GoDaddy 等）的 DNS 管理中添加以下记录：

### 方式一：使用 CNAME 记录（推荐）

**主域名（jubianai.cn）**：
```
类型: CNAME
主机记录: @ (或留空，取决于 DNS 提供商)
记录值: cname.vercel-dns.com
TTL: 3600 (或自动)
```

**www 子域名**：
```
类型: CNAME
主机记录: www
记录值: cname.vercel-dns.com
TTL: 3600 (或自动)
```

### 方式二：使用 A 记录（如果 CNAME 不支持）

如果域名提供商不支持根域名的 CNAME 记录，使用 A 记录：

**主域名（jubianai.cn）**：
```
类型: A
主机记录: @
记录值: 76.76.21.21 (Vercel 的 IP，请查看 Vercel 提供的具体 IP)
TTL: 3600
```

**www 子域名**：
```
类型: CNAME
主机记录: www
记录值: cname.vercel-dns.com
TTL: 3600
```

> **注意**：Vercel 会在添加域名后显示具体的 DNS 配置信息，请按照 Vercel 提供的配置进行设置。

## 步骤 3: 等待 DNS 生效

1. **DNS 传播时间**
   - 通常需要几分钟到几小时
   - 最长可能需要 24-48 小时

2. **验证 DNS 配置**
   ```bash
   # 检查 DNS 解析
   nslookup jubianai.cn
   dig jubianai.cn
   ```

3. **在 Vercel 中验证**
   - 返回 Vercel Dashboard → Domains
   - 查看域名状态
   - 显示 "Valid Configuration" 表示配置正确

## 步骤 4: SSL 证书自动配置

Vercel 会自动为自定义域名配置 SSL 证书：
- 证书类型：Let's Encrypt
- 自动续期：是
- 配置时间：DNS 生效后几分钟内

## 步骤 5: 验证部署

1. **访问测试**
   - 访问 `https://jubianai.cn`
   - 应该显示 Vercel 部署的页面

2. **检查 HTTPS**
   - 确保自动跳转到 HTTPS
   - 浏览器显示安全锁图标

3. **测试功能**
   - 检查页面加载是否正常
   - 测试视频生成功能
   - 检查 API 连接

## 故障排除

### 问题 1: DNS 未生效

**症状**：访问 `jubianai.cn` 显示错误或无法访问

**解决方案**：
- 检查 DNS 记录是否正确
- 等待 DNS 传播（最长 48 小时）
- 使用在线工具检查 DNS：https://dnschecker.org/

### 问题 2: SSL 证书未生成

**症状**：HTTPS 访问显示证书错误

**解决方案**：
- 确保 DNS 记录已正确配置
- 等待 Vercel 自动生成证书（通常几分钟）
- 在 Vercel Dashboard 中检查证书状态

### 问题 3: 显示旧的页面内容

**症状**：访问域名显示旧的静态页面，而不是新的 Nuxt 3 前端

**解决方案**：
1. **检查 Vercel 项目配置**
   - 确保 Root Directory 设置为 `frontend-nuxt`（如果单独部署 Nuxt）
   - 或者确保根目录的 `vercel.json` 配置正确

2. **重新部署**
   - 在 Vercel Dashboard 中触发新的部署
   - 确保部署的是最新的代码

3. **检查构建配置**
   - 确保 `vercel.json` 中的配置正确
   - 检查构建日志是否有错误

### 问题 4: 页面显示 JS 加载失败

**症状**：页面显示 "JS: X 加载失败"

**解决方案**：
1. **检查构建输出**
   - 在 Vercel Dashboard 中查看构建日志
   - 确保构建成功

2. **检查资源路径**
   - 确保所有资源路径使用相对路径
   - 检查 `nuxt.config.ts` 中的配置

3. **清除缓存**
   - 在 Vercel 中重新部署
   - 清除浏览器缓存

## 当前 Vercel 项目配置建议

如果当前 Vercel 项目部署的是根目录的静态文件，需要：

### 选项 A: 创建新的 Vercel 项目（推荐）

1. 在 Vercel 中创建新项目
2. 连接同一个 GitHub 仓库
3. 设置 Root Directory 为 `frontend-nuxt`
4. 配置构建命令和输出目录
5. 添加自定义域名 `jubianai.cn`

### 选项 B: 修改现有项目配置

1. 在 Vercel 项目设置中
2. 修改 Root Directory 为 `frontend-nuxt`
3. 更新 Build Command 和 Output Directory
4. 重新部署

## 快速检查清单

- [ ] 在 Vercel 中添加了 `jubianai.cn` 域名
- [ ] 在 DNS 提供商处配置了 CNAME 或 A 记录
- [ ] DNS 记录已生效（使用 nslookup 验证）
- [ ] Vercel 显示域名配置正确
- [ ] SSL 证书已自动生成
- [ ] 访问 `https://jubianai.cn` 显示正确的页面
- [ ] 所有功能正常工作

## 联系支持

如果遇到问题：
1. 查看 Vercel 文档：https://vercel.com/docs
2. 检查 Vercel Dashboard 中的错误信息
3. 查看构建和部署日志


