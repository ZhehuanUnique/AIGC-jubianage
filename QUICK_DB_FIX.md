# 快速修复数据库问题

## 🎯 问题确认

根据测试结果：
- ✅ API 正常工作
- ✅ 数据库 API 正常响应（返回空列表）
- ❌ 视频生成时未保存到数据库

## 🔧 快速解决方案

### 方案 1: 检查 Render 环境变量（最快）

1. **访问 Render Dashboard**
   - https://dashboard.render.com
   - 进入你的服务（jubianai-backend）

2. **检查环境变量**
   - 点击 "Environment" 标签
   - 查找 `SUPABASE_DB_URL`
   - 如果不存在，需要添加

3. **如果不存在，添加环境变量：**
   ```
   Key: SUPABASE_DB_URL
   Value: postgresql://postgres:[YOUR-PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres
   ```

4. **重启服务**
   - 在 Render Dashboard 中点击 "Manual Deploy" → "Deploy latest commit"

### 方案 2: 检查数据库表（如果已配置数据库）

1. **访问 Supabase Dashboard**
   - https://supabase.com/dashboard
   - 进入你的项目

2. **检查表是否存在**
   - 进入 "Table Editor"
   - 查找 `video_generations` 表
   - 如果不存在，需要创建

3. **创建表（如果不存在）**
   - 进入 "SQL Editor"
   - 运行 `jubianai/supabase_init.sql` 中的 SQL 脚本

## 📊 测试结果解读

从测试脚本的结果看：
- 任务提交成功：`任务 ID: 8723801727334442544`
- 但记录未保存：`新记录数: 0`

这说明：
1. 视频生成 API 正常工作
2. 但数据库保存步骤被跳过或失败

## 🔍 下一步

请检查 Render 日志，查找：
1. 服务启动时是否有数据库警告
2. 视频生成时是否有保存记录的消息

告诉我日志中看到的内容，我可以帮你进一步诊断。


