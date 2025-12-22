# RAG 数据库导出指南

## 概述

RAG 数据库是**完全独立**的，与 jubianai 项目的 PostgreSQL 数据库分开存储：

- **RAG 数据库**：Chroma 向量数据库（`doubao-rag/vector_db/`）
- **jubianai 数据库**：PostgreSQL（用于资产元数据）

两者互不干扰，可以单独使用。

## 数据库位置

### RAG 数据库
- **路径**: `doubao-rag/vector_db/`
- **文件**: `chroma.sqlite3`（向量数据）
- **关键帧**: `doubao-rag/frames/`（图片文件）

### jubianai 数据库
- **类型**: PostgreSQL
- **用途**: 存储资产元数据（与 RAG 无关）

## 导出数据库

### 方法 1：使用导出脚本（推荐）

```bash
cd doubao-rag/backend
python db_export.py ./rag_export
```

这会创建一个包含以下内容的导出目录：
- `vector_db/` - 向量数据库
- `frames/` - 关键帧图片
- `rag_config.json` - 配置信息
- `database_stats.json` - 统计信息
- `rag_package/` - 独立使用的代码包

### 方法 2：手动复制

```bash
# 创建导出目录
mkdir -p rag_export

# 复制数据库
cp -r doubao-rag/vector_db rag_export/

# 复制关键帧（可选）
cp -r doubao-rag/frames rag_export/
```

### 方法 3：使用 Python API

```python
from doubao_rag.backend.db_export import export_rag_database

# 导出数据库
result = export_rag_database(
    output_dir="./rag_export",
    include_frames=True,  # 包含关键帧文件
    create_package=True   # 创建独立包
)

print(f"导出完成: {result['output_dir']}")
```

## 在其他地方使用导出的数据库

### 1. 复制文件

将导出的目录复制到新位置：
```bash
cp -r rag_export /path/to/new/location/
```

### 2. 使用独立包

导出的 `rag_package/` 目录包含所有必要的代码：

```python
# 在新项目中
import sys
sys.path.insert(0, '/path/to/rag_package')

from vector_db import VectorDB
from vectorizer import ImageVectorizer
from rag_service import RAGService

# 使用导出的数据库路径
rag_service = RAGService(
    db_path="./vector_db",  # 相对于当前目录
    frames_dir="./frames"   # 相对于当前目录
)

# 使用服务
results = rag_service.search_similar_frames(
    query="快速运镜",
    n_results=5
)
```

### 3. 使用环境变量

```bash
export RAG_DB_PATH="/path/to/vector_db"
export RAG_FRAMES_DIR="/path/to/frames"
```

然后在代码中：
```python
from doubao_rag.backend.db_config import RAGDatabaseConfig
from doubao_rag.backend.rag_service import RAGService

config = RAGDatabaseConfig()  # 自动从环境变量读取
rag_service = RAGService(
    db_path=config.get_db_path(),
    frames_dir=config.get_frames_dir()
)
```

## 数据库结构

### Chroma 数据库
- **格式**: SQLite3
- **位置**: `vector_db/chroma.sqlite3`
- **内容**: 向量嵌入、元数据、索引

### 关键帧文件
- **格式**: JPG 图片
- **位置**: `frames/<video_id>/frame_*.jpg`
- **内容**: 提取的视频关键帧

## 注意事项

1. **数据库和关键帧必须一起使用**
   - 向量数据库存储的是关键帧的向量表示
   - 关键帧文件用于显示和进一步处理
   - 两者路径在元数据中关联

2. **路径问题**
   - 如果移动数据库，需要确保关键帧路径正确
   - 或者使用绝对路径配置

3. **版本兼容性**
   - Chroma 数据库版本需要兼容
   - 建议使用相同版本的 chromadb

## 快速导出命令

```bash
# 导出到当前目录
cd doubao-rag/backend
python db_export.py ../../rag_standalone

# 只导出数据库（不包含关键帧）
python db_export.py ../../rag_standalone --no-frames

# 不创建独立包
python db_export.py ../../rag_standalone --no-package
```

## 验证导出

检查导出目录：
```bash
ls -lh rag_export/
# 应该看到：
# - vector_db/
# - frames/
# - rag_config.json
# - database_stats.json
# - rag_package/
```

查看统计信息：
```bash
cat rag_export/database_stats.json
```

