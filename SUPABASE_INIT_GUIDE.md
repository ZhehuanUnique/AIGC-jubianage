# Supabase 数据库初始化与阿里云 OSS 配置完整指南

## 📋 第一部分：在 Supabase 中执行初始化 SQL

### 步骤 1: 打开 SQL Editor

1. **登录 Supabase Dashboard**
   - 访问 https://supabase.com/dashboard
   - 选择你的项目

2. **进入 SQL Editor**
   - 点击左侧菜单的 **"SQL Editor"**（📝 图标）
   - 或直接访问：`https://app.supabase.com/project/[PROJECT-REF]/sql`

### 步骤 2: 执行初始化脚本

1. **创建新查询**
   - 在 SQL Editor 页面，点击 **"New query"** 按钮（右上角）

2. **复制 SQL 代码**
   - 打开项目中的 `jubianai/supabase_init.sql` 文件
   - 复制**所有内容**（Ctrl+A, Ctrl+C）

3. **粘贴到 SQL Editor**
   - 在 SQL Editor 的编辑区域粘贴代码
   - 你会看到完整的 SQL 脚本，包括：
     - 创建 `users` 表
     - 创建 `video_generations` 表
     - 创建 `assets` 表
     - 创建 `knowledge_base` 表
     - 创建索引
     - 插入默认用户

4. **执行 SQL**
   - 点击右上角的 **"Run"** 按钮（或按 `Ctrl+Enter`）
   - 等待执行完成（通常几秒钟）

5. **验证执行结果**
   - 如果成功，你会看到 "Success. No rows returned" 或类似的成功消息
   - 如果失败，会显示错误信息，需要检查并修复

### 步骤 3: 验证表创建

1. **进入 Table Editor**
   - 点击左侧菜单的 **"Table Editor"**（📊 图标）

2. **检查表**
   - 在左侧表列表中，应该能看到以下表：
     - ✅ `users` - 用户表
     - ✅ `video_generations` - 视频生成历史表
     - ✅ `assets` - 资产管理表（可选）
     - ✅ `knowledge_base` - 知识库表（可选）

3. **检查表结构**
   - 点击表名，查看表的列和结构
   - 确认所有字段都已创建

### 步骤 4: 验证默认用户

1. **查看 users 表**
   - 在 Table Editor 中，选择 `users` 表
   - 应该能看到一个默认用户：
     - `username`: `default_user`
     - `api_key`: `default_key`
     - `is_active`: `true`

## 📋 第二部分：配置阿里云 OSS 对象存储

### 步骤 1: 创建阿里云 OSS Bucket

1. **登录阿里云控制台**
   - 访问 https://ecs.console.aliyun.com
   - 使用你的阿里云账号登录

2. **进入对象存储 OSS**
   - 在控制台首页，搜索 "对象存储 OSS"
   - 或直接访问：https://oss.console.aliyun.com

3. **创建 Bucket**
   - 点击 **"创建 Bucket"** 按钮
   - 填写配置：
     - **Bucket 名称**: 例如 `jubianai-videos`（必须全局唯一）
     - **地域**: 选择离你最近的区域（如：华东1（杭州））
     - **存储类型**: 选择 **标准存储**
     - **读写权限**: 选择 **私有**（推荐）或 **公共读**
     - **服务端加密**: 可选，建议启用
   - 点击 **"确定"** 创建

4. **记录 Bucket 信息**
   - **Bucket 名称**: 例如 `jubianai-videos`
   - **地域（Region）**: 例如 `oss-cn-hangzhou`
   - **Endpoint**: 例如 `oss-cn-hangzhou.aliyuncs.com`

### 步骤 2: 创建 AccessKey

1. **进入 AccessKey 管理**
   - 在阿里云控制台，点击右上角头像
   - 选择 **"AccessKey 管理"**
   - 或直接访问：https://ram.console.aliyun.com/manage/ak

