# 腾讯云 COS MCP 故障排除指南

## 常见错误

### 错误 1: JSON 解析错误

**错误信息：**
```
Client error for command Unexpected end of JSON input
Client error for command Unexpected token 'C', "COS配置信息:" is not valid JSON
Client error for command No number after minus sign in JSON
```

**原因：**
- MCP 服务器启动时输出了非 JSON 格式的文本（如中文提示信息）
- 配置参数不正确，导致服务器无法正常启动
- 连接类型可能不匹配

**解决方案：**

#### 方案 1: 使用 stdio 连接类型（推荐）

将 `connectType` 从 `sse` 改为 `stdio`：

```json
{
  "mcpServers": {
    "tencent-cos": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=your-bucket-name-APPID",
        "--SecretId=your-secret-id",
        "--SecretKey=your-secret-key",
        "--DatasetName=your-dataset-name",
        "--connectType=stdio"
      ]
    }
  }
}
```

**注意：** 使用 `stdio` 时，**不要**包含 `--port` 参数。

#### 方案 2: 使用环境变量配置

将敏感信息移到环境变量中，避免参数解析问题：

```json
{
  "mcpServers": {
    "tencent-cos": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=your-bucket-name-APPID",
        "--DatasetName=your-dataset-name",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "your-secret-id",
        "COS_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

#### 方案 3: 使用 JSON 配置方式

使用 `--cos-config` 参数传递 JSON 配置：

```json
{
  "mcpServers": {
    "tencent-cos": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--cos-config",
        "{\"Region\":\"ap-guangzhou\",\"Bucket\":\"your-bucket-name-APPID\",\"SecretId\":\"your-secret-id\",\"SecretKey\":\"your-secret-key\",\"DatasetName\":\"your-dataset-name\"}",
        "--connectType=stdio"
      ]
    }
  }
}
```

### 错误 2: 服务器未找到

**错误信息：**
```
No server info found
Handling ListOfferings action, server stored: false
```

**原因：**
- 服务器启动失败
- 配置参数错误
- 网络连接问题

**解决方案：**

1. **检查包名是否正确**
   - 确认使用 `cos-mcp@latest` 或 `@tencent/cos-mcp`
   - 尝试手动安装：`npm install -g cos-mcp@latest`

2. **验证配置参数**
   - 确保所有必需参数都已提供
   - 检查参数格式是否正确（特别是 `--Region`、`--Bucket`）

3. **检查网络连接**
   - 确保可以访问 npm registry
   - 检查防火墙设置

### 错误 3: 认证失败

**错误信息：**
```
Authentication failed
Invalid SecretId or SecretKey
```

**原因：**
- SecretId 或 SecretKey 错误
- 密钥已过期或被删除
- 密钥权限不足

**解决方案：**

1. **重新获取密钥**
   - 访问 [腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)
   - 创建新的密钥或查看现有密钥

2. **检查密钥格式**
   - SecretId 格式：`YOUR_SECRET_ID_HERE`
   - SecretKey 格式：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **验证权限**
   - 确保密钥有 COS 访问权限
   - 检查存储桶的访问策略

## 推荐配置

### 完整配置示例（使用 stdio）

```json
{
  "mcpServers": {
    "tencent-cos": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=your-bucket-name-APPID",
        "--DatasetName=your-dataset-name",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "COS_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    }
  }
}
```

### 关键配置要点

1. **连接类型**
   - 推荐使用 `stdio`（标准输入输出）
   - 如果必须使用 `sse`，确保端口未被占用

2. **参数格式**
   - 所有参数使用 `--参数名=值` 格式
   - 参数名区分大小写（如 `--Region` 不是 `--region`）

3. **环境变量**
   - 敏感信息（SecretId、SecretKey）使用 `env` 配置
   - 避免在命令行参数中直接暴露密钥

4. **必需参数**
   - `--Region`: COS 地域（如 `ap-guangzhou`）
   - `--Bucket`: 存储桶名称（格式：`bucket-name-APPID`）
   - `--SecretId` 或环境变量 `COS_SECRET_ID`
   - `--SecretKey` 或环境变量 `COS_SECRET_KEY`
   - `--DatasetName`: 数据集名称（用于智能检索）
   - `--connectType`: 连接类型（`stdio` 或 `sse`）

## 验证配置

配置完成后，按以下步骤验证：

1. **保存配置文件**
   - 编辑 `.cursor/mcp.json`
   - 保存更改

2. **重启 Cursor**
   - 完全关闭 Cursor
   - 重新打开 Cursor

3. **检查 MCP 状态**
   - 在 Cursor 设置中查看 MCP 服务器状态
   - 确认 `tencent-cos` 显示为绿色（运行中）

4. **测试功能**
   - 尝试询问 AI："列出 COS 存储桶中的文件"
   - 或："上传文件到 COS"

## 调试步骤

如果问题仍然存在，按以下步骤调试：

1. **手动测试服务器**
   ```bash
   npx -y cos-mcp@latest \
     --Region=ap-guangzhou \
     --Bucket=your-bucket-name-APPID \
     --SecretId=your-secret-id \
     --SecretKey=your-secret-key \
     --DatasetName=your-dataset-name \
     --connectType=stdio
   ```

2. **检查输出**
   - 查看是否有错误信息
   - 确认服务器是否正常启动

3. **查看日志**
   - 在 Cursor 中查看 MCP 服务器日志
   - 检查是否有详细的错误信息

4. **简化配置**
   - 先使用最基本的配置
   - 逐步添加参数，找出问题所在

## 相关资源

- [腾讯云 COS MCP 接入指南](./腾讯云COS_MCP接入指南.md)
- [MCP 令牌获取指南](./MCP令牌获取指南.md)
- [COS MCP Server 官方文档](https://docs.cloudbase.net/en/ai/mcp/develop/server-templates/cloudrun-mcp-cos)

