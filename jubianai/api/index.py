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

# 导入 FastAPI 应用
from backend.api import app
from mangum import Mangum

# 使用 Mangum 将 FastAPI 适配为 ASGI
handler = Mangum(app, lifespan="off")

