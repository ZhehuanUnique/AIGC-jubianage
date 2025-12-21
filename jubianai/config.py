"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API 配置
API_KEY = os.getenv("API_KEY", "")
SEEDANCE_API_ENDPOINT = os.getenv("SEEDANCE_API_ENDPOINT", "")

# 即梦 API 配置（火山引擎）
JIMENG_ACCESS_KEY_ID = os.getenv("JIMENG_ACCESS_KEY_ID", "")
JIMENG_SECRET_ACCESS_KEY = os.getenv("JIMENG_SECRET_ACCESS_KEY", "")
JIMENG_API_ENDPOINT = os.getenv("JIMENG_API_ENDPOINT", "https://visual.volcengineapi.com")  # 火山引擎视觉API端点
JIMENG_REGION = os.getenv("JIMENG_REGION", "cn-north-1")  # 区域
JIMENG_SERVICE = os.getenv("JIMENG_SERVICE", "cv")  # 服务名称

# 服务器配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# 视频生成默认参数
DEFAULT_VIDEO_SETTINGS = {
    "width": 1024,
    "height": 576,
    "duration": 5,  # 秒
    "fps": 24,
}

