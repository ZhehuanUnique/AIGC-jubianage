# Supabase Connection String 位置指南

## 📍 如何找到 Connection String

### 方法 1: 通过 Database Settings（推荐）

1. **登录 Supabase Dashboard**
   - 访问 https://supabase.com/dashboard
   - 选择你的项目

2. **进入 Database Settings**
   - 点击左侧菜单的 **"Settings"**（⚙️ 齿轮图标）
   - 选择 **"Database"**

3. **找到 Connection string**
   - 在 Database Settings 页面中，向下滚动
   - 找到 **"Connection string"** 部分
   - 这个部分通常在：
     - "Database password" 部分下方
     - "Connection pooling configuration" 部分附近
     - 或者页面中间位置

4. **复制连接字符串**
   - 点击 **"URI"** 标签（默认可能显示其他格式）
   - 你会看到类似这样的连接字符串：
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
     ```
   - 点击输入框右侧的**复制按钮**（📋）或手动复制

### 方法 2: 通过 Connection Info

1. **在 Database Settings 页面**
   - 向下滚动到页面底部
   - 找到 **"Connection info"** 或 **"Connection string"** 部分
   - 这里也会显示连接字符串

### 方法 3: 通过 Project Settings

1. **进入 Project Settings**
   - 点击左侧菜单的 **"Settings"**
   - 选择 **"General"** 或 **"Database"**

2. **查找连接信息**
   - 在项目概览中，通常会显示数据库连接信息
   - 或者点击 **"Database"** 标签查看详细连接信息

## 🔑 重要提示

### 密码替换

连接字符串中的 `[YOUR-PASSWORD]` 需要替换为：
- 你创建项目时设置的**数据库密码**
- 如果忘记了密码，可以在 Database Settings 页面点击 **"Reset database password"** 重置

### 连接字符串格式

```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

示例：
```
postgresql://postgres:mypassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

### 使用连接字符串

1. **在环境变量中设置**
   ```bash
   SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

2. **在代码中使用**
   - 确保密码已正确替换
   - 不要在代码中硬编码密码
   - 使用环境变量存储

## 🆘 如果找不到 Connection String

### 可能的原因

1. **页面未完全加载**
   - 刷新页面
   - 等待页面完全加载

2. **权限问题**
   - 确保你是项目的 Owner 或 Admin
   - 检查你的账户权限

3. **项目状态**
   - 确保项目已创建完成
   - 检查项目是否处于活动状态

### 解决方案

1. **直接构建连接字符串**
   - 如果你知道项目信息，可以手动构建：
     ```
     postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
     ```
   - `[PROJECT-REF]` 可以在项目 URL 中找到
   - 例如：`https://app.supabase.com/project/abcdefghijklmnop`
   - 其中 `abcdefghijklmnop` 就是 PROJECT-REF

2. **查看项目概览**
   - 在项目 Dashboard 首页
   - 通常会显示数据库连接信息

3. **联系支持**
   - 如果仍然找不到，可以联系 Supabase 支持

## 📸 页面位置参考

Connection string 通常在以下位置：

```
Database Settings 页面
├── Database password
│   └── Reset database password 按钮
├── Connection pooling configuration
│   ├── Pool Size
│   └── Max Client Connections
└── Connection string  ← 在这里！
    ├── URI 标签（点击这个）
    ├── JDBC 标签
    └── 其他格式标签
```

## ✅ 验证连接字符串

获取连接字符串后，可以使用以下方法验证：

1. **使用 psql 命令行工具**
   ```bash
   psql "postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
   ```

2. **在代码中测试**
   - 使用 SQLAlchemy 或其他数据库工具测试连接
   - 确保连接成功

3. **检查环境变量**
   - 确保 `SUPABASE_DB_URL` 环境变量已正确设置
   - 密码已正确替换

