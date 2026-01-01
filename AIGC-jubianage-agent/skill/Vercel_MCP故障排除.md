# Vercel MCP 故障排除指南

## 常见错误

### 错误 1: 包不存在 (404 Not Found)

**错误信息：**
```
npm error 404 Not Found - GET https://registry.npmjs.org/@modelcontextprotocol%2fserver-vercel - Not found
npm error 404  The requested resource '@modelcontextprotocol/server-vercel@*' could not be found
```

**原因：**
- `@modelcontextprotocol/server-vercel` 包在 npm 上不存在
- 包名可能已更改或尚未发布
- 需要使用其他方式配置 Vercel MCP

**解决方案：**

#### 方案 1: 使用社区实现的 Vercel MCP 包 ✅

已找到多个可用的 Vercel MCP 包！推荐使用：

**推荐配置（功能最全面）：**

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": ["-y", "@mistertk/vercel-mcp"],
      "env": {
        "VERCEL_ACCESS_TOKEN": "您的Vercel访问令牌"
      }
    }
  }
}
```

**其他可选包：**
- `@robinson_ai_systems/vercel-mcp` - 50+ 工具
- `vercel-mcp-server` - 基础版本
- `vercel-mcp` - 简单版本

详细说明请参考：[Vercel MCP 解决方案指南](./Vercel_MCP解决方案.md)

#### 方案 2: 检查官方 MCP 服务器列表

1. 访问 [Model Context Protocol 官方仓库](https://github.com/modelcontextprotocol/servers)
2. 查看是否有 Vercel 相关的服务器实现
3. 确认正确的包名和配置方式

#### 方案 3: 暂时禁用 Vercel MCP

如果 Vercel MCP 服务器尚未正式发布，可以暂时从配置中移除：

```json
{
  "mcpServers": {
    // 暂时注释掉或删除 vercel 配置
    // "vercel": { ... }
  }
}
```

### 错误 2: npm 访问令牌过期

**错误信息：**
```
npm notice Access token expired or revoked. Please try logging in again.
```

**原因：**
- npm 访问令牌已过期或被撤销
- npm 配置问题

**解决方案：**

1. **清除 npm 缓存**
   ```bash
   npm cache clean --force
   ```

2. **重新登录 npm（如果需要）**
   ```bash
   npm login
   ```

3. **检查 npm 配置**
   ```bash
   npm config list
   ```

4. **如果使用私有 npm registry，检查配置**
   ```bash
   npm config get registry
   ```

### 错误 3: JSON 解析错误

**错误信息：**
```
Client error for command Unexpected token 'M', "Microsoft "... is not valid JSON
Client error for command Unexpected token '(', "(c) Micros"... is not valid JSON
```

**原因：**
- Windows 系统输出干扰了 JSON 解析
- 命令执行时输出了非 JSON 格式的文本

**解决方案：**

1. **确保使用 stdio 连接类型**
   ```json
   {
     "mcpServers": {
       "vercel": {
         "command": "npx",
         "args": ["-y", "正确的包名"],
         "env": {
           "VERCEL_ACCESS_TOKEN": "您的令牌"
         }
       }
     }
   }
   ```

2. **检查命令是否正确执行**
   - 手动运行 `npx -y 包名` 查看输出
   - 确认没有错误信息

### 错误 4: 请求超时

**错误信息：**
```
Failed to reload client: MCP error -32001: Request timed out
```

**原因：**
- 服务器启动时间过长
- 网络连接问题
- 包下载失败

**解决方案：**

1. **增加超时时间**（如果配置支持）
2. **检查网络连接**
3. **手动安装包**
   ```bash
   npm install -g 包名
   ```

## 验证 Vercel MCP 是否可用

### 方法 1: 检查 npm 包是否存在

```bash
npm view @modelcontextprotocol/server-vercel
```

如果返回 404，说明包不存在。

### 方法 2: 搜索替代方案

1. 访问 [npmjs.com](https://www.npmjs.com)
2. 搜索 "vercel mcp" 或 "vercel model context protocol"
3. 查看是否有可用的包

### 方法 3: 查看官方文档

1. 访问 [Vercel 官方文档](https://vercel.com/docs)
2. 搜索 "MCP" 或 "Model Context Protocol"
3. 查看是否有官方支持

## 当前状态

根据错误日志，`@modelcontextprotocol/server-vercel` 包在 npm 上不存在。可能的原因：

1. **包尚未发布**：Vercel MCP 服务器可能还在开发中
2. **包名已更改**：可能使用了不同的包名
3. **需要其他配置方式**：可能需要通过其他方式集成 Vercel

## 建议

1. **暂时禁用 Vercel MCP**：如果不需要立即使用，可以暂时从配置中移除
2. **关注官方更新**：关注 Model Context Protocol 和 Vercel 的官方更新
3. **使用其他 MCP 服务器**：如果只需要部署功能，可以考虑其他 MCP 服务器

## 相关资源

- [Model Context Protocol 官方仓库](https://github.com/modelcontextprotocol/servers)
- [Vercel 官方文档](https://vercel.com/docs)
- [npm 包搜索](https://www.npmjs.com/search?q=vercel+mcp)

## 更新配置示例

如果找到了正确的包名，使用以下配置：

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": ["-y", "正确的包名"],
      "env": {
        "VERCEL_ACCESS_TOKEN": "您的Vercel访问令牌"
      }
    }
  }
}
```

**重要提示：**
- 将 `正确的包名` 替换为实际存在的 npm 包名
- 确保 `VERCEL_ACCESS_TOKEN` 是有效的 Vercel 访问令牌
- 配置后重启 Cursor

