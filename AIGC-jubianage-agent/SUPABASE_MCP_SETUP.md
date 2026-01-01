# Supabase MCP 配置说明

## 概述

MCP (Model Context Protocol) 允许 Cursor AI 助手直接与 Supabase 项目交互，无需手动操作控制台。

**重要提示**：每个项目都有自己独立的 MCP 配置。MCP 配置存储在项目根目录的 `.cursor/mcp.json` 文件中。

## 已配置的功能

当前项目已配置 Supabase MCP，支持以下功能：

### 数据库管理
- ✅ 执行 SQL 迁移
- ✅ 更新 Row Level Security (RLS) 策略
- ✅ 管理存储桶和文件权限
- ✅ 修改 API 配置

### 查询和分析
- ✅ 执行 SQL 查询
- ✅ 查看表数据
- ✅ 分析数据库结构
- ✅ 检查数据关系

## 配置文件位置

```
.cursor/mcp.json
```

## 配置内容（Ref 模式）

**推荐使用 Ref 模式**：为每个项目单独配置，使用 `--project-ref` 参数指定项目ID，这样可以确保每个项目只操作自己的数据库，互不干扰。

```json
{
  "mcpServers": {
    "supabase-jubianage-agent": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref=ogndfzxtzsifaqwzfojs"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_55d3bff12a73fad53040ea5b2db387d0d84a2e03"
      }
    }
  }
}
```

### Ref 模式的优势

1. **项目隔离**：每个项目使用独立的 `--project-ref`，确保只操作指定项目的数据库
2. **安全性**：访问令牌通过环境变量 `SUPABASE_ACCESS_TOKEN` 传递，更安全
3. **灵活性**：可以为不同项目配置不同的 MCP 服务器实例
4. **只读模式**：使用 `--read-only` 参数可以限制为只读操作，防止误操作

### 配置说明

- **`command`**: Windows 系统使用 `cmd`，Linux/Mac 使用 `sh` 或直接使用 `npx`
- **`--project-ref`**: Supabase 项目的唯一标识符，可在项目设置中找到
- **`--read-only`**: （可选）限制为只读操作，防止误修改
- **`SUPABASE_ACCESS_TOKEN`**: Supabase 访问令牌，在 Supabase 控制台生成

### 多项目配置示例

如果需要配置多个 Supabase 项目，可以为每个项目创建独立的配置：

```json
{
  "mcpServers": {
    "supabase-jubianai": {
      "command": "cmd",
      "args": [
        "/c", "npx", "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref=sggdokxjqycskeybyqvv"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_55d3bff12a73fad53040ea5b2db387d0d84a2e03"
      }
    },
    "supabase-jubianage-agent": {
      "command": "cmd",
      "args": [
        "/c", "npx", "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref=ogndfzxtzsifaqwzfojs"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_55d3bff12a73fad53040ea5b2db387d0d84a2e03"
      }
    }
  }
}
```

### 多项目配置的优势

这样配置后，您可以：

1. **查看和修改每个项目的配置**：每个项目都有独立的 MCP 服务器实例，可以单独查看和修改各自的数据库配置、表结构等
2. **在项目间切换操作**：通过指定不同的服务器名称（如 `supabase-jubianai` 或 `supabase-jubianage-agent`），可以在不同项目间切换操作
3. **避免误操作其他项目**：每个项目使用独立的 `--project-ref`，确保操作只影响指定的项目，不会误操作其他项目的数据库

### 使用多项目配置

配置完成后，重启 Cursor。在使用时，可以通过以下方式指定要操作的项目：

- 直接提问时，AI 助手会根据上下文自动选择合适的项目
- 如果需要明确指定项目，可以在提问中提及项目名称，例如："在 jubianai 项目中查看有哪些表"

## 使用方法

配置完成后，重启 Cursor，然后可以直接向 AI 助手提问，例如：

### 示例问题

1. **查看数据库结构**
   - "帮我查看 Supabase 项目中有哪些表"
   - "查看 users 表的结构"
   - "分析数据库表之间的关系"

2. **执行查询**
   - "执行一个查询，找出所有活跃用户"
   - "查询最近 7 天注册的用户数量"
   - "查看某个用户的详细信息"

3. **管理数据库**
   - "创建一个新的用户表"
   - "添加一个新的字段到 users 表"
   - "更新 RLS 策略"

4. **查看配置**
   - "查看认证配置"
   - "查看存储桶配置"
   - "查看 API 端点配置"

## 安全注意事项

⚠️ **重要**：访问令牌已保存在配置文件中。请确保：

1. 不要将 `.cursor/mcp.json` 提交到公共代码仓库
2. 如果已提交，请立即撤销访问令牌并生成新令牌
3. 定期轮换访问令牌
4. 使用 `.gitignore` 排除 `.cursor/` 目录（如果包含敏感信息）

## 验证配置

配置完成后，重启 Cursor，然后尝试询问：

```
"帮我查看 Supabase 项目中有哪些表"
```

如果配置成功，AI 助手应该能够直接访问您的 Supabase 项目并返回结果。

## 故障排除

### 如果 MCP 无法连接

1. **检查访问令牌**
   - 确认访问令牌是否正确
   - 确认令牌是否已过期
   - 在 Supabase 控制台重新生成令牌

2. **检查网络连接**
   - 确保可以访问 Supabase API
   - 检查防火墙设置

3. **检查 Node.js 和 npx**
   - 确保已安装 Node.js
   - 运行 `npx --version` 验证 npx 是否可用

4. **查看 Cursor 日志**
   - 在 Cursor 中查看 MCP 连接日志
   - 检查是否有错误信息

## 更新配置

如果需要更新访问令牌或添加其他 MCP 服务器：

1. 编辑 `.cursor/mcp.json` 文件
2. 更新配置内容
3. 重启 Cursor

## 添加其他 MCP 服务器

您可以在同一个配置文件中添加多个 MCP 服务器：

```json
{
  "mcpServers": {
    "supabase-jubianage-agent": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref=ogndfzxtzsifaqwzfojs"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "your-token-here"
      }
    },
    "other-service": {
      "command": "npx",
      "args": [
        "-y",
        "@other/mcp-server@latest"
      ]
    }
  }
}
```

## 相关资源

- [Supabase MCP Server 文档](https://github.com/supabase/mcp-server-supabase)
- [Cursor MCP 文档](https://docs.cursor.com/mcp)

