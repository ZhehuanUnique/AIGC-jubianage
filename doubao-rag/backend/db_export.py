"""
数据库导出工具
用于导出 RAG 数据库，方便单独使用
"""
import shutil
import json
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

from vector_db import VectorDB
from db_config import RAGDatabaseConfig


class RAGDatabaseExporter:
    """RAG 数据库导出器"""
    
    def __init__(self, config: Optional[RAGDatabaseConfig] = None):
        """
        初始化导出器
        
        Args:
            config: 数据库配置（如果为 None，使用默认配置）
        """
        self.config = config or RAGDatabaseConfig()
        self.vector_db = VectorDB(
            db_path=str(self.config.get_db_path()),
            collection_name=self.config.collection_name
        )
    
    def export_database(
        self,
        output_dir: str,
        include_frames: bool = True,
        create_package: bool = True
    ) -> Dict:
        """
        导出数据库到指定目录
        
        Args:
            output_dir: 输出目录
            include_frames: 是否包含关键帧文件
            create_package: 是否创建完整的独立包
        
        Returns:
            Dict: 导出信息
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        export_info = {
            "export_time": datetime.now().isoformat(),
            "db_path": str(self.config.get_db_path()),
            "frames_dir": str(self.config.get_frames_dir()),
            "collection_name": self.config.collection_name,
            "files_exported": []
        }
        
        # 1. 导出向量数据库
        db_output = output_path / "vector_db"
        db_output.mkdir(exist_ok=True)
        
        source_db = self.config.get_db_path()
        if source_db.exists():
            # 复制整个数据库目录
            if source_db.is_dir():
                shutil.copytree(source_db, db_output, dirs_exist_ok=True)
                export_info["files_exported"].append("vector_db/")
            else:
                # 如果是单个文件
                shutil.copy2(source_db, db_output)
                export_info["files_exported"].append(f"vector_db/{source_db.name}")
        
        # 2. 导出关键帧（如果包含）
        if include_frames:
            frames_output = output_path / "frames"
            source_frames = self.config.get_frames_dir()
            
            if source_frames.exists():
                shutil.copytree(source_frames, frames_output, dirs_exist_ok=True)
                export_info["files_exported"].append("frames/")
        
        # 3. 导出配置信息
        config_file = output_path / "rag_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)
        export_info["files_exported"].append("rag_config.json")
        
        # 4. 导出统计信息
        stats = self.vector_db.get_stats()
        stats_file = output_path / "database_stats.json"
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        export_info["files_exported"].append("database_stats.json")
        
        # 5. 如果创建独立包，复制必要的代码文件
        if create_package:
            self._create_standalone_package(output_path)
            export_info["package_created"] = True
        
        export_info["output_dir"] = str(output_path.resolve())
        
        return export_info
    
    def _create_standalone_package(self, output_path: Path):
        """创建独立使用的包"""
        package_dir = output_path / "rag_package"
        package_dir.mkdir(exist_ok=True)
        
        # 复制必要的 Python 文件
        backend_dir = Path(__file__).parent
        files_to_copy = [
            "vector_db.py",
            "vectorizer.py",
            "video_processor.py",
            "rag_service.py",
            "db_config.py"
        ]
        
        for file_name in files_to_copy:
            source_file = backend_dir / file_name
            if source_file.exists():
                shutil.copy2(source_file, package_dir / file_name)
        
        # 创建 README
        readme_content = f"""# RAG 数据库独立包

## 数据库信息
- 导出时间: {datetime.now().isoformat()}
- 数据库路径: {self.config.get_db_path()}
- 集合名称: {self.config.collection_name}

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
"""
        
        with open(package_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # 创建 requirements.txt
        requirements = """chromadb>=0.4.0
sentence-transformers>=2.2.0
opencv-python>=4.8.0
pillow>=10.0.0
numpy>=1.24.0
"""
        with open(package_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)


def export_rag_database(
    output_dir: str,
    db_path: Optional[str] = None,
    frames_dir: Optional[str] = None,
    include_frames: bool = True,
    create_package: bool = True
) -> Dict:
    """
    导出 RAG 数据库的便捷函数
    
    Args:
        output_dir: 输出目录
        db_path: 数据库路径（可选）
        frames_dir: 关键帧目录（可选）
        include_frames: 是否包含关键帧文件
        create_package: 是否创建独立包
    
    Returns:
        Dict: 导出信息
    """
    config = RAGDatabaseConfig(db_path=db_path, frames_dir=frames_dir)
    exporter = RAGDatabaseExporter(config)
    return exporter.export_database(
        output_dir=output_dir,
        include_frames=include_frames,
        create_package=create_package
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python db_export.py <输出目录> [--no-frames] [--no-package]")
        print("示例: python db_export.py ./rag_export")
        print("      python db_export.py ./rag_export --no-frames")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    include_frames = "--no-frames" not in sys.argv
    create_package = "--no-package" not in sys.argv
    
    print(f"正在导出 RAG 数据库到: {output_dir}")
    result = export_rag_database(
        output_dir=output_dir,
        include_frames=include_frames,
        create_package=create_package
    )
    
    print("\n✅ 导出完成！")
    print(f"输出目录: {result['output_dir']}")
    print(f"导出文件: {len(result['files_exported'])} 个")
    if result.get('package_created'):
        print("独立包已创建在: rag_package/")


