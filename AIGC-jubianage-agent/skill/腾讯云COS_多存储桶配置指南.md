# 腾讯云 COS 多存储桶配置指南

## 问题说明

在 `.cursor/mcp.json` 中，**不能使用相同的键名**。如果有多个存储桶，需要为每个存储桶配置不同的服务器名称。

## 错误配置示例 ❌

```json
{
  "mcpServers": {
    "tencent-cos": {
      "--Bucket=bucket1-APPID"
    },
    "tencent-cos": {  // ❌ 错误：重复的键名，后面的会覆盖前面的
      "--Bucket=bucket2-APPID"
    }
  }
}
```

## 正确配置示例 ✅

### 方式一：使用描述性名称（推荐）

```json
{
  "mcpServers": {
    "tencent-cos-bucket1": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=bucket1-1392491103",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "COS_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    },
    "tencent-cos-bucket2": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-beijing",
        "--Bucket=bucket2-1392491103",
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

### 方式二：使用数字后缀

```json
{
  "mcpServers": {
    "tencent-cos-1": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=bucket1-1392491103",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "COS_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    },
    "tencent-cos-2": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-beijing",
        "--Bucket=bucket2-1392491103",
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

### 方式三：使用项目/用途命名

```json
{
  "mcpServers": {
    "tencent-cos-jubianage-agent": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=jubianage-agent-1392491103",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "COS_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    },
    "tencent-cos-backup": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-beijing",
        "--Bucket=backup-1392491103",
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

## 配置要点

### 1. 每个存储桶需要独立的配置

- ✅ 使用不同的服务器名称（键名）
- ✅ 每个配置包含完整的参数
- ✅ 可以有不同的 Region、Bucket、DatasetName

### 2. 共享密钥 vs 独立密钥

**如果两个存储桶属于同一个账号：**
- 可以使用相同的 `COS_SECRET_ID` 和 `COS_SECRET_KEY`

**如果两个存储桶属于不同账号：**
- 需要使用不同的 `COS_SECRET_ID` 和 `COS_SECRET_KEY`

### 3. DatasetName 配置

如果不同存储桶需要不同的数据集：

```json
{
  "mcpServers": {
    "tencent-cos-bucket1": {
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=bucket1-1392491103",
        "--DatasetName=dataset1",
        "--connectType=stdio"
      ]
    },
    "tencent-cos-bucket2": {
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-beijing",
        "--Bucket=bucket2-1392491103",
        "--DatasetName=dataset2",
        "--connectType=stdio"
      ]
    }
  }
}
```

## 完整配置示例

假设您有两个存储桶：
- `jubianage-agent-1392491103`（广州）
- `backup-storage-1392491103`（北京）

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
    },
    "tencent-cos-main": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=jubianage-agent-1392491103",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "COS_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    },
    "tencent-cos-backup": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-beijing",
        "--Bucket=backup-storage-1392491103",
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

## 使用方式

配置完成后，重启 Cursor。在使用时：

1. **AI 助手会自动识别**：根据上下文选择合适的存储桶
2. **明确指定存储桶**：可以在提问中指定，例如：
   - "在 main 存储桶中上传文件"
   - "列出 backup 存储桶中的文件"

## 验证配置

1. **检查 JSON 格式**：确保没有重复的键名
2. **重启 Cursor**：完全关闭后重新打开
3. **查看 MCP 状态**：在 Cursor 设置中，应该看到多个 `tencent-cos-*` 服务器，都显示为绿色（运行中）

## 常见问题

### Q1: 两个存储桶可以使用相同的密钥吗？

**A:** 如果两个存储桶属于同一个腾讯云账号，可以使用相同的 `COS_SECRET_ID` 和 `COS_SECRET_KEY`。

### Q2: 如何区分使用哪个存储桶？

**A:** 通过不同的服务器名称（键名）来区分。AI 助手会根据上下文或您的明确指示选择合适的存储桶。

### Q3: 可以配置多少个存储桶？

**A:** 理论上没有限制，但建议根据实际需求配置，避免过多配置影响性能。

### Q4: 如果两个存储桶在不同地域，需要分别配置吗？

**A:** 是的，每个存储桶都需要独立的配置，包括 `--Region` 参数。

## 注意事项

1. ⚠️ **键名必须唯一**：不能使用相同的键名
2. ⚠️ **完整配置**：每个存储桶都需要完整的配置参数
3. ⚠️ **密钥安全**：确保密钥安全，不要泄露
4. ⚠️ **重启生效**：修改配置后需要重启 Cursor

