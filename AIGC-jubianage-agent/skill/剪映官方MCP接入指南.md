# 剪映官方 MCP 接入指南

## 当前状态

根据错误日志，`@volcengine/vevod-mcp` 包在 npm 上不存在（404 错误）。

## 可能的原因

1. **包尚未发布**：火山引擎可能还在开发中，尚未发布到 npm
2. **包名不同**：可能使用了不同的包名
3. **私有包**：可能需要特殊权限或认证才能访问

## 配置模板

如果包可用，使用以下配置：

```json
{
  "mcpServers": {
    "vevod": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@volcengine/vevod-mcp"
      ],
      "env": {
        "VOLC_ACCESS_KEY_ID": "您的AccessKeyId",
        "VOLC_SECRET_ACCESS_KEY": "您的SecretAccessKey",
        "VOLC_REGION": "cn-north-1"
      }
    }
  }
}
```

## 获取火山引擎密钥

### 步骤 1: 登录火山引擎控制台

1. 访问 [火山引擎控制台](https://console.volcengine.com)
2. 使用您的账号登录

### 步骤 2: 进入访问密钥管理

1. 点击右上角头像
2. 选择 **访问密钥** 或 **Access Key 管理**
3. 或直接访问 [访问密钥管理](https://console.volcengine.com/iam/keymanage/)

### 步骤 3: 创建或查看密钥

1. 如果已有密钥，直接查看并复制
2. 如果没有，点击 **创建密钥** 或 **新建密钥**
3. 系统会生成：
   - **AccessKeyId**：类似 `AKLT_EXAMPLE_32_CHARACTERS_LONG`
   - **SecretAccessKey**：类似 `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
4. **重要**：SecretAccessKey 只会显示一次，请立即保存

### 步骤 4: 获取地域（Region）

根据您的服务所在区域选择：

- `cn-north-1` - 华北（北京）
- `cn-north-2` - 华北（张家口）
- `cn-south-1` - 华南（广州）
- `ap-southeast-1` - 亚太（新加坡）

## 验证包是否存在

### 方法 1: 使用 npm 命令

```bash
npm view @volcengine/vevod-mcp
```

如果返回 404，说明包不存在。

### 方法 2: 检查官方文档

1. 访问 [火山引擎开发者文档](https://www.volcengine.com/docs)
2. 搜索 "MCP" 或 "Model Context Protocol"
3. 查看是否有相关文档

### 方法 3: 联系支持

1. 访问 [火山引擎支持中心](https://www.volcengine.com/support)
2. 咨询是否有 VEVOD MCP 服务器包
3. 或询问正确的包名和安装方式

## 替代方案

如果官方 MCP 包不可用，可以：

### 方案 1: 继续使用 UI 自动化

当前项目已实现剪映 UI 自动化，可以继续使用：
- 自动打开剪映
- 自动点击"开始创作"
- 自动导入视频

相关文件：
- `server/services/jianyingUIAutomationV2.py`
- `server/services/jianyingAssistantService.js`

### 方案 2: 等待官方发布

关注火山引擎的更新，等待官方发布 MCP 服务器包。

### 方案 3: 使用其他视频编辑器 MCP

如果其他视频编辑器提供了 MCP 支持，可以考虑使用。

## 配置后的步骤

1. **保存 `.cursor/mcp.json`**
2. **重启 Cursor**
3. **检查 MCP 状态**：
   - 如果包可用，应该显示为绿色（运行中）
   - 如果包不可用，会显示错误（404）

## 相关资源

- [火山引擎控制台](https://console.volcengine.com)
- [访问密钥管理](https://console.volcengine.com/iam/keymanage/)
- [火山引擎开发者文档](https://www.volcengine.com/docs)
- [MCP 完整配置指南](./MCP完整配置指南.md)

