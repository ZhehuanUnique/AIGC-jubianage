# 检查 Render 日志中的数据库信息

## 🔍 需要查找的日志信息

在 Render Dashboard 的服务日志中，查找以下关键信息：

### 1. 服务启动时的数据库日志

查找以下消息（通常在服务启动时显示）：

**如果数据库未配置：**
```
警告: SUPABASE_DB_URL 未设置，数据库功能将不可用
历史记录功能需要配置数据库，请参考 SUPABASE_SETUP.md
```

**如果数据库已配置但连接失败：**
```
警告: 数据库连接失败: [错误信息]
后端将在没有数据库的情况下运行，历史记录功能将不可用
```

**如果数据库连接成功：**
- 通常不会有特殊日志（静默成功）

### 2. 视频生成时的数据库日志

当提交视频生成任务时，查找以下消息：

**如果保存成功：**
```
✅ 视频生成记录已保存: task_id=8723801727334442544, user_id=1
```

**如果数据库未配置：**
```
⚠️ 数据库未配置，跳过保存历史记录（SUPABASE_DB_URL 未设置）
```

**如果保存失败：**
```
❌ 保存视频生成记录失败: [错误信息]
```

## 📋 检查步骤

### 步骤 1: 查看服务启动日志

1. 访问 Render Dashboard
2. 进入你的服务（jubianai-backend）
3. 查看 "Logs" 标签
4. 查找服务启动时的日志（通常在部署后）
5. 查找数据库相关的警告或错误信息

### 步骤 2: 提交一个测试视频

1. 在网站上提交一个视频生成任务
2. 立即查看 Render 日志
3. 查找视频生成相关的日志
4. 确认是否有保存记录的消息

### 步骤 3: 检查环境变量

1. 在 Render Dashboard 中
2. 进入你的服务
3. 查看 "Environment" 标签
4. 确认是否有 `SUPABASE_DB_URL` 环境变量
5. 如果有，确认值是否正确

## 🛠️ 解决方案

### 如果看到 "SUPABASE_DB_URL 未设置"

**需要配置数据库：**

1. **创建 Supabase 项目**（如果还没有）
   - 访问 https://supabase.com
   - 创建新项目

2. **获取数据库连接字符串**
   - 在 Supabase Dashboard 中
   - Settings → Database
   - 复制 Connection String
   - 格式：`postgresql://postgres:[PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres`

3. **在 Render 中设置环境变量**
   - Render Dashboard → 你的服务 → Environment
   - 添加环境变量：
     - Key: `SUPABASE_DB_URL`
     - Value: 你的连接字符串

4. **初始化数据库表**
   - 在 Supabase Dashboard 中
   - SQL Editor
   - 运行 `jubianai/supabase_init.sql` 中的 SQL

5. **重启服务**
   - 在 Render Dashboard 中手动重启服务

### 如果看到 "保存视频生成记录失败"

**检查错误信息：**
- 表不存在：需要运行 `supabase_init.sql`
- 连接失败：检查连接字符串是否正确
- 权限问题：检查数据库用户权限

## 📝 快速检查命令

在 Render 日志中搜索以下关键词：
- `SUPABASE_DB_URL`
- `数据库`
- `视频生成记录已保存`
- `保存视频生成记录失败`


