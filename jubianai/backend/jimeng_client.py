"""
即梦 API 客户端（火山引擎）
用于调用即梦视频生成服务
支持图生视频：首帧和首尾帧两种模式
"""
import httpx
import hmac
import hashlib
import base64
import json
from datetime import datetime
from typing import Optional, Dict, Any, Union
import os

# 从环境变量获取配置
JIMENG_ACCESS_KEY_ID = os.getenv("JIMENG_ACCESS_KEY_ID", "")
JIMENG_SECRET_ACCESS_KEY = os.getenv("JIMENG_SECRET_ACCESS_KEY", "")
JIMENG_API_ENDPOINT = os.getenv("JIMENG_API_ENDPOINT", "https://visual.volcengineapi.com")
JIMENG_REGION = os.getenv("JIMENG_REGION", "cn-north-1")
JIMENG_SERVICE = os.getenv("JIMENG_SERVICE", "cv")


def generate_volcengine_signature(
    secret_key: str,
    method: str,
    uri: str,
    query_string: str,
    headers: Dict[str, str],
    body: str = ""
) -> str:
    """
    生成火山引擎 API 的签名（Signature V4）
    参考：https://www.volcengine.com/docs/6160/1099475
    """
    # 1. 构建规范请求（Canonical Request）
    canonical_headers = []
    signed_headers = []
    
    # 按字母顺序排序 headers
    sorted_headers = sorted([(k.lower(), v) for k, v in headers.items()])
    for key, value in sorted_headers:
        canonical_headers.append(f"{key}:{value.strip()}")
        signed_headers.append(key)
    
    canonical_headers_str = "\n".join(canonical_headers) + "\n"
    signed_headers_str = ";".join(signed_headers)
    
    # 构建规范请求
    canonical_request = f"{method}\n{uri}\n{query_string}\n{canonical_headers_str}\n{signed_headers_str}\n{hashlib.sha256(body.encode('utf-8')).hexdigest()}"
    
    # 2. 构建待签名字符串（String to Sign）
    algorithm = "HMAC-SHA256"
    request_date = headers.get("X-Date", datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))
    date_stamp = request_date[:8]  # YYYYMMDD
    credential_scope = f"{date_stamp}/{JIMENG_REGION}/{JIMENG_SERVICE}/request"
    
    string_to_sign = f"{algorithm}\n{request_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    
    # 3. 计算签名
    def sign(key: bytes, msg: str) -> bytes:
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    
    k_date = sign(f"volc{secret_key}".encode('utf-8'), date_stamp)
    k_region = sign(k_date, JIMENG_REGION)
    k_service = sign(k_region, JIMENG_SERVICE)
    k_signing = sign(k_service, "request")
    signature = sign(k_signing, string_to_sign)
    
    # 4. 返回签名（十六进制）
    return signature.hex()


