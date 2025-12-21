# 数据库设置指南

## PostgreSQL vs MySQL

### 为什么选择 PostgreSQL？

1. **功能更强大**：
   - 支持 JSON/JSONB 数据类型（非常适合存储元数据）
   - 支持全文搜索
   - 支持数组、范围等高级数据类型
   - 更好的并发控制

2. **更适合现代应用**：
   - 更好的 JSON 支持（适合 API 开发）
   - 更强大的查询功能
   - 更好的扩展性

3. **Vercel 集成**：
   - Vercel Postgres 基于 PostgreSQL
   - 无缝集成，自动配置连接
   - 免费层提供 256MB 存储

## 设置步骤

### 1. 在 Vercel 中创建 Postgres 数据库

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 进入你的项目（`jubianai`）
3. 点击 "Storage" 标签
4. 点击 "Create Database"
5. 选择 "Postgres"
6. 选择免费计划（Hobby）
7. 创建数据库

### 2. 配置环境变量

Vercel 会自动创建以下环境变量：
- `POSTGRES_URL` - 数据库连接字符串

你可以在项目设置中查看这些变量。

### 3. 初始化数据库表

有两种方式初始化数据库：

#### 方式 1：通过 API 自动初始化（推荐）

应用启动时会自动创建表（如果不存在）。

#### 方式 2：手动运行初始化脚本

```bash
cd jubianai
python init_db.py
```

### 4. 验证数据库连接

访问 API 健康检查端点：
```
https://jubianai.vercel.app/health
```

访问资产列表端点（应该返回空列表，而不是错误）：
```
https://jubianai.vercel.app/api/v1/assets/list
```

## 数据库表结构

### assets 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| filename | VARCHAR(255) | 原始文件名 |
| character_name | VARCHAR(100) | 人物名称 |
| view_type | VARCHAR(50) | 视图类型（正视图、侧视图等） |
| file_path | VARCHAR(500) | 文件路径或 URL |
| file_url | VARCHAR(500) | 完整文件 URL（如果使用云存储） |
| upload_time | TIMESTAMP | 上传时间 |
| file_size | INTEGER | 文件大小（字节） |
| file_type | VARCHAR(20) | 文件类型（image, video 等） |
| metadata | TEXT | JSON 格式的额外元数据 |

## 本地开发

### 安装 PostgreSQL

**Windows:**
1. 下载 [PostgreSQL for Windows](https://www.postgresql.org/download/windows/)
2. 安装并记住密码

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

### 创建本地数据库

```bash
# 登录 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE jubianai;

# 退出
\q
```

### 配置本地环境变量

创建 `.env` 文件：

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jubianai
```

或者使用 `DATABASE_URL`：

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/jubianai
```

### 运行本地开发

```bash
cd jubianai
python init_db.py  # 初始化数据库表
uvicorn backend.api:app --reload  # 启动 API
```

## 文件存储说明

⚠️ **重要**：在 Vercel Serverless 环境中，文件系统是只读的。

### 当前方案

- **元数据**：存储在 PostgreSQL 数据库中 ✅
- **文件本身**：需要上传到云存储服务

### 推荐的文件存储方案

1. **Vercel Blob Storage**（推荐）
   - 与 Vercel 无缝集成
   - 免费层：256MB 存储
   - 简单易用

2. **AWS S3**
   - 功能强大
   - 按使用量付费
   - 需要额外配置

3. **Cloudinary**
   - 专为图片/视频优化
   - 提供图片处理功能
   - 有免费层

## 下一步

1. ✅ 数据库已集成
2. ⏳ 集成文件存储服务（Vercel Blob Storage 或 S3）
3. ⏳ 更新上传接口，支持文件上传到云存储

## 故障排查

### 数据库连接失败

1. 检查环境变量是否正确设置
2. 检查 Vercel Postgres 是否已创建
3. 查看 Vercel 部署日志

### 表不存在错误

运行初始化脚本：
```bash
python init_db.py
```

### 连接超时

检查数据库连接字符串格式是否正确。

