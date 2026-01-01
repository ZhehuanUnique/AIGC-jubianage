# 腾讯云 COS MCP 接入指南

## 概述

腾讯云提供了 COS（对象存储）的 MCP Server，支持通过 Model Context Protocol 与 AI 助手交互，实现对象存储的自动化管理。

## 功能特性

### 1. 对象存储 COS 接口
- 上传/下载对象
- 获取对象列表
- 删除对象
- 获取对象元数据

### 2. 数据万象 CI 接口
- 文档转 PDF
- 图片文字水印
- 图片二维码识别
- 图片质量评分
- 图片超分
- 图片通用抠图
- 图片智能裁剪
- 智能检索 MetaInsight（文搜图、图搜图）
- 视频智能封面

## 安装方式

### 方式一：npm 全局安装

```bash
npm install -g cos-mcp@latest
```

### 方式二：在项目中安装

```bash
npm install cos-mcp --save-dev
```

## 配置方式

### 方式一：命令行参数启动

```bash
cos-mcp \
  --Region=ap-guangzhou \
  --Bucket=your-bucket-name-APPID \
  --SecretId=your-secret-id \
  --SecretKey=your-secret-key \
  --DatasetName=your-dataset-name \
  --port=3001 \
  --connectType=sse
```

### 方式二：JSON 配置启动

```bash
cos-mcp \
  --cos-config='{"Region":"ap-guangzhou","Bucket":"your-bucket-name-APPID","SecretId":"your-secret-id","SecretKey":"your-secret-key","DatasetName":"your-dataset-name"}' \
  --port=3001 \
  --connectType=sse
```

### 方式三：在 Cursor 中配置 MCP（推荐使用 stdio）

在 `.cursor/mcp.json` 中添加：

**推荐配置（使用 stdio 连接类型）：**

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

**重要提示：**
- ✅ **推荐使用 `stdio` 连接类型**，避免 JSON 解析错误
- ✅ **使用环境变量存储敏感信息**（SecretId、SecretKey），更安全
- ✅ **使用 `stdio` 时，不要包含 `--port` 参数**
- ⚠️ 如果使用 `sse` 连接类型，需要包含 `--port` 参数，但可能遇到 JSON 解析问题

**备选配置（使用 sse 连接类型）：**

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
        "--port=3001",
        "--connectType=sse"
      ],
      "env": {
        "COS_SECRET_ID": "your-secret-id",
        "COS_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

## 参数说明

- `Region`: COS 存储桶所在的地域（如：ap-guangzhou、ap-beijing）
- `Bucket`: 存储桶名称（格式：bucket-name-APPID）
- `SecretId`: 腾讯云 API 密钥 ID
- `SecretKey`: 腾讯云 API 密钥 Key
- `DatasetName`: 数据集名称（用于智能检索）
- `port`: MCP Server 监听端口（默认：3001）
- `connectType`: 连接类型（sse 或 stdio）

## 使用场景

1. **自动上传生成的图片/视频到 COS**
2. **管理 COS 中的文件（列表、删除、下载）**
3. **图片处理（水印、裁剪、超分等）**
4. **智能检索（文搜图、图搜图）**
5. **文档转换（转 PDF）**

## 获取腾讯云密钥

### 步骤

1. **登录腾讯云控制台**
   - 访问 [腾讯云控制台](https://console.cloud.tencent.com)

2. **进入访问管理**
   - 点击右上角头像 → **访问管理**
   - 或直接访问 [访问管理控制台](https://console.cloud.tencent.com/cam)

3. **进入 API 密钥管理**
   - 左侧菜单：**访问密钥** → **API 密钥管理**

4. **创建或查看密钥**
   - 如果已有密钥，直接查看并复制
   - 如果没有，点击 **新建密钥**
   - **SecretId**：类似 `AKID_EXAMPLE_32_CHARACTERS_LONG`
   - **SecretKey**：类似 `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（只显示一次，请立即保存）

5. **获取地域和存储桶信息**
   - 访问 [COS 控制台](https://console.cloud.tencent.com/cos)
   - 查看存储桶的 **地域**（Region）和 **名称**（格式：`bucket-name-APPID`）

6. **获取数据集名称（DatasetName）**
   - 访问 [数据万象控制台](https://console.cloud.tencent.com/ci)
   - 进入 **智能检索** 或 **MetaInsight**
   - 查看或创建数据集，获取数据集名称
   - **注意**：DatasetName 是可选的，只有在需要使用智能检索功能时才需要

**详细步骤请参考：** [Bucket 和 DatasetName 获取指南](./腾讯云COS_Bucket和DatasetName获取指南.md)

## 相关文档

- [COS MCP Server 接入指南](https://docs.cloudbase.net/en/ai/mcp/develop/server-templates/cloudrun-mcp-cos)
- [腾讯云存储推出 COS MCP Server](https://brands.cnblogs.com/tencentcloud/p/20498)
- [GitHub 和 Vercel 令牌获取指南](./MCP令牌获取指南.md)

## 注意事项

1. **安全性**：不要将 SecretId 和 SecretKey 直接写在配置文件中，建议使用环境变量
2. **权限**：确保 API 密钥有足够的权限访问 COS 存储桶
3. **地域**：确保 Region 参数与存储桶实际所在地域一致
4. **存储桶名称**：格式必须为 `bucket-name-APPID`（APPID 是腾讯云账号的 APPID）
5. **连接类型**：推荐使用 `stdio` 而不是 `sse`，可以避免 JSON 解析错误
6. **参数格式**：所有参数使用 `--参数名=值` 格式，参数名区分大小写

## 故障排除

如果遇到 JSON 解析错误（如 `Unexpected end of JSON input`、`"COS配置信息:" is not valid JSON`），请参考：

- [腾讯云 COS MCP 故障排除指南](./腾讯云COS_MCP故障排除.md)

**快速解决方案：**
1. 将 `--connectType=sse` 改为 `--connectType=stdio`
2. 移除 `--port` 参数（使用 stdio 时不需要）
3. 确保使用环境变量存储 SecretId 和 SecretKey

