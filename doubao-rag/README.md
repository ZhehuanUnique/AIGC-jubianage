# 视频 RAG 系统（基于 LangGraph）

将视频转换为向量，形成 RAG 库，用于生成视频时参考镜头、运镜等风格。

**使用 LangGraph 框架构建**，提供灵活的工作流和状态管理。

## 功能特性

- ✅ **视频处理**：提取关键帧（按时间间隔或场景变化）
- ✅ **向量化**：使用 CLIP 模型将图片转为向量
- ✅ **向量存储**：使用 Chroma 向量数据库存储
- ✅ **相似检索**：根据文本或图片检索相似帧
- ✅ **提示词增强**：通过 RAG 检索增强视频生成提示词
- ✅ **自动集成**：已集成到视频生成流程，自动增强提示词
- ✅ **LangGraph 工作流**：使用 LangGraph 构建可扩展的工作流

## 安装依赖

### ⚠️ 重要：避免 Rust 编译错误和代理问题

`tokenizers` 需要 Rust 编译器，但我们可以使用预编译包避免编译。

#### 方式 1：使用安装脚本（推荐，最简单）

**如果遇到代理错误，使用 `install-no-proxy.bat`：**

**Windows:**
```bash
cd doubao-rag
install-no-proxy.bat
```

**或普通安装脚本：**
```bash
cd doubao-rag
install.bat
```

**Linux/Mac:**
```bash
cd doubao-rag
chmod +x install.sh
./install.sh
```

#### 方式 2：手动分步安装

```bash
# 1. 基础依赖
pip install fastapi uvicorn python-multipart pydantic opencv-python pillow numpy

# 2. LangGraph
pip install langgraph langchain langchain-core

# 3. 预编译的 tokenizers（关键步骤！必须先安装）
pip install tokenizers --only-binary :all:

# 如果上面失败，尝试使用国内镜像：
pip install tokenizers --only-binary :all: -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. sentence-transformers
pip install sentence-transformers

# 5. chromadb
pip install chromadb

# 6. 可选
pip install ffmpeg-python
```

#### 方式 3：使用国内镜像（如果方式 2 失败）

```bash
# 先安装预编译的 tokenizers
pip install tokenizers --only-binary :all: -i https://pypi.tuna.tsinghua.edu.cn/simple

# 然后安装其他依赖
pip install -r doubao-rag/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --prefer-binary
```

#### 方式 4：安装 Rust（最后的选择）

如果预编译包都失败，可以安装 Rust：
- Windows: 下载 https://rustup.rs/ 并安装
- 或使用: `choco install rust` (需要 Chocolatey)
- 安装后重启终端，然后运行 `pip install -r doubao-rag/requirements.txt`

## 快速开始

### 1. 启动 API 服务

**重要**：必须在项目根目录 `AIGC-jubianage` 下启动，因为代码中的路径是相对于项目根目录的：

```bash
# 在 AIGC-jubianage 目录下
cd C:\Users\Administrator\Desktop\AIGC-jubianage

# 启动 RAG API 服务
python -m uvicorn doubao-rag.backend.api:app --host 0.0.0.0 --port 8001
```

### 2. 上传并处理视频

curl 命令可以在任何目录执行，但文件路径要正确：

```bash
# 如果视频文件在 AIGC-jubianage 目录下
cd C:\Users\Administrator\Desktop\AIGC-jubianage
curl -X POST "http://localhost:8001/api/v1/rag/video/upload" \
  -F "file=@your_video.mp4" \
  -F "video_id=my_video" \
  -F "method=interval" \
  -F "interval_seconds=1.0"

# 如果视频文件在其他目录，使用绝对路径
curl -X POST "http://localhost:8001/api/v1/rag/video/upload" \
  -F "file=@C:/path/to/your_video.mp4" \
  -F "video_id=my_video" \
  -F "method=interval" \
  -F "interval_seconds=1.0"
```

