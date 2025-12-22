# RAG 数据库独立包

## 数据库信息
- 导出时间: 2025-12-22T06:44:19.765545
- 数据库路径: /workspaces/AIGC-jubianage/doubao-rag/vector_db
- 集合名称: video_frames

## 使用方法

### 1. 基本使用

```python
from vector_db import VectorDB
from vectorizer import ImageVectorizer
from rag_service import RAGService

# 使用导出的数据库路径
db_path = "vector_db"  # 相对于当前目录
frames_dir = "frames"  # 相对于当前目录

# 初始化服务
rag_service = RAGService(
    db_path=db_path,
    frames_dir=frames_dir
)

# 搜索相似帧
results = rag_service.search_similar_frames(
    query="快速运镜",
    n_results=5
)
```

### 2. 使用环境变量

```bash
export RAG_DB_PATH="./vector_db"
export RAG_FRAMES_DIR="./frames"
```

### 3. 依赖要求

```bash
pip install chromadb sentence-transformers opencv-python pillow numpy
```

## 文件说明

- `vector_db/` - Chroma 向量数据库
- `frames/` - 关键帧图片文件
- `rag_config.json` - 数据库配置
- `database_stats.json` - 数据库统计信息
- `rag_package/` - 独立使用的 Python 代码包
