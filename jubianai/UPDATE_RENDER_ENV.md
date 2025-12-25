# 更新 Render 环境变量步骤

## ✅ 你已获取的连接字符串

```
postgresql://postgres.sggdokxjqycskeybyqvv:[YOUR-PASSWORD]@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
```

**确认信息**：
- ✅ 主机：`pooler.supabase.com`（正确，这是连接池）
- ✅ 用户名：`postgres.sggdokxjqycskeybyqvv`（正确，包含项目引用）
- ✅ 端口：`5432`（Transaction Pooler 使用此端口）

## 📋 更新步骤

### 步骤 1: 替换密码

1. **获取你的 Supabase 数据库密码**
   - 如果你记得密码，直接使用
   - 如果不记得，需要重置：
     - Supabase Dashboard → Settings → Database
     - 找到 "Database password" 部分
     - 点击 "Reset database password"
     - 复制新密码

2. **替换连接字符串中的 `[YOUR-PASSWORD]`**
   - 将 `[YOUR-PASSWORD]` 替换为你的实际密码
   - 例如：
     ```
     postgresql://postgres.sggdokxjqycskeybyqvv:MyPassword123@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
     ```

### 步骤 2: 更新 Render 环境变量

1. **访问 Render Dashboard**
   - https://dashboard.render.com
   - 登录你的账户

2. **进入你的服务**
   - 找到 `jubianai` 或 `jubianai-backend` 服务
   - 点击进入

3. **编辑环境变量**
   - 点击 **Environment** 标签
   - 找到 `SUPABASE_DB_URL` 环境变量
   - 点击编辑图标（铅笔图标）或直接点击值

4. **更新连接字符串**
   - 删除旧的连接字符串（端口 5432 的直接连接）
   - 粘贴新的连接字符串（已替换密码的完整字符串）
   - 点击 **Save** 保存

### 步骤 3: 重启服务

1. **在 Render Dashboard 中**
2. **点击 Manual Deploy** → **Deploy latest commit**
3. **等待部署完成**（通常 1-2 分钟）

### 步骤 4: 验证连接

部署完成后，检查 Render 日志：

**如果成功，应该看到：**
```
✅ 数据库连接成功
```

**如果失败，检查：**
- 密码是否正确
- 连接字符串是否完整
- 是否有特殊字符需要 URL 编码

## 🔍 验证清单

- [ ] 连接字符串中的 `[YOUR-PASSWORD]` 已替换为实际密码
- [ ] 主机名是 `pooler.supabase.com`（不是 `supabase.co`）
- [ ] 用户名包含项目引用（`postgres.sggdokxjqycskeybyqvv`）
- [ ] Render 环境变量已更新
- [ ] 服务已重新部署
- [ ] 日志显示 "✅ 数据库连接成功"

## 💡 关于端口 5432 vs 6543

- **端口 5432**：Transaction Pooler 使用此端口
- **端口 6543**：Session Pooler 使用此端口

两种都可以解决 IPv6 问题，因为都使用 `pooler.supabase.com` 主机。

## ⚠️ 密码特殊字符处理

如果密码包含特殊字符（如 `@`, `#`, `%`, `&` 等），需要进行 URL 编码：

- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `&` → `%26`
- `/` → `%2F`
- `:` → `%3A`
- `?` → `%3F`
- `=` → `%3D`

或者，最简单的方法是：
1. 在 Supabase 中重置密码
2. 使用只包含字母和数字的简单密码
3. 更新连接字符串

## ✅ 完成

更新后，数据库连接应该成功，视频生成记录应该能正常保存到数据库。


