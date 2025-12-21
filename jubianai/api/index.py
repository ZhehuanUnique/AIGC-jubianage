"""
Vercel Serverless Function 入口
将 FastAPI 应用适配为 Vercel Serverless Function
"""
import sys
import os
from pathlib import Path
import traceback

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 延迟初始化数据库（在第一次请求时初始化，而不是在模块加载时）
# 这样可以避免在 Vercel Serverless Functions 冷启动时因为数据库连接问题导致整个函数崩溃

try:
    # 导入 FastAPI 应用
    from backend.api import app
    from mangum import Mangum
    
    # 使用 Mangum 将 FastAPI 适配为 ASGI
    handler = Mangum(app, lifespan="off")
    
    print("FastAPI app initialized successfully")
except Exception as e:
    # 如果导入失败，创建一个简单的错误处理函数
    error_msg = str(e)
    error_traceback = traceback.format_exc()
    print(f"Error initializing FastAPI app: {error_msg}")
    print(error_traceback)
    
    # 创建一个简单的错误处理函数
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Application initialization error: {error_msg}",
            "headers": {"Content-Type": "application/json"}
        }

