# Milvus 启动指南

## 🚀 快速启动 Milvus

### 方式 1：使用 Docker 单容器启动（最简单）

```powershell
# 拉取 Milvus 镜像
docker pull milvusdb/milvus:latest

# 启动 Milvus（单机版）
docker run -d --name milvus-standalone `
  -p 19530:19530 `
  -p 9091:9091 `
  milvusdb/milvus:latest
```

**参数说明**：
- `-d`：后台运行
- `--name milvus-standalone`：容器名称
- `-p 19530:19530`：gRPC 端口（必需）
- `-p 9091:9091`：HTTP 端口（可选，用于监控）

### 方式 2：使用 Docker Compose 启动（推荐，更稳定）

**1. 创建 `docker-compose.yml` 文件**

在项目根目录或任意位置创建 `docker-compose.yml`：

```yaml
version: '3.5'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - etcd_data:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - minio_data:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.3.3
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - milvus_data:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      start_period: 90s
      timeout: 20s
      retries: 3

volumes:
  etcd_data:
  minio_data:
  milvus_data:
```

**2. 启动 Milvus**

```powershell
# 在 docker-compose.yml 所在目录执行
docker-compose up -d
```

**3. 查看启动状态**

```powershell
# 查看所有容器状态
docker-compose ps

# 查看日志
docker-compose logs -f standalone
```

## ✅ 验证 Milvus 是否运行

### 方法 1：检查 Docker 容器

```powershell
# 查看 Milvus 容器是否运行
docker ps | findstr milvus

# 应该看到类似输出：
# CONTAINER ID   IMAGE                    STATUS         PORTS
# xxxxx          milvusdb/milvus:latest   Up X minutes   0.0.0.0:19530->19530/tcp
```

### 方法 2：检查端口是否监听

```powershell
# 检查 19530 端口是否被监听
netstat -an | findstr 19530

# 应该看到类似输出：
# TCP    0.0.0.0:19530          0.0.0.0:0              LISTENING
```

### 方法 3：使用 Milvus 客户端测试连接

创建测试脚本 `test-milvus-connection.js`：

```javascript
import { MilvusClient } from '@zilliz/milvus2-sdk-node'

async function testConnection() {
  try {
    const client = new MilvusClient({
      address: 'localhost:19530',
    })

    // 测试连接
    const result = await client.listCollections()
    console.log('✅ Milvus 连接成功！')
    console.log('集合列表:', result)
  } catch (error) {
    console.error('❌ Milvus 连接失败:', error.message)
  }
}

testConnection()
```

运行测试：

```powershell
cd server
node test-milvus-connection.js
```

### 方法 4：访问 Milvus 监控界面

如果使用 Docker Compose 启动，可以访问：

```
http://localhost:9091/healthz
```

如果返回 `OK`，说明 Milvus 正常运行。

## 🔧 常见问题解决

### 问题 1：端口被占用

**错误信息**：`port is already allocated`

**解决方法**：

```powershell
# 查看占用 19530 端口的进程
netstat -ano | findstr 19530

# 停止占用端口的进程（替换 PID 为实际进程ID）
taskkill /PID <PID> /F

# 或者修改 Milvus 端口映射
docker run -d --name milvus-standalone -p 19531:19530 milvusdb/milvus:latest
# 然后在 .env 中修改 MILVUS_PORT=19531
```

### 问题 2：容器启动失败

**查看日志**：

```powershell
# 查看容器日志
docker logs milvus-standalone

# 或使用 Docker Compose
docker-compose logs standalone
```

**常见原因**：
- 内存不足（Milvus 需要至少 2GB 内存）
- 端口冲突
- Docker 资源不足

### 问题 3：连接超时（DEADLINE_EXCEEDED）

**错误信息**：`Error: 4 DEADLINE_EXCEEDED: Deadline exceeded`

**解决方法**：

1. **检查 Milvus 是否运行**：
   ```powershell
   docker ps | findstr milvus
   ```

2. **检查防火墙设置**：
   - 确保 19530 端口没有被防火墙阻止

3. **增加超时时间**：
   在 `server/services/videoMotionPrompt/geminiRagService.js` 中，Milvus 客户端初始化时可以设置超时：
   ```javascript
   this.milvusClient = new MilvusClient({
     address: `${this.milvusHost}:${this.milvusPort}`,
     timeout: 60000, // 60秒超时
   })
   ```

4. **检查网络连接**：
   ```powershell
   # 测试端口连通性
   telnet localhost 19530
   ```

### 问题 4：不想使用 Milvus，切换到 Chroma

如果不想使用 Milvus，可以切换到 Chroma（更简单）：

**1. 修改 `.env` 文件**：

```env
# 改为使用 Chroma
VECTOR_DB_TYPE=chroma
```

**2. 停止 Milvus 容器**（如果已启动）：

```powershell
# 停止并删除容器
docker stop milvus-standalone
docker rm milvus-standalone

# 或使用 Docker Compose
docker-compose down
```

**3. 安装 Chroma 依赖**：

```powershell
cd server
npm install chromadb
```

**4. 重启后端服务**：

```powershell
cd server
npm start
```

## 📋 完整启动流程

### 第一次启动 Milvus

```powershell
# 1. 拉取镜像
docker pull milvusdb/milvus:latest

# 2. 启动容器
docker run -d --name milvus-standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest

# 3. 等待几秒钟让 Milvus 完全启动
timeout /t 10

# 4. 验证连接
docker ps | findstr milvus

# 5. 检查日志（可选）
docker logs milvus-standalone
```

### 日常使用

```powershell
# 启动 Milvus（如果已停止）
docker start milvus-standalone

# 停止 Milvus
docker stop milvus-standalone

# 重启 Milvus
docker restart milvus-standalone

# 查看状态
docker ps -a | findstr milvus
```

## 🎯 推荐配置

### 开发环境（推荐使用 Chroma）

```env
VECTOR_DB_TYPE=chroma
GEMINI_RAG_VECTOR_DB_PATH=./data/gemini_rag_vectors
```

**优点**：
- ✅ 无需额外服务
- ✅ 启动快速
- ✅ 资源占用少

### 生产环境（推荐使用 Milvus）

```env
VECTOR_DB_TYPE=milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

**优点**：
- ✅ 性能更好
- ✅ 支持大规模数据
- ✅ 更稳定

## 💡 提示

1. **首次启动需要时间**：Milvus 首次启动可能需要 30-60 秒
2. **资源要求**：确保 Docker 有足够的内存（至少 2GB）
3. **持久化数据**：使用 Docker Compose 可以持久化数据，重启不会丢失
4. **监控**：访问 `http://localhost:9091` 可以查看 Milvus 状态

## 🔗 相关文档

- [Milvus 官方文档](https://milvus.io/docs)
- [Docker 安装指南](https://milvus.io/docs/install_standalone-docker.md)
- [RAG库高级版本使用指南.md](./RAG库高级版本使用指南.md)