2. **创建 AccessKey**
   - 点击 **"创建 AccessKey"**
   - 按照提示完成身份验证（可能需要手机验证码）
   - 创建成功后，会显示：
     - **AccessKey ID**: 例如 `LTAI5txxxxxxxxxxxxx`
     - **AccessKey Secret**: 例如 `xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **重要**: 立即复制并保存这两个值，Secret 只显示一次！

3. **保存 AccessKey**
   - 将 AccessKey ID 和 Secret 保存到安全的地方
   - 不要泄露给他人

### 步骤 3: 配置 Bucket 权限（可选）

1. **设置 CORS（如果需要）**
   - 在 OSS 控制台，选择你的 Bucket
   - 点击 **"数据安全"** → **"跨域设置"**
   - 添加规则：
     - **来源**: `*` 或你的域名
     - **允许 Methods**: `GET`, `PUT`, `POST`, `DELETE`
     - **允许 Headers**: `*`
     - **暴露 Headers**: `ETag`, `x-oss-request-id`
     - **缓存时间**: `3600`

2. **设置生命周期规则（可选）**
   - 可以设置自动删除旧文件
   - 或转换存储类型以节省成本

### 步骤 4: 配置 CDN（可选，推荐）

1. **开通 CDN 服务**
   - 在阿里云控制台，搜索 "CDN"
   - 或访问：https://cdn.console.aliyun.com

2. **添加域名**
   - 点击 **"添加域名"**
   - 填写配置：
     - **加速域名**: 例如 `videos.jubianai.cn`
     - **业务类型**: 选择 **全站加速**
     - **源站信息**: 选择 **OSS 域名**
     - **OSS Bucket**: 选择你创建的 Bucket
   - 点击 **"确定"**

3. **配置 DNS**
   - 按照提示配置 DNS 解析
   - 添加 CNAME 记录指向 CDN 域名

4. **记录 CDN 域名**
   - 记录你的 CDN 域名，例如：`videos.jubianai.cn`

### 步骤 5: 在 Render 中配置环境变量

1. **登录 Render Dashboard**
   - 访问 https://dashboard.render.com
   - 选择你的后端项目

2. **进入环境变量设置**
   - 在项目页面，点击左侧菜单 **"Environment"**
   - 或点击顶部菜单 **"Environment"**

3. **添加环境变量**

   添加以下环境变量：

   ```bash
   # 对象存储类型
   STORAGE_TYPE=aliyun_oss
   
   # 阿里云 OSS AccessKey
   ALIYUN_OSS_ACCESS_KEY_ID=LTAI5txxxxxxxxxxxxx
   ALIYUN_OSS_ACCESS_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
   # OSS Bucket 配置
   ALIYUN_OSS_BUCKET_NAME=jubianai-videos
   ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
   
   # CDN 域名（如果配置了 CDN）
   ALIYUN_OSS_BUCKET_DOMAIN=videos.jubianai.cn
   ```

4. **添加每个环境变量**
   - 点击 **"Add Environment Variable"**
   - 输入 Key 和 Value
   - 选择 Environment（Production/Preview/Development）
   - 点击 **"Save"**

5. **重新部署**
   - 环境变量添加后，Render 会自动重新部署
   - 或手动点击 **"Manual Deploy"** → **"Deploy latest commit"**

## 📋 第三部分：验证配置

### 验证数据库

1. **在 Supabase 中测试**
   - 在 Table Editor 中，尝试插入一条测试数据
   - 或通过 API 测试

2. **通过后端 API 测试**
   - 访问：`https://jubianai-backend.onrender.com/health`
   - 应该返回 `{"status": "healthy"}`

### 验证对象存储

1. **生成一个视频**
   - 在前端生成一个视频
   - 等待视频生成完成

2. **检查 OSS**
   - 在阿里云 OSS 控制台
   - 进入你的 Bucket
   - 查看 `videos/` 目录
   - 应该能看到上传的视频文件

3. **检查数据库**
   - 在 Supabase Table Editor 中
   - 查看 `video_generations` 表
   - 确认 `video_url` 字段包含 OSS URL

## 🔍 常见问题

### 问题 1: SQL 执行失败

**错误**: "relation already exists"

**解决**: 
- 表已存在，可以删除后重新创建
- 或使用 `CREATE TABLE IF NOT EXISTS`（脚本中已包含）

**错误**: "syntax error"

**解决**:
- 检查 SQL 语法
- 确保复制了完整的脚本
- 检查是否有特殊字符问题

### 问题 2: OSS 上传失败

**错误**: "AccessDenied"

**解决**:
- 检查 AccessKey ID 和 Secret 是否正确
- 确认 AccessKey 有 OSS 的读写权限
- 检查 Bucket 名称和 Endpoint 是否正确

**错误**: "Bucket not found"

**解决**:
- 确认 Bucket 名称正确
- 确认 Endpoint 对应的区域正确
- 检查 Bucket 是否存在

### 问题 3: 视频 URL 不正确

**问题**: 视频 URL 不是 OSS 地址

**解决**:
- 检查环境变量是否已正确配置
- 确认后端已重新部署
- 查看后端日志，检查是否有错误

## 📝 配置检查清单

### Supabase 数据库
- [ ] 已执行 `supabase_init.sql` 脚本
- [ ] 已创建所有表（users, video_generations, assets, knowledge_base）
- [ ] 已创建默认用户
- [ ] 已配置 `SUPABASE_DB_URL` 环境变量

### 阿里云 OSS
- [ ] 已创建 OSS Bucket
- [ ] 已创建 AccessKey
- [ ] 已配置所有环境变量（STORAGE_TYPE, ALIYUN_OSS_*）
- [ ] 已测试上传功能（可选）
- [ ] 已配置 CDN（可选）

### 后端部署
- [ ] 环境变量已添加到 Render
- [ ] 后端已重新部署
- [ ] 健康检查通过
- [ ] 可以生成视频并保存到数据库

## 🎯 下一步

配置完成后：

1. **测试视频生成**
   - 在前端生成一个视频
   - 检查是否保存到数据库
   - 检查是否上传到 OSS

2. **查看历史记录**
   - 在前端查看历史视频列表
   - 确认视频可以正常播放

3. **测试下载功能**
   - 点击下载按钮
   - 确认可以从 OSS 下载视频

## 💡 提示

- **安全性**: 不要将 AccessKey Secret 提交到代码仓库
- **成本优化**: 可以设置 OSS 生命周期规则，自动删除旧文件
- **CDN 加速**: 配置 CDN 可以显著提升视频加载速度
- **监控**: 在阿里云控制台监控 OSS 的使用量和费用

配置完成后，你的视频生成平台就可以自动保存历史记录并上传到对象存储了！

