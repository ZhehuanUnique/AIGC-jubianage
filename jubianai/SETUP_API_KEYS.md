# 即梦 API 密钥配置指南

## 密钥配置示例

```
Access Key ID: your_access_key_id_here
Secret Access Key: your_secret_access_key_here
```

**注意**: 请使用你自己的实际密钥替换上述占位符。

## 配置步骤

### 方法 1：创建 `.env` 文件（推荐，本地开发）

在 `jubianai/` 目录下创建 `.env` 文件（如果不存在），添加以下内容：

```bash
# 即梦 AI (火山引擎) API 配置
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
```

**注意**：
- `.env` 文件已添加到 `.gitignore`，不会被提交到版本控制
- 确保文件路径为 `jubianai/.env`（不是项目根目录）

### 方法 2：设置系统环境变量（Windows）

在 PowerShell 中运行：

```powershell
# 临时设置（当前会话有效）
$env:VOLCENGINE_ACCESS_KEY_ID="your_access_key_id_here"
$env:VOLCENGINE_SECRET_ACCESS_KEY="your_secret_access_key_here"

# 永久设置（需要管理员权限）
[System.Environment]::SetEnvironmentVariable("VOLCENGINE_ACCESS_KEY_ID", "your_access_key_id_here", "User")
[System.Environment]::SetEnvironmentVariable("VOLCENGINE_SECRET_ACCESS_KEY", "your_secret_access_key_here", "User")
```

### 方法 3：部署平台环境变量

#### Railway
在 Railway Dashboard → 项目设置 → Variables 中添加：
- `VOLCENGINE_ACCESS_KEY_ID` = `your_access_key_id_here`
- `VOLCENGINE_SECRET_ACCESS_KEY` = `your_secret_access_key_here`

#### Render
在 Render Dashboard → Environment Variables 中添加：
- `VOLCENGINE_ACCESS_KEY_ID` = `your_access_key_id_here`
- `VOLCENGINE_SECRET_ACCESS_KEY` = `your_secret_access_key_here`

#### Vercel
在 Vercel Dashboard → Project Settings → Environment Variables 中添加：
- `VOLCENGINE_ACCESS_KEY_ID` = `your_access_key_id_here`
- `VOLCENGINE_SECRET_ACCESS_KEY` = `your_secret_access_key_here`

## 验证配置

### 1. 检查环境变量是否加载

运行以下 Python 脚本验证：

```python
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv('jubianai/.env')

access_key = os.getenv("VOLCENGINE_ACCESS_KEY_ID")
secret_key = os.getenv("VOLCENGINE_SECRET_ACCESS_KEY")

print(f"Access Key ID: {access_key[:20]}..." if access_key else "❌ 未设置")
print(f"Secret Access Key: {secret_key[:20]}..." if secret_key else "❌ 未设置")
```

### 2. 测试 API 调用

重启后端服务后，尝试生成视频，如果之前出现 "Access Denied" 错误，现在应该可以正常工作了。

## 重要提示

1. **Secret Access Key 格式**：
   - 您提供的 Secret Access Key 是 Base64 编码的（以 `==` 结尾）
   - 根据火山引擎 SDK 文档，应该**直接使用**这个 Base64 编码的字符串
   - SDK 会自动处理签名，不需要手动解码

2. **安全性**：
   - 不要将 `.env` 文件提交到 Git
   - 不要在代码中硬编码密钥
   - 定期轮换密钥以提高安全性

3. **重启服务**：
   - 配置环境变量后，需要**重启后端服务**才能生效

## 故障排查

如果仍然出现 "Access Denied" 错误，请检查：

1. ✅ 环境变量名称是否正确（区分大小写）
2. ✅ 密钥值是否正确（无多余空格）
3. ✅ 后端服务是否已重启
4. ✅ API 密钥是否有权限访问即梦 API
5. ✅ 即梦 API 服务是否已开通

详细排查步骤请参考：`jubianai/ACCESS_DENIED_FIX.md`

