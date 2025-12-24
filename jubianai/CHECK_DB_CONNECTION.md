# 检查 Supabase 数据库连接状态

## 🔍 从日志判断

从你提供的 Render 日志来看，**没有看到数据库相关的信息**。这意味着：

### 可能的情况：

1. **✅ 数据库已连接（静默成功）**
   - 如果连接成功，代码可能不会打印额外信息
   - 只有在失败时才会打印警告

2. **❌ 数据库未配置**
   - 如果 `SUPABASE_DB_URL` 未设置，应该会看到：
     ```
     警告: SUPABASE_DB_URL 未设置，数据库功能将不可用
     历史记录功能需要配置数据库，请参考 SUPABASE_SETUP.md
     ```

3. **⚠️ 数据库连接失败**
   - 如果连接失败，应该会看到：
     ```
     警告: 数据库连接失败: {错误信息}
     ```

## 🧪 测试数据库连接

### 方法 1: 通过 API 测试（推荐）

访问以下 URL 测试数据库功能：

```bash
# 测试健康检查（应该返回 200）
curl https://jubianai-backend.onrender.com/health

# 测试历史记录 API（如果数据库未配置，会返回 503）
curl https://jubianai-backend.onrender.com/api/v1/video/history
```

**预期结果**：
- **如果数据库已连接**：历史记录 API 应该返回 `[]`（空数组）或视频列表
- **如果数据库未配置**：历史记录 API 会返回 `503 Service Unavailable` 和错误信息

### 方法 2: 检查 Render 环境变量

1. 打开 Render Dashboard: https://dashboard.render.com
2. 进入 `jubianai-backend` 服务
3. 点击左侧菜单的 **"Environment"**
4. 检查是否有 `SUPABASE_DB_URL` 环境变量
5. 如果有，检查值是否正确（格式应该是完整的连接字符串）

### 方法 3: 查看完整启动日志

在 Render Dashboard 中：
1. 进入 `jubianai-backend` 服务
2. 点击 **"Logs"** 标签
3. 查看服务启动时的日志（通常在部署后立即显示）
4. 查找以下关键词：
   - `SUPABASE_DB_URL`
   - `数据库`
   - `database`
   - `警告`
   - `警告:`

## 📋 快速检查清单

- [ ] 在 Render 环境变量中检查 `SUPABASE_DB_URL` 是否存在
- [ ] 测试历史记录 API：`GET /api/v1/video/history`
- [ ] 查看完整的启动日志（不是运行时的健康检查日志）
- [ ] 尝试生成一个视频，看是否能保存到数据库

## 🔧 如果数据库未连接

### 步骤 1: 确认环境变量

在 Render Dashboard → Environment 中，确保有：
```
SUPABASE_DB_URL=postgresql://postgres:你的密码@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres
```

### 步骤 2: 重新部署

1. 在 Render Dashboard 中，点击 **"Manual Deploy"** → **"Deploy latest commit"**
2. 等待部署完成
3. 查看启动日志，应该能看到数据库连接信息

### 步骤 3: 验证连接

使用以下 Python 脚本测试连接（本地运行）：

```python
import os
from sqlalchemy import create_engine, text

# 替换为你的实际连接字符串
db_url = "postgresql://postgres:你的密码@db.sggdokxjqycskeybyqvv.supabase.co:5432/postgres"

try:
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ 数据库连接成功！")
        print(f"查询结果: {result.fetchone()}")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
```

## 💡 当前状态判断

根据你提供的日志：
- ✅ 服务正常运行（健康检查返回 200）
- ❓ 数据库状态未知（需要进一步检查）

**建议操作**：
1. 在 Render Dashboard 中检查环境变量
2. 测试历史记录 API
3. 查看完整的启动日志