**Windows PowerShell 注意**：使用 `curl.exe` 代替 `curl`，或使用反引号 ` 代替反斜杠 `\`

### 3. 搜索相似帧

```bash
curl -X POST "http://localhost:8001/api/v1/rag/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "快速运镜",
    "n_results": 5
  }'
```

### 4. 增强提示词

```bash
curl -X POST "http://localhost:8001/api/v1/rag/enhance-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一个快速移动的镜头",
    "n_references": 3
  }'
```

## 集成到视频生成流程

RAG 系统已自动集成到视频生成流程中。当调用视频生成接口时，系统会自动：

1. **检索相似帧**：根据提示词在向量库中检索相似的关键帧
2. **增强提示词**：将检索到的参考信息融入提示词
3. **生成视频**：使用增强后的提示词生成视频

### 工作流程

```
用户输入提示词
    ↓
RAG 检索相似帧（镜头、运镜等）
    ↓
增强提示词（加入参考信息）
    ↓
调用视频生成 API（使用增强后的提示词）
    ↓
返回生成的视频
```

### 响应示例

```json
{
  "success": true,
  "task_id": "task_123456",
  "message": "视频生成任务已提交",
  "rag_enhanced": true,
  "original_prompt": "一个快速移动的镜头",
  "enhanced_prompt": "一个快速移动的镜头 [参考: 参考时间点: 5.0s, 参考时间点: 12.0s]",
  "rag_references_count": 2
}
```

### 配置说明

- **自动启用**：RAG 功能自动启用，无需配置
- **容错机制**：如果 RAG 服务不可用，自动回退到使用原始提示词
- **调整参数**：在 `jubianai/backend/api.py` 中修改 `n_references` 参数

## API 接口

### POST `/api/v1/rag/video/upload`
上传并处理视频（提取帧 → 向量化 → 存储）

### POST `/api/v1/rag/search`
通过文本搜索相似帧

### POST `/api/v1/rag/search/image`
通过图片搜索相似帧

### POST `/api/v1/rag/enhance-prompt`
增强提示词

### DELETE `/api/v1/rag/video/{video_id}`
删除视频及其所有帧

### GET `/api/v1/rag/stats`
获取统计信息

## 项目结构

```
doubao-rag/
├── backend/
│   ├── video_processor.py    # 视频处理（提取关键帧）
│   ├── vectorizer.py          # 向量化（图片转向量）
│   ├── vector_db.py           # 向量数据库（Chroma）
│   ├── rag_service.py         # RAG 服务（整合所有功能）
│   └── api.py                 # API 接口
├── frames/                    # 关键帧存储目录
├── vector_db/                 # 向量数据库存储目录
├── uploads/                   # 上传视频存储目录
└── requirements.txt          # 依赖列表
```

## 技术栈

- **工作流框架**：LangGraph
- **视频处理**：OpenCV
- **向量化**：sentence-transformers (CLIP)
- **向量数据库**：Chroma
- **API 框架**：FastAPI

## LangGraph 工作流

系统使用 LangGraph 构建了三个主要工作流：

### 1. 视频处理工作流
```
提取关键帧 → 向量化 → 存储到数据库
```

### 2. RAG 检索工作流
```
编码查询（文本/图片）→ 检索相似帧
```

### 3. 提示词增强工作流
```
编码提示词 → 检索参考帧 → 增强提示词
```

### 工作流优势

- **可扩展**：易于添加新节点和条件分支
- **可调试**：每个步骤的状态清晰可见
- **可监控**：可以追踪工作流的执行过程
- **可组合**：工作流可以组合使用

## 注意事项

1. **启动位置**：必须在 `AIGC-jubianage` 目录下启动服务
2. **首次使用**：需要先上传视频到 RAG 库
3. **模型下载**：首次使用 CLIP 模型需要下载（约 600MB）
4. **性能影响**：RAG 检索会增加少量延迟（通常 < 1 秒）
5. **存储空间**：向量数据库需要存储空间
