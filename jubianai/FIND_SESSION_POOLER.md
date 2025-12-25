# 如何找到 Supabase Session Pooler

## 📍 方法 1: 通过 Database Settings（推荐）

### 步骤：

1. **访问 Supabase Dashboard**
   - https://supabase.com/dashboard
   - 选择你的项目

2. **进入 Database 设置**
   - 左侧菜单 → **Settings**（设置）
   - 点击 **Database**（数据库）

3. **找到 Connection Pooling 部分**
   - 向下滚动页面
   - 找到 **Connection Pooling** 部分
   - 你会看到两个选项：
     - **Session mode**（会话模式）- 推荐
     - **Transaction mode**（事务模式）

4. **复制 Session mode 连接字符串**
   - 点击 **Session mode** 下的 **Copy** 按钮
   - 连接字符串格式：
     ```
     postgresql://postgres.sggdokxjqycskeybyqvv:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
     ```

## 📍 方法 2: 通过连接字符串界面

### 步骤：

1. **打开连接字符串界面**
   - 在 Supabase Dashboard 中
   - 点击右上角的 **Connect** 按钮
   - 或者点击项目设置中的连接相关选项

2. **切换到 Connection Pooling**
   - 在 "Method" 下拉菜单中
   - 选择 **Session Pooler** 或 **Transaction Pooler**
   - （不要选择 "Direct connection"）

3. **复制连接字符串**
   - 复制显示的连接字符串
   - 端口应该是 **6543**（不是 5432）

## 📍 方法 3: 通过 Pooler Settings 按钮

### 步骤：

1. **在连接字符串界面中**
   - 如果看到 "Not IPv4 compatible" 警告框
   - 点击警告框中的 **"Pooler settings"** 按钮
   - 这会直接跳转到 Connection Pooling 设置

## 🔍 如何识别 Session Pooler 连接字符串？

### ✅ Session Pooler 连接字符串特征：

1. **用户名格式**：`postgres.[PROJECT-REF]`
   - 例如：`postgres.sggdokxjqycskeybyqvv`

2. **主机名**：`pooler.supabase.com`
   - 例如：`aws-0-ap-southeast-1.pooler.supabase.com`

3. **端口**：`6543`
   - 不是 `5432`（直接连接使用 5432）

4. **完整格式**：
   ```
   postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

### ❌ Direct Connection 连接字符串特征（不要用这个）：

1. **用户名**：`postgres`（没有项目引用）

2. **主机名**：`db.[PROJECT-REF].supabase.co`
   - 例如：`db.sggdokxjqycskeybyqvv.supabase.co`

3. **端口**：`5432`

## 🎯 快速检查清单

- [ ] 连接字符串中包含 `pooler.supabase.com`
- [ ] 端口是 `6543`（不是 5432）
- [ ] 用户名是 `postgres.[PROJECT-REF]` 格式
- [ ] 不是 `db.[PROJECT-REF].supabase.co` 格式

## 💡 如果找不到 Connection Pooling

如果找不到 Connection Pooling 选项，可能是：

1. **项目版本较旧**：需要升级项目
2. **权限问题**：确认你有项目管理员权限
3. **区域限制**：某些区域可能不支持

**替代方案**：
- 联系 Supabase 支持
- 或购买 IPv4 add-on（不推荐，成本较高）

## 📸 界面位置参考

在 Supabase Dashboard 中，路径通常是：
```
Dashboard → [你的项目] → Settings → Database → Connection Pooling
```

或者：
```
Dashboard → [你的项目] → Connect → Connection String → Method: Session Pooler
```


