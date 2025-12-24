# 切换到 Supabase Connection Pooling（解决 IPv6 问题）

## 🎯 问题

当前错误：
```
connection to server at "db.sggdokxjqycskeybyqvv.supabase.co" (2406:da1a:6b0:f614:555:1553:751a:60a3), port 5432 failed: Network is unreachable
```

**原因**：Supabase 直接连接（端口 5432）可能使用 IPv6，但 Render 无法访问。

## ✅ 解决方案：使用 Connection Pooling

Supabase Connection Pooling 使用 IPv4，更适合服务器应用。

## 📋 操作步骤

### 步骤 1: 获取 Connection Pooling URL

1. **访问 Supabase Dashboard**
   - https://supabase.com/dashboard
   - 选择你的项目

2. **进入 Database 设置**
   - 左侧菜单 → **Settings**
   - 点击 **Database**

3. **找到 Connection Pooling**
   - 向下滚动到 **Connection Pooling** 部分
   - 选择 **Session mode**（推荐）或 **Transaction mode**

4. **复制 Connection String**
   - 点击 **Copy** 按钮
   - 格式类似：
     ```
     postgresql://postgres.sggdokxjqycskeybyqvv:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
     ```
   - **注意**：端口是 `6543`（不是 5432）

### 步骤 2: 更新 Render 环境变量

1. **访问 Render Dashboard**
   - https://dashboard.render.com
   - 进入你的服务（jubianai-backend）

2. **编辑环境变量**
   - 点击 **Environment** 标签
   - 找到 `SUPABASE_DB_URL`
   - 点击编辑（铅笔图标）

3. **替换连接字符串**
   - 删除旧的连接字符串
   - 粘贴新的 Connection Pooling URL（端口 6543）
   - 点击 **Save**

### 步骤 3: 重启服务

1. **在 Render Dashboard 中**
2. **点击 Manual Deploy** → **Deploy latest commit**
3. **等待部署完成**

### 步骤 4: 验证连接

部署后，检查 Render 日志：

**如果成功，应该看到：**
```
✅ 数据库连接成功
```

**如果仍然失败，检查：**
- Connection Pooling URL 是否正确
- 密码是否正确
- 端口是否为 6543

## 🔍 Connection Pooling URL 格式

### 直接连接（当前使用，可能有 IPv6 问题）：
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Connection Pooling（推荐，使用 IPv4）：
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**关键区别**：
- 用户名：`postgres.[PROJECT-REF]`（不是 `postgres`）
- 主机：`pooler.supabase.com`（不是 `supabase.co`）
- 端口：`6543`（不是 `5432`）

## 💡 为什么使用 Connection Pooling？

1. **IPv4 支持**：通常使用 IPv4，避免 IPv6 问题
2. **更好的连接管理**：自动管理连接池
3. **更高的连接限制**：适合服务器应用
4. **更稳定**：连接更可靠

## ✅ 完成

切换到 Connection Pooling 后：
- ✅ 数据库连接应该成功
- ✅ 视频生成记录应该能正常保存
- ✅ 历史记录应该能正常显示

