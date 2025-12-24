# 修复 IPv6 数据库连接问题

## 🔍 问题诊断

错误信息：
```
connection to server at "db.sggdokxjqycskeybyqvv.supabase.co" (2406:da1a:6b0:f614:555:1553:751a:60a3), port 5432 failed: Network is unreachable
```

**问题原因**：
- Supabase 数据库域名解析到了 IPv6 地址
- Render 服务器可能无法访问 IPv6 或网络配置不支持 IPv6
- psycopg2 尝试使用 IPv6 连接失败

## 🔧 解决方案

### 方案 1: 修改 Supabase 连接字符串（推荐）

在 Render Dashboard 中修改 `SUPABASE_DB_URL`：

1. **获取 Supabase 连接信息**
   - 在 Supabase Dashboard 中
   - Settings → Database
   - 查看 Connection String

2. **使用 IPv4 连接池（如果可用）**
   - Supabase 通常提供两种连接方式：
     - Direct connection（直接连接）
     - Connection Pooling（连接池，通常使用 IPv4）

3. **修改连接字符串**
   - 如果使用 Connection Pooling，连接字符串格式：
     ```
     postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
     ```
   - 注意端口是 `6543`（连接池）而不是 `5432`（直接连接）

### 方案 2: 使用 Supabase 连接池

Supabase 提供两种连接方式：

**直接连接（端口 5432）**：
- 可能使用 IPv6
- 连接数有限制

**连接池（端口 6543）**：
- 通常使用 IPv4
- 更好的连接管理
- 推荐用于服务器应用

### 方案 3: 检查 Supabase 网络设置

1. **在 Supabase Dashboard 中**
2. **Settings → Database**
3. **检查 Connection Pooling 设置**
4. **启用 Connection Pooling**（如果未启用）

## 📝 快速修复步骤

### 步骤 1: 获取连接池 URL

1. 访问 Supabase Dashboard
2. Settings → Database
3. 找到 **Connection Pooling** 部分
4. 复制 **Connection String**（使用端口 6543 的那个）

### 步骤 2: 更新 Render 环境变量

1. 在 Render Dashboard 中
2. 进入你的服务
3. Environment 标签
4. 编辑 `SUPABASE_DB_URL`
5. 替换为连接池 URL（端口 6543）
6. 保存

### 步骤 3: 重启服务

1. 在 Render Dashboard 中
2. Manual Deploy → Deploy latest commit

## 🔍 验证修复

修复后，检查 Render 日志：

**如果成功，应该看到：**
```
✅ 数据库连接成功（IPv4）
```

**如果仍然失败，应该看到：**
```
⚠️ 数据库连接测试失败: [错误信息]
```

## 💡 连接字符串格式对比

### 直接连接（可能使用 IPv6）：
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 连接池（通常使用 IPv4）：
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**注意**：
- 连接池 URL 中，用户名格式是 `postgres.[PROJECT-REF]`
- 端口是 `6543` 而不是 `5432`
- 主机名是 `pooler.supabase.com` 而不是 `supabase.co`

## 🚀 推荐方案

**使用 Supabase Connection Pooling**：
1. 更好的连接管理
2. 通常使用 IPv4（避免 IPv6 问题）
3. 适合服务器应用
4. 连接数限制更宽松

