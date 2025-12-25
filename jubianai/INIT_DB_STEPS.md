# 数据库表初始化步骤

## 🚀 快速开始

### 1. 打开 Supabase SQL Editor

1. 访问 https://supabase.com/dashboard
2. 选择你的项目
3. 点击左侧菜单的 **SQL Editor**
4. 点击 **New Query**

### 2. 运行初始化脚本

1. 打开项目中的 `jubianai/supabase_init.sql` 文件
2. **复制全部内容**
3. 粘贴到 Supabase SQL Editor
4. 点击 **Run** 按钮（或按 `Ctrl+Enter`）

### 3. 确认执行成功

应该看到：
```
Success. No rows returned
```

### 4. 验证表已创建

1. 在 Supabase Dashboard 中
2. 点击左侧菜单的 **Table Editor**
3. 确认看到以下表：
   - `users`
   - `video_generations`
   - `assets`（可选）
   - `knowledge_base`（可选）

### 5. 验证默认用户

1. 在 **Table Editor** 中
2. 选择 `users` 表
3. 应该看到一条记录：
   - `username`: `default_user`
   - `api_key`: `default_key`

### 6. 重启 Render 服务

1. 在 Render Dashboard 中
2. 进入你的服务
3. 点击 **Manual Deploy** → **Deploy latest commit**

## ✅ 完成

初始化完成后，视频生成记录应该能够正常保存了！

## 🧪 测试

生成一个新视频，然后：
1. 检查 Render 日志，应该看到 `✅ 视频生成记录已保存`
2. 刷新历史记录，应该能看到新记录


