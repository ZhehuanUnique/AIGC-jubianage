"""
独立使用 RAG 数据库的示例
演示如何在其他项目中使用导出的数据库
"""
from pathlib import Path
import sys

# 假设导出的数据库在当前目录的 rag_export 文件夹中
export_dir = Path(__file__).parent.parent / "test_export"

# 添加独立包到路径（如果使用独立包）
package_dir = export_dir / "rag_package"
if package_dir.exists():
    sys.path.insert(0, str(package_dir))

# 方式 1：直接使用导出的路径
from vector_db import VectorDB
from vectorizer import ImageVectorizer
from rag_service import RAGService

# 使用导出的数据库路径
db_path = str(export_dir / "vector_db")
frames_dir = str(export_dir / "frames")

print(f"数据库路径: {db_path}")
print(f"关键帧目录: {frames_dir}")

# 初始化 RAG 服务
rag_service = RAGService(
    db_path=db_path,
    frames_dir=frames_dir
)

# 获取统计信息
stats = rag_service.get_stats()
print(f"\n数据库统计:")
print(f"  总帧数: {stats['total_frames']}")
print(f"  集合名称: {stats['collection_name']}")

# 搜索相似帧
print("\n搜索测试:")
results = rag_service.search_similar_frames(
    query="视频画面",
    n_results=3
)

print(f"找到 {len(results)} 个结果:")
for i, result in enumerate(results, 1):
    metadata = result.get("metadata", {})
    print(f"  {i}. 视频ID: {metadata.get('video_id')}, 时间戳: {metadata.get('timestamp')}s")

# 方式 2：使用环境变量配置
import os
os.environ["RAG_DB_PATH"] = str(export_dir / "vector_db")
os.environ["RAG_FRAMES_DIR"] = str(export_dir / "frames")

from db_config import RAGDatabaseConfig

config = RAGDatabaseConfig()
print(f"\n使用环境变量配置:")
print(f"  数据库路径: {config.get_db_path()}")
print(f"  关键帧目录: {config.get_frames_dir()}")


