"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API 配置
API_KEY = os.getenv("API_KEY", "")
SEEDANCE_API_ENDPOINT = os.getenv("SEEDANCE_API_ENDPOINT", "")

# 即梦 AI (火山引擎) AK/SK 配置
# 注意：敏感信息请通过环境变量配置，不要硬编码在代码中
VOLCENGINE_ACCESS_KEY_ID = os.getenv("VOLCENGINE_ACCESS_KEY_ID", "")
VOLCENGINE_SECRET_ACCESS_KEY = os.getenv("VOLCENGINE_SECRET_ACCESS_KEY", "")

# 即梦 API 端点（根据文档调整）
# 即梦 API 使用 visual.volcengineapi.com（cv 服务通过 visual 端点访问）
JIMENG_API_ENDPOINT = os.getenv(
    "JIMENG_API_ENDPOINT",
    "https://visual.volcengineapi.com"
)

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