async def generate_video_from_image_first_frame(
    image_base64: str,
    duration: int = 5,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    首帧图生视频接口
    根据文档：https://www.volcengine.com/docs/85621/1785204?lang=zh
    
    Args:
        image_base64: 首帧图片的 Base64 编码
        duration: 视频时长（秒），默认5秒
        access_key_id: AccessKeyId
        secret_access_key: SecretAccessKey
        **kwargs: 其他参数（如 prompt, negative_prompt 等）
    
    Returns:
        包含 task_id 或 video_url 的字典
    """
    # 使用提供的密钥或环境变量
    ak_id = access_key_id or JIMENG_ACCESS_KEY_ID
    ak_secret = secret_access_key or JIMENG_SECRET_ACCESS_KEY
    
    if not ak_id or not ak_secret:
        raise ValueError("即梦 API 密钥未配置，请设置 JIMENG_ACCESS_KEY_ID 和 JIMENG_SECRET_ACCESS_KEY")
    
    # 构建请求体
    request_body = {
        "req_key": "jimeng_video_gen_v3_720p",  # 720P 图生视频
        "image": image_base64,  # Base64 编码的图片
        "duration": duration,
    }
    
    # 添加可选参数
    if "prompt" in kwargs:
        request_body["prompt"] = kwargs["prompt"]
    if "negative_prompt" in kwargs:
        request_body["negative_prompt"] = kwargs["negative_prompt"]
    if "seed" in kwargs and kwargs["seed"] is not None:
        request_body["seed"] = kwargs["seed"]
    
    body_str = json.dumps(request_body, ensure_ascii=False)
    
    # 构建请求头
    request_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    headers = {
        "Content-Type": "application/json",
        "X-Date": request_date,
        "Authorization": f"HMAC-SHA256 Credential={ak_id}/{request_date[:8]}/{JIMENG_REGION}/{JIMENG_SERVICE}/request",
    }
    
    # 生成签名
    uri = "/"  # 火山引擎 API 路径
    query_string = ""  # 查询字符串
    signature = generate_volcengine_signature(ak_secret, "POST", uri, query_string, headers, body_str)
    headers["Authorization"] += f", Signature={signature}"
    
    # 发送请求
    url = f"{JIMENG_API_ENDPOINT}{uri}"
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                url,
                json=request_body,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if e.response else str(e)
        raise Exception(f"即梦 API 请求失败: {e.response.status_code} - {error_detail}")
    except Exception as e:
        raise Exception(f"调用即梦 API 时发生错误: {str(e)}")


async def generate_video_from_images_first_last(
    start_image_base64: str,
    end_image_base64: str,
    duration: int = 5,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    首尾帧图生视频接口
    根据文档：https://www.volcengine.com/docs/85621/1791184?lang=zh
    
    Args:
        start_image_base64: 首帧图片的 Base64 编码
        end_image_base64: 尾帧图片的 Base64 编码
        duration: 视频时长（秒），默认5秒
        access_key_id: AccessKeyId
        secret_access_key: SecretAccessKey
        **kwargs: 其他参数（如 prompt, negative_prompt 等）
    
    Returns:
        包含 task_id 或 video_url 的字典
    """
    # 使用提供的密钥或环境变量
    ak_id = access_key_id or JIMENG_ACCESS_KEY_ID
    ak_secret = secret_access_key or JIMENG_SECRET_ACCESS_KEY
    
    if not ak_id or not ak_secret:
        raise ValueError("即梦 API 密钥未配置，请设置 JIMENG_ACCESS_KEY_ID 和 JIMENG_SECRET_ACCESS_KEY")
    
    # 构建请求体
    request_body = {
        "req_key": "jimeng_video_gen_v3_720p",  # 720P 图生视频
        "start_image": start_image_base64,  # 首帧 Base64 编码
        "end_image": end_image_base64,  # 尾帧 Base64 编码
        "duration": duration,
    }
    
    # 添加可选参数
    if "prompt" in kwargs:
        request_body["prompt"] = kwargs["prompt"]
    if "negative_prompt" in kwargs:
        request_body["negative_prompt"] = kwargs["negative_prompt"]
    if "seed" in kwargs and kwargs["seed"] is not None:
        request_body["seed"] = kwargs["seed"]
    
    body_str = json.dumps(request_body, ensure_ascii=False)
    
    # 构建请求头
    request_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    headers = {
        "Content-Type": "application/json",
        "X-Date": request_date,
        "Authorization": f"HMAC-SHA256 Credential={ak_id}/{request_date[:8]}/{JIMENG_REGION}/{JIMENG_SERVICE}/request",
    }
    
    # 生成签名
    uri = "/"  # 火山引擎 API 路径
    query_string = ""  # 查询字符串
    signature = generate_volcengine_signature(ak_secret, "POST", uri, query_string, headers, body_str)
    headers["Authorization"] += f", Signature={signature}"
    
    # 发送请求
    url = f"{JIMENG_API_ENDPOINT}{uri}"
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                url,
                json=request_body,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if e.response else str(e)
        raise Exception(f"即梦 API 请求失败: {e.response.status_code} - {error_detail}")
    except Exception as e:
        raise Exception(f"调用即梦 API 时发生错误: {str(e)}")


async def check_video_status(
    task_id: str,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    查询视频生成状态
    
    Args:
        task_id: 任务 ID
        access_key_id: AccessKeyId
        secret_access_key: SecretAccessKey
    
    Returns:
        包含任务状态的字典
    """
    # 使用提供的密钥或环境变量
    ak_id = access_key_id or JIMENG_ACCESS_KEY_ID
    ak_secret = secret_access_key or JIMENG_SECRET_ACCESS_KEY
    
    if not ak_id or not ak_secret:
        raise ValueError("即梦 API 密钥未配置")
    
    # 构建请求体
    request_body = {
        "req_key": "jimeng_video_query",
        "task_id": task_id,
    }
    
    body_str = json.dumps(request_body, ensure_ascii=False)
    
    # 构建请求头
    request_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    headers = {
        "Content-Type": "application/json",
        "X-Date": request_date,
        "Authorization": f"HMAC-SHA256 Credential={ak_id}/{request_date[:8]}/{JIMENG_REGION}/{JIMENG_SERVICE}/request",
    }
    
    # 生成签名
    uri = "/"
    query_string = ""
    signature = generate_volcengine_signature(ak_secret, "POST", uri, query_string, headers, body_str)
    headers["Authorization"] += f", Signature={signature}"
    
    # 发送请求
    url = f"{JIMENG_API_ENDPOINT}{uri}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=request_body, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text if e.response else str(e)
        raise Exception(f"即梦 API 请求失败: {e.response.status_code} - {error_detail}")
    except Exception as e:
        raise Exception(f"调用即梦 API 时发生错误: {str(e)}")
