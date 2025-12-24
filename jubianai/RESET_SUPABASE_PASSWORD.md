# Supabase 数据库密码重置指南

## 🔑 如果忘记了数据库密码

### 方法 1: 重置数据库密码（推荐）

1. **登录 Supabase Dashboard**
   - 访问 https://supabase.com/dashboard
   - 登录你的账号

2. **进入项目设置**
   - 选择你的项目（如 `jubianai`）
   - 点击左侧菜单的 **"Settings"** ⚙️
   - 选择 **"Database"**

3. **重置密码**
   - 在 Database Settings 页面中，找到 **"Database Password"** 部分
   - 点击 **"Reset Database Password"** 或 **"Change Database Password"** 按钮
   - 输入新密码（**务必记住这个新密码！**）
   - 确认新密码
   - 点击 **"Save"** 或 **"Update Password"**

4. **更新连接字符串**
   - 重置密码后，连接字符串中的 `[YOUR-PASSWORD]` 需要替换为**新密码**
   - 格式：`postgresql://postgres:新密码@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres`

### 方法 2: 查看项目创建时的邮件

如果你在创建 Supabase 项目时收到了确认邮件，密码可能包含在邮件中。检查你的邮箱。

### 方法 3: 使用 Supabase CLI（高级）

如果你安装了 Supabase CLI，可以通过命令行重置密码：

```bash
supabase db reset
```

## ⚠️ 重要提示

### 密码特殊字符处理

如果新密码包含特殊字符（如 `@`, `#`, `%`, `&`, `=` 等），需要进行 **URL 编码**：

| 字符 | URL 编码 |
|------|----------|
| `@`  | `%40`    |
| `#`  | `%23`    |
| `%`  | `%25`    |
| `&`  | `%26`    |
| `=`  | `%3D`    |
| `+`  | `%2B`    |
| ` `  | `%20`    |

**示例**：
- 原始密码：`My@Password#123`
- URL 编码后：`My%40Password%23123`
- 完整连接字符串：`postgresql://postgres:My%40Password%23123@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres`

### 在线 URL 编码工具

可以使用以下工具进行 URL 编码：
- https://www.urlencoder.org/
- https://www.url-encode-decode.com/

### Python 编码示例

```python
from urllib.parse import quote

password = "My@Password#123"
encoded_password = quote(password)
print(encoded_password)  # 输出: My%40Password%23123
```

## 📋 配置步骤（使用新密码）

### 1. 获取连接字符串

根据你提供的 Supabase 信息：
```
postgresql://postgres:[YOUR-PASSWORD]@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres
```

### 2. 替换密码

将 `[YOUR-PASSWORD]` 替换为你的实际密码（如果包含特殊字符，先进行 URL 编码）。

**示例**（假设密码是 `mypassword123`）：
```
postgresql://postgres:mypassword123@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres
```

### 3. 在 Render 中配置

1. 打开 Render Dashboard: https://dashboard.render.com
2. 进入 `jubianai-backend` 服务
3. 点击左侧菜单的 **"Environment"**
4. 点击 **"Add Environment Variable"** 或编辑现有变量
5. 添加/更新环境变量：
   - **Key**: `SUPABASE_DB_URL`
   - **Value**: `postgresql://postgres:你的密码@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres`
6. 点击 **"Save Changes"**

### 4. 重新部署

1. 在 Render Dashboard 中，点击 **"Manual Deploy"** → **"Deploy latest commit"**
2. 等待部署完成
3. 查看日志，应该不再有数据库警告

## ✅ 验证配置

部署完成后，检查日志应该看到：
```
✅ 数据库连接成功
```

而不是：
```
❌ 警告: SUPABASE_DB_URL 未设置，数据库功能将不可用
```

## 🆘 如果重置密码后仍然无法连接

1. **检查密码是否正确**
   - 确认没有多余空格
   - 确认特殊字符已正确编码

2. **测试连接**
   - 可以使用 PostgreSQL 客户端（如 pgAdmin、DBeaver）测试连接
   - 或使用 Python 脚本测试：
   ```python
   import os
   from sqlalchemy import create_engine
   
   db_url = "postgresql://postgres:你的密码@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres"
   try:
       engine = create_engine(db_url)
       conn = engine.connect()
       print("✅ 连接成功！")
       conn.close()
   except Exception as e:
       print(f"❌ 连接失败: {e}")
   ```

3. **检查 Supabase 项目状态**
   - 确认项目已完全创建完成
   - 检查项目是否暂停或过期

## 💡 建议

为了避免将来忘记密码：
1. **使用密码管理器**（如 1Password、LastPass、Bitwarden）保存密码
2. **记录在安全的地方**（不要提交到 Git）
3. **使用简单但安全的密码**（避免特殊字符，减少编码麻烦）

