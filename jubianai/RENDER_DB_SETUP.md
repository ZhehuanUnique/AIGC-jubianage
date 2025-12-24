# Render 数据库配置指南（快速版）

## ⚠️ 重要说明

**数据库是可选的！** 如果不配置数据库：
- ✅ 视频生成功能**仍然可以正常工作**
- ✅ 即梦 API 调用**不受影响**
- ❌ 历史记录功能不可用（无法保存和查询历史视频）

如果你只需要视频生成功能，可以**暂时跳过数据库配置**。

## 📋 快速配置步骤（5 分钟）

### 步骤 1: 创建 Supabase 项目

1. 访问 https://supabase.com
2. 使用 GitHub 账号登录
3. 点击 **"New Project"**
4. 填写信息：
   - **Name**: `jubianai`（或任意名称）
   - **Database Password**: 设置一个强密码（**务必记住！**）
   - **Region**: 选择离你最近的区域（如：Southeast Asia (Singapore)）
5. 点击 **"Create new project"**
6. 等待 2-3 分钟，项目创建完成

### 步骤 2: 获取数据库连接字符串

1. 在 Supabase Dashboard 中，点击左侧 **"Settings"** ⚙️
2. 选择 **"Database"**
3. 向下滚动，找到 **"Connection string"** 部分
4. 点击 **"URI"** 标签
5. 复制连接字符串，格式类似：
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
6. **重要**: 将 `[YOUR-PASSWORD]` 替换为你创建项目时设置的数据库密码

### 步骤 3: 在 Render 中配置环境变量

1. 打开 Render Dashboard: https://dashboard.render.com
2. 进入你的 `jubianai-backend` 服务
3. 点击左侧菜单的 **"Environment"**
4. 点击 **"Add Environment Variable"**
5. 添加以下环境变量：

   **Key**: `SUPABASE_DB_URL`  
   **Value**: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

   （将 `[YOUR-PASSWORD]` 和 `xxxxx` 替换为实际值）

6. 点击 **"Save Changes"**

### 步骤 4: 初始化数据库表

1. 在 Supabase Dashboard 中，点击左侧 **"SQL Editor"**
2. 打开项目中的 `jubianai/supabase_init.sql` 文件
3. 复制所有 SQL 代码
4. 粘贴到 Supabase SQL Editor
5. 点击 **"Run"** 执行

### 步骤 5: 重新部署

1. 在 Render Dashboard 中，点击 **"Manual Deploy"** → **"Deploy latest commit"**
2. 等待部署完成
3. 查看日志，应该不再有数据库警告

## ✅ 验证配置

部署完成后，检查日志应该看到：
```
✅ 数据库连接成功
✅ 数据库表已初始化
```

而不是：
```
❌ 警告: SUPABASE_DB_URL 未设置，数据库功能将不可用
```

## 🔍 测试数据库功能

1. 生成一个视频
2. 调用 API: `GET https://jubianai-backend.onrender.com/api/v1/video/history`
3. 应该能看到刚才生成的视频记录

## 🆘 常见问题

### 问题 1: 连接字符串格式错误

**错误示例**:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

**正确格式**:
```
postgresql://postgres:你的实际密码@db.xxxxx.supabase.co:5432/postgres
```

**注意**: 如果密码包含特殊字符（如 `@`, `#`, `%`），需要进行 URL 编码：
- `@` → `%40`
- `#` → `%23`
- `%` → `%25`

### 问题 2: 找不到 Connection string

**解决**:
- 确保在 **Settings → Database** 页面
- 向下滚动，可能在页面中间或底部
- 尝试刷新页面

### 问题 3: 表不存在错误

**解决**:
- 确认已执行 `supabase_init.sql` 脚本
- 在 Supabase SQL Editor 中检查表是否存在
- 查看 `jubianai/supabase_init.sql` 文件

### 问题 4: 密码包含特殊字符

如果数据库密码包含特殊字符，需要进行 URL 编码：

**Python 编码示例**:
```python
from urllib.parse import quote
password = "your@password#123"
encoded_password = quote(password)
# 结果: "your%40password%23123"
```

**在线工具**: https://www.urlencoder.org/

## 📝 完整配置清单

- [ ] 已创建 Supabase 项目
- [ ] 已获取数据库连接字符串
- [ ] 已在 Render 中设置 `SUPABASE_DB_URL` 环境变量
- [ ] 已执行 `supabase_init.sql` 脚本
- [ ] 已重新部署后端服务
- [ ] 日志中不再有数据库警告
- [ ] 可以成功生成视频并保存到数据库

## 🔗 相关文档

- 完整配置指南: `jubianai/SUPABASE_SETUP.md`
- 数据库架构: `jubianai/DATABASE_ARCHITECTURE.md`
- 初始化 SQL: `jubianai/supabase_init.sql`

