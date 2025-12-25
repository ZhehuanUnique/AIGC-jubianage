# 免费额度耗尽解决方案

## 🔍 确认是哪个服务的额度耗尽

### 可能的情况：

1. **即梦 API（火山引擎）免费额度耗尽** ⚠️ 最可能
2. **Render 免费额度耗尽**
3. **Supabase 免费额度耗尽**

## 📋 解决方案

### 情况 1: 即梦 API 免费额度耗尽

#### 检查额度

1. 登录 [火山引擎控制台](https://console.volcengine.com/)
2. 进入 **费用中心** → **账单管理**
3. 查看 **即梦 API** 的使用情况和剩余额度

#### 解决方案

**选项 A: 充值（推荐）**
1. 进入 **费用中心** → **充值**
2. 充值一定金额（如 100 元）
3. 继续使用即梦 API 服务

**选项 B: 等待额度重置**
- 某些免费额度可能按月重置
- 查看额度重置时间

**选项 C: 升级到付费套餐**
1. 进入 **产品与服务** → **视觉智能（Visual）**
2. 查看付费套餐详情
3. 选择合适的套餐

**选项 D: 使用其他视频生成 API**
- 考虑集成其他视频生成服务
- 如：Runway、Pika、Stable Video Diffusion 等

### 情况 2: Render 免费额度耗尽

#### 检查额度

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. 查看 **Billing** 页面
3. 检查免费额度使用情况

#### 解决方案

**选项 A: 升级到付费计划**
1. 在 Render Dashboard 中点击 **Upgrade**
2. 选择适合的计划（Starter $7/月 起）
3. 付费后继续使用

**选项 B: 迁移到其他平台**
- **Railway**: 提供 $5 免费额度/月，按量付费
- **Fly.io**: 提供免费额度
- **Heroku**: 提供 Eco Dyno（$5/月）
- **Vercel**: 如果只部署前端，有免费额度

**选项 C: 使用自己的服务器**
- 在 VPS（如阿里云、腾讯云）上部署
- 使用 Docker 容器化部署

### 情况 3: Supabase 免费额度耗尽

#### 检查额度

1. 登录 [Supabase Dashboard](https://supabase.com/dashboard)
2. 进入项目 → **Settings** → **Usage**
3. 查看数据库、存储等使用情况

#### 解决方案

**选项 A: 升级到 Pro 计划**
- Supabase Pro: $25/月
- 包含更多数据库空间和 API 请求

**选项 B: 迁移到其他数据库**
- **Railway PostgreSQL**: 提供免费数据库
- **Neon**: 提供免费 PostgreSQL
- **PlanetScale**: MySQL 免费额度

**选项 C: 使用本地数据库**
- 如果不需要云数据库，可以使用本地 PostgreSQL

## 🎯 推荐方案（按优先级）

### 如果即梦 API 额度耗尽：

1. **短期方案**: 充值少量金额继续使用
2. **长期方案**: 考虑集成多个视频生成 API，分散风险
3. **替代方案**: 研究其他视频生成服务

### 如果 Render 额度耗尽：

1. **推荐**: 迁移到 Railway（按量付费，更灵活）
2. **备选**: 使用自己的 VPS 服务器
3. **临时**: 升级 Render 到 Starter 计划

### 如果 Supabase 额度耗尽：

1. **推荐**: 迁移到 Railway PostgreSQL（免费）
2. **备选**: 使用 Neon 或 PlanetScale
3. **临时**: 升级 Supabase Pro

## 💡 成本优化建议

### 1. 使用多个服务分散风险

- 视频生成：即梦 API + 备用 API
- 部署：Render + Railway（备用）
- 数据库：Supabase + Neon（备用）

### 2. 优化资源使用

- 减少不必要的 API 调用
- 使用缓存减少数据库查询
- 优化视频生成参数，减少处理时间

### 3. 监控使用情况

- 设置使用量告警
- 定期检查额度使用情况
- 提前规划升级或迁移

## 📝 迁移指南

### 从 Render 迁移到 Railway

1. **创建 Railway 项目**
   - 访问 https://railway.app
   - 连接 GitHub 仓库

2. **配置环境变量**
   - 复制 Render 上的所有环境变量
   - 在 Railway 中设置相同的环境变量

3. **部署**
   - Railway 会自动检测并部署
   - 更新域名指向 Railway 的 URL

### 从 Supabase 迁移到 Railway PostgreSQL

1. **导出数据**
   ```sql
   pg_dump -h db.xxxxx.supabase.co -U postgres -d postgres > backup.sql
   ```

2. **创建 Railway PostgreSQL**
   - 在 Railway 中创建 PostgreSQL 服务
   - 获取连接字符串

3. **导入数据**
   ```sql
   psql -h railway-postgres-host -U postgres -d postgres < backup.sql
   ```

4. **更新环境变量**
   - 更新 `SUPABASE_DB_URL` 为 Railway PostgreSQL 连接字符串

## 🔗 相关资源

- [火山引擎定价](https://www.volcengine.com/pricing)
- [Render 定价](https://render.com/pricing)
- [Railway 定价](https://railway.app/pricing)
- [Supabase 定价](https://supabase.com/pricing)

## ⚠️ 重要提示

1. **备份数据**: 在迁移前务必备份所有数据
2. **测试环境**: 先在测试环境验证迁移
3. **监控**: 迁移后密切监控服务状态
4. **文档**: 更新部署文档和环境变量配置


