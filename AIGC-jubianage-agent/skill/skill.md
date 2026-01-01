# AIGC 剧变时代 Agent - 技能文档

本文档整合了项目中所有通用功能和配置指南。

## 📋 目录

1. [MCP 配置指南](#mcp-配置指南)
2. [图片生成模型说明](#图片生成模型说明)
3. [数据库管理](#数据库管理)
4. [Milvus 向量数据库](#milvus-向量数据库)
5. [腾讯云 COS 配置](#腾讯云-cos-配置)
6. [常用命令](#常用命令)

---

## MCP 配置指南

### MCP 服务器配置位置

配置文件：`.cursor/mcp.json`

### 当前已配置的 MCP 服务器

1. **Supabase** - 数据库管理
2. **腾讯云 COS** - 对象存储
3. **GitHub** - 代码仓库管理
4. **Vercel** - 部署管理
5. **火山引擎 Vevod** - 视频处理
6. **302.ai Custom MCP** - AI 服务

### MCP 工具数量优化

**问题**：当工具数量超过 80 个时，Cursor 会显示警告。

**解决方案**：
1. 在 Cursor 设置中禁用不需要的工具
2. 只保留实际使用的工具
3. 推荐工具数量：50-80 个

### Vercel MCP 工具选择

**需要保留的工具**：
- `get_deployment` - 获取部署信息
- `get_deployment_events` - 获取部署事件
- `get_deployment_logs` - 获取部署日志
- `get_project` - 获取项目信息
- 域名管理相关工具
- 环境变量管理相关工具

**需要禁用的工具类别**：
- 团队管理工具
- 监控和分析工具
- 安全设置工具

### MCP 令牌获取

#### GitHub Personal Access Token
1. 访问 [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. 生成新令牌，选择所需权限
3. 复制令牌（只显示一次）

#### Vercel Access Token
1. 访问 [Vercel Account → Tokens](https://vercel.com/account/tokens)
2. 创建新令牌
3. 复制令牌（只显示一次）

#### 腾讯云 COS 密钥
1. 访问 [腾讯云控制台 → 访问管理 → API密钥管理](https://console.cloud.tencent.com/cam/capi)
2. 创建或查看密钥
3. 获取 SecretId 和 SecretKey

---

## 图片生成模型说明

### 支持参考图的模型

1. **nano-banana-pro** ✅
   - 支持单张参考图

2. **seedream-4-0** ✅
   - 支持单张或多张参考图（最多10张）

3. **seedream-4-5** ✅
   - 支持单张或多张参考图（最多10张）

4. **flux-2-max** ✅
   - 支持单张或多张参考图（最多8张）

5. **flux-2-flex** ✅
   - 支持单张或多张参考图（最多8张）

6. **flux-2-pro** ✅
   - 支持单张或多张参考图（最多8张）

### 不支持参考图的模型

1. **midjourney-v7-t2i** ❌
   - 不支持参考图（图生图模式）
   - 只能使用文生图模式
   - 会生成4张图片的网格（2x2布局）
   - 自动 Upscale 功能：网格图生成后自动放大

### 使用说明

- **自动启用参考图模式**：当关联了角色、场景、物品或姿势时，系统会自动启用参考图模式
- **参考图优先级**：
  - nano-banana-pro：只支持单张，使用第一张图片
  - Seedream、Flux：支持多张参考图，传递所有关联的图片
- **图片比例**：所有分镜使用全局设置的图片比例（16:9、9:16 或 1:1）

---

## 数据库管理

### Supabase 配置

**配置文件位置**：`.cursor/mcp.json`

**只读模式配置**：
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
        "SUPABASE_ACCESS_TOKEN": "您的访问令牌"
      }
    }
  }
}
```

### 用户数据隔离

- 所有项目、任务、角色、场景、物品等数据都按 `user_id` 隔离
- 每个用户只能看到和操作自己的数据
- 创建数据时自动关联当前登录用户

### 数据库表结构

主要表：
- `users` - 用户表
- `projects` - 项目表（包含 `user_id`）
- `tasks` - 任务表（包含 `user_id`）
- `characters` - 角色表
- `scenes` - 场景表
- `items` - 物品表
- `shots` - 分镜表
- `files` - 文件表

---

## Milvus 向量数据库

### 快速启动

#### 方式 1：Docker 单容器启动

```powershell
docker pull milvusdb/milvus:latest
docker run -d --name milvus-standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest
```

#### 方式 2：Docker Compose 启动（推荐）

```powershell
cd milvus
docker-compose up -d
```

### 验证 Milvus 运行

```powershell
# 检查容器状态
docker ps | findstr milvus

# 检查端口
netstat -an | findstr 19530
```

### 常用命令

```powershell
# 启动
docker start milvus-standalone

# 停止
docker stop milvus-standalone

# 查看日志
docker logs milvus-standalone

# 进入容器
docker exec -it milvus-standalone /bin/bash
```

---

## 腾讯云 COS 配置

### MCP 配置

```json
{
  "mcpServers": {
    "tencent-cos-AIGC-jubianage-agent": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=jubianage-agent-1392491103",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "您的SecretId",
        "COS_SECRET_KEY": "您的SecretKey"
      }
    }
  }
}
```

### 功能特性

- 对象存储：上传/下载/删除对象
- 图片处理：水印、超分、抠图、质量评估
- 文档处理：文档转 PDF
- 智能检索：文搜图、图搜图

---

## 常用命令

### Docker 相关

```powershell
# Milvus 启动
cd milvus
docker-compose up -d

# Milvus 停止
docker-compose down

# 查看 Milvus 容器
docker ps | findstr milvus
```

### 项目相关

```powershell
# 启动后端服务
cd server
npm start

# 启动前端服务
cd client
npm start
```

### 数据库相关

```powershell
# 查看 Supabase 表
# 使用 MCP 工具：mcp_supabase-jubianage-agent_list_tables

# 执行 SQL 迁移
# 使用 MCP 工具：mcp_supabase-jubianage-agent_apply_migration
```

---

## 注意事项

1. **MCP 配置修改后需要重启 Cursor**
2. **API 密钥和令牌不要提交到代码仓库**
3. **用户数据完全隔离，不同用户之间数据不互通**
4. **工具数量建议控制在 80 个以下**
5. **所有新的 .md 文档应保存在 `skill` 文件夹中**

---

## 相关资源

- [Supabase Dashboard](https://app.supabase.com)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [腾讯云控制台](https://console.cloud.tencent.com)
- [302.ai Dashboard](https://302.ai/dashboard)

