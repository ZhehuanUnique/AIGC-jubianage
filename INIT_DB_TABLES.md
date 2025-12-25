# 初始化数据库表 - 快速指南

## 🎯 问题确认

根据测试结果：
- ✅ `SUPABASE_DB_URL` 已配置
- ✅ 数据库连接正常（API 正常响应）
- ❌ 视频生成记录未保存
- ⚠️ **最可能的原因：数据库表不存在**

## 🔧 解决方案：初始化数据库表

### 步骤 1: 访问 Supabase Dashboard

1. 访问 https://supabase.com/dashboard
2. 登录并选择你的项目
3. 进入 **SQL Editor**（左侧菜单）

### 步骤 2: 运行初始化脚本

1. 在 SQL Editor 中，点击 **New Query**
2. 复制 `jubianai/supabase_init.sql` 文件的全部内容
3. 粘贴到 SQL Editor
4. 点击 **Run** 或按 `Ctrl+Enter`

### 步骤 3: 验证表是否创建成功

1. 在 Supabase Dashboard 中
2. 进入 **Table Editor**（左侧菜单）
3. 确认以下表已创建：
   - ✅ `users` - 用户表
   - ✅ `video_generations` - 视频生成历史表
   - ✅ `assets` - 资产管理表（可选）
   - ✅ `knowledge_base` - 知识库表（可选）

### 步骤 4: 验证默认用户

1. 在 **Table Editor** 中
2. 选择 `users` 表
3. 确认有一个 `default_user` 记录
4. 如果没有，说明初始化脚本未完全执行

### 步骤 5: 重启 Render 服务

1. 在 Render Dashboard 中
2. 进入你的服务
3. 点击 **Manual Deploy** → **Deploy latest commit**
4. 等待部署完成

## 📋 SQL 脚本位置

SQL 脚本位于：`jubianai/supabase_init.sql`

**重要表结构：**

### users 表
- `id` - 主键
- `username` - 用户名（唯一）
- `api_key` - API 密钥（唯一）
- `is_active` - 是否激活

### video_generations 表
- `id` - 主键
- `task_id` - 任务ID（唯一，即梦 API 返回的）
- `user_id` - 用户ID（外键，关联 users 表）
- `prompt` - 提示词
- `status` - 状态（pending/processing/completed/failed）
- `video_url` - 视频URL
- `created_at` - 创建时间
- `completed_at` - 完成时间

## 🧪 测试

初始化表后，测试：

1. **生成一个新视频**
2. **检查 Render 日志**，应该看到：
   ```
   ✅ 视频生成记录已保存: task_id=xxx, user_id=1
   ```
3. **刷新历史记录**，应该能看到新记录

## ⚠️ 注意事项

1. **外键约束**：`video_generations.user_id` 必须引用 `users.id`
2. **默认用户**：如果 `users` 表中没有 `default_user`，保存会失败
3. **唯一约束**：`task_id` 必须唯一，重复提交会失败

## 🔍 如果仍然失败

如果初始化表后仍然无法保存，检查：

1. **Render 日志**：
   - 查找 `❌ 保存视频生成记录失败`
   - 查看具体错误信息

2. **Supabase 日志**：
   - 在 Supabase Dashboard 中
   - 查看 **Logs** → **Postgres Logs**
   - 查找 INSERT 相关的错误

3. **数据库连接字符串**：
   - 确认 `SUPABASE_DB_URL` 完整且正确
   - 格式：`postgresql://postgres:[PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres`


