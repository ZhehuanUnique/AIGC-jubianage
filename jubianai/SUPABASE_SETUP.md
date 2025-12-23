# Supabase 数据库设置指南

## 📋 步骤 1: 创建 Supabase 项目

1. **访问 Supabase**
   - 访问 https://supabase.com
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 填写项目信息：
     - **Name**: jubianai（或你喜欢的名称）
     - **Database Password**: 设置一个强密码（**记住这个密码！**）
     - **Region**: 选择离你最近的区域（如：Southeast Asia (Singapore)）
   - 点击 "Create new project"
   - 等待项目创建完成（通常 2-3 分钟）

## 📋 步骤 2: 获取数据库连接字符串

1. **进入项目设置**
   - 在 Supabase Dashboard 中，点击左侧菜单的 **"Settings"**（齿轮图标 ⚙️）
   - 选择 **"Database"**（数据库）

2. **找到 Connection string 部分**
   - 在 Database Settings 页面中，向下滚动
   - 找到 **"Connection string"** 或 **"Connection pooling"** 部分
   - 这个部分通常在页面的中间或下方位置

3. **获取连接字符串**
   - 在 Connection string 部分，你会看到多个标签页：
     - **URI**（推荐使用）
     - JDBC
     - Golang
     - 等等
   - 点击 **"URI"** 标签
   - 你会看到一个输入框，里面是连接字符串，格式类似：
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
     ```
   - 点击输入框右侧的**复制按钮**（📋 图标）或直接复制文本
   - **重要**: 连接字符串中的 `[YOUR-PASSWORD]` 需要替换为你创建项目时设置的数据库密码

4. **如果找不到 Connection string**
   - 确保你在正确的项目页面
   - 检查是否在 **Settings → Database** 页面
   - 尝试刷新页面
   - 或者查看页面底部的 "Connection info" 部分

3. **设置环境变量**
   - 在 Render Dashboard 或你的部署环境中
   - 添加环境变量：
     ```
     SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
     ```

## 📋 步骤 3: 初始化数据库表

1. **打开 SQL Editor**
   - 在 Supabase Dashboard 中，点击左侧菜单的 **"SQL Editor"**

2. **执行初始化脚本**
   - 打开项目中的 `jubianai/supabase_init.sql` 文件
   - 复制所有 SQL 代码
   - 粘贴到 Supabase SQL Editor 中
   - 点击 **"Run"** 执行

3. **验证表创建**
   - 在左侧菜单选择 **"Table Editor"**
   - 应该能看到以下表：
     - ✅ `users`
     - ✅ `video_generations`
     - ✅ `assets`（可选）
     - ✅ `knowledge_base`（可选）

## 📋 步骤 4: 配置对象存储（阿里云 OSS 或 AWS S3）

### 选项 A: 阿里云 OSS

1. **创建 OSS Bucket**
   - 登录阿里云控制台
   - 进入 **对象存储 OSS**
   - 创建 Bucket（选择区域、读写权限等）

2. **获取 Access Key**
   - 进入 **AccessKey 管理**
   - 创建 AccessKey（或使用现有）
   - 记录 AccessKey ID 和 AccessKey Secret

3. **设置环境变量**
   ```
   STORAGE_TYPE=aliyun_oss
   ALIYUN_OSS_ACCESS_KEY_ID=your_access_key_id
   ALIYUN_OSS_ACCESS_KEY_SECRET=your_access_key_secret
   ALIYUN_OSS_BUCKET_NAME=your_bucket_name
   ALIYUN_OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
   ALIYUN_OSS_BUCKET_DOMAIN=your-cdn-domain.com  # 可选，CDN域名
   ```

### 选项 B: 亚马逊 S3

1. **创建 S3 Bucket**
   - 登录 AWS 控制台
   - 进入 **S3**
   - 创建 Bucket

2. **获取 Access Key**
   - 进入 **IAM** → **Users** → **Security credentials**
   - 创建 Access Key
   - 记录 Access Key ID 和 Secret Access Key

3. **设置环境变量**
   ```
   STORAGE_TYPE=s3
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_S3_BUCKET_NAME=your_bucket_name
   AWS_S3_REGION=us-east-1
   ```

## 📋 步骤 5: 配置后端环境变量

在 Render Dashboard 或你的部署环境中，添加以下环境变量：

```bash
# Supabase 数据库
SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres

# 默认用户 API Key（单用户模式）
DEFAULT_API_KEY=default_key

# 对象存储（二选一）
# 阿里云 OSS
STORAGE_TYPE=aliyun_oss
ALIYUN_OSS_ACCESS_KEY_ID=your_access_key_id
ALIYUN_OSS_ACCESS_KEY_SECRET=your_access_key_secret
ALIYUN_OSS_BUCKET_NAME=your_bucket_name
ALIYUN_OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com

# 或 AWS S3
# STORAGE_TYPE=s3
# AWS_ACCESS_KEY_ID=your_access_key_id
# AWS_SECRET_ACCESS_KEY=your_secret_access_key
# AWS_S3_BUCKET_NAME=your_bucket_name
# AWS_S3_REGION=us-east-1
```

## 📋 步骤 6: 部署和测试

1. **重新部署后端**
   - 推送代码到 GitHub
   - Render 会自动重新部署

2. **测试视频生成**
   - 访问前端页面
   - 生成一个视频
   - 检查是否保存到数据库

3. **查看历史记录**
   - 调用 `/api/v1/video/history` API
   - 或在前端查看历史记录

## 🔍 验证数据库

在 Supabase Dashboard 中：

1. **查看数据**
   - 进入 **"Table Editor"**
   - 选择 `video_generations` 表
   - 应该能看到生成的视频记录

2. **查看用户**
   - 选择 `users` 表
   - 应该能看到默认用户

## 🆘 常见问题

### 问题 1: 连接数据库失败

**解决**:
- 检查 `SUPABASE_DB_URL` 是否正确
- 确认密码是否正确（URL 中的密码需要 URL 编码）
- 检查 Supabase 项目是否已创建完成

### 问题 2: 表不存在

**解决**:
- 确认已执行 `supabase_init.sql` 脚本
- 在 Supabase SQL Editor 中检查表是否存在

### 问题 3: 对象存储上传失败

**解决**:
- 检查对象存储配置是否正确
- 确认 Access Key 有上传权限
- 检查 Bucket 名称和区域是否正确

## 📝 下一步

完成设置后：
1. ✅ 视频生成会自动保存到数据库
2. ✅ 视频会自动上传到对象存储
3. ✅ 可以通过 API 查询历史记录
4. ✅ 前端可以显示历史记录和下载视频

