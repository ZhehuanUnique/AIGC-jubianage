# 检查 video_generations 表

## ✅ 已确认

从你的截图看到：
- ✅ `users` 表已存在
- ✅ `default_user` 已创建（id=1, username=default_user, api_key=default_key）
- ⚠️ `video_generations` 表名称被截断，需要确认

## 🔍 需要检查

### 1. 确认 video_generations 表是否存在

在 Supabase Table Editor 中：
1. 查看左侧表列表
2. 确认是否有 `video_generations` 表（名称可能被截断显示为 `video_generati...`）
3. 如果不存在，需要运行初始化脚本

### 2. 检查表结构

如果 `video_generations` 表存在，点击它，确认有以下列：
- `id` - 主键
- `task_id` - 任务ID（唯一）
- `user_id` - 用户ID（外键）
- `prompt` - 提示词
- `status` - 状态
- `video_url` - 视频URL
- `created_at` - 创建时间
- 等等

### 3. 检查表数据

1. 点击 `video_generations` 表
2. 查看是否有任何记录
3. 如果表是空的，这是正常的（如果还没有成功保存过）

## 🛠️ 如果 video_generations 表不存在

### 解决方案：运行初始化脚本

1. **在 Supabase Dashboard 中**
2. **进入 SQL Editor**（左侧菜单）
3. **点击 New Query**
4. **复制 `jubianai/supabase_init.sql` 的全部内容**
5. **粘贴到 SQL Editor**
6. **点击 Run**（或按 `Ctrl+Enter`）

### 验证

运行脚本后：
1. 回到 **Table Editor**
2. 确认 `video_generations` 表已创建
3. 确认表结构正确

## 🧪 测试保存功能

表创建后：

1. **生成一个新视频**
2. **立即检查 Render 日志**，应该看到：
   ```
   ✅ 视频生成记录已保存: task_id=xxx, user_id=1
   ```
3. **在 Supabase Table Editor 中**
   - 打开 `video_generations` 表
   - 应该能看到新记录

## 📝 快速检查清单

- [ ] `users` 表存在 ✅（已确认）
- [ ] `default_user` 存在 ✅（已确认）
- [ ] `video_generations` 表存在 ❓（需要确认）
- [ ] `video_generations` 表结构正确 ❓（需要确认）

## 💡 如果表已存在但仍然无法保存

如果 `video_generations` 表已存在，但仍然无法保存，可能的原因：

1. **外键约束问题**：
   - `user_id` 必须引用 `users.id`
   - 确认 `default_user` 的 id 是 1

2. **唯一约束问题**：
   - `task_id` 必须唯一
   - 如果重复提交相同任务，会失败

3. **权限问题**：
   - 确认数据库用户有 INSERT 权限

4. **连接字符串问题**：
   - 确认 Render 中的 `SUPABASE_DB_URL` 完整且正确


