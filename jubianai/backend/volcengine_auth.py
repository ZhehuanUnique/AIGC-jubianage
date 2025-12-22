"""
火山引擎 API 签名认证工具
用于即梦 AI API 的 AK/SK 认证
"""
import hmac
import hashlib
import base64
import time
from datetime import datetime
from typing import Dict, Any
from urllib.parse import quote


def generate_signature(
    access_key_id: str,
    secret_access_key: str,
    method: str,
    uri: str,
    query: Dict[str, Any] = None,
    headers: Dict[str, str] = None,
    body: str = ""
) -> Dict[str, str]:
    """
    生成火山引擎 API 签名
    
    Args:
        access_key_id: Access Key ID
        secret_access_key: Secret Access Key (base64 解码后的)
        method: HTTP 方法 (GET, POST, etc.)
        uri: 请求 URI 路径
        query: 查询参数
        headers: 请求头
        body: 请求体字符串
    
    Returns:
        包含签名信息的字典，用于设置 Authorization 头
    """
    # 解码 Secret Access Key (base64)
    try:
        secret_key = base64.b64decode(secret_access_key).decode('utf-8')
    except Exception:
        # 如果不是 base64，直接使用
        secret_key = secret_access_key
    
    # 时间戳
    timestamp = str(int(time.time()))
    date = datetime.utcnow().strftime('%Y%m%d')
    
    # 构建规范请求
    canonical_uri = uri
    canonical_querystring = ""
    if query:
        sorted_query = sorted(query.items())
        canonical_querystring = "&".join([f"{k}={quote(str(v), safe='')}" for k, v in sorted_query])
    
    # 规范头
    canonical_headers = ""
    signed_headers = ""
    if headers:
        sorted_headers = sorted([(k.lower(), v) for k, v in headers.items()])
        canonical_headers = "\n".join([f"{k}:{v}" for k, v in sorted_headers])
        signed_headers = ";".join([k for k, v in sorted_headers])
    
    # 请求体哈希
    body_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
    
    # 构建待签名字符串
    canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{body_hash}"
    
    # 计算签名
    algorithm = "HMAC-SHA256"
    credential_scope = f"{date}/cn-north-1/visual/request"
    string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    
    # 计算签名密钥
    k_date = hmac.new(f"volc{secret_key}".encode('utf-8'), date.encode('utf-8'), hashlib.sha256).digest()
    k_region = hmac.new(k_date, "cn-north-1".encode('utf-8'), hashlib.sha256).digest()
    k_service = hmac.new(k_region, "visual".encode('utf-8'), hashlib.sha256).digest()
    k_signing = hmac.new(k_service, "request".encode('utf-8'), hashlib.sha256).digest()
    
    # 计算最终签名
    signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # 构建 Authorization 头
    authorization = f"{algorithm} Credential={access_key_id}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    
    return {
        "Authorization": authorization,
        "X-Date": timestamp,
    }


def generate_simple_signature(
    access_key_id: str,
    secret_access_key: str,
    method: str,
    uri: str,
    body: str = ""
) -> Dict[str, str]:
    """
    简化版签名（适用于某些火山引擎 API）
    
    如果上面的签名方式不工作，可以尝试这个简化版本
    """
    # 解码 Secret Access Key
    try:
        secret_key = base64.b64decode(secret_access_key).decode('utf-8')
    except Exception:
        secret_key = secret_access_key
    
    # 时间戳
    timestamp = str(int(time.time()))
    
    # 构建待签名字符串
    string_to_sign = f"{method}\n{uri}\n{body}\n{timestamp}"
    
    # 计算签名
    signature = base64.b64encode(
        hmac.new(
            secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    return {
        "Authorization": f"HMAC-SHA256 Credential={access_key_id}, Signature={signature}",
        "X-Date": timestamp,
    }

