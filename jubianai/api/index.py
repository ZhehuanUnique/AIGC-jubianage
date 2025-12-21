"""
Vercel Serverless Function 入口
将 FastAPI 应用适配为 Vercel Serverless Function
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 在导入 app 之前初始化数据库（Vercel Serverless Functions 不支持 startup 事件）
try:
    from backend.database import init_db
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Database initialization error: {e}")
    # 不阻止应用启动，允许在没有数据库的情况下运行

# 导入 FastAPI 应用
from backend.api import app
from mangum import Mangum

# 使用 Mangum 将 FastAPI 适配为 ASGI
handler = Mangum(app, lifespan="off")

