"""
Vercel Serverless Function 入口
直接调用 FastAPI 应用的路由处理
"""
import os
import sys
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler
import asyncio

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 全局变量存储 FastAPI 应用
_app = None

def get_app():
    """获取 FastAPI 应用实例（延迟加载）"""
    global _app
    if _app is None:
        try:
            from backend.api import app
            _app = app
        except Exception as e:
            print(f"Error importing FastAPI app: {e}")
            import traceback
            traceback.print_exc()
            _app = None
    return _app

class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime 的标准 handler 类"""
    
    def log_message(self, format, *args):
        """重写 log_message 方法，避免日志错误"""
        pass
    
    def do_GET(self):
        """处理 GET 请求"""
        self.handle_request()
    
    def do_POST(self):
        """处理 POST 请求"""
        self.handle_request()
    
    def do_OPTIONS(self):
        """处理 OPTIONS 请求（CORS 预检）"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_PUT(self):
        """处理 PUT 请求"""
        self.handle_request()
    
    def do_DELETE(self):
        """处理 DELETE 请求"""
        self.handle_request()
    
    def send_cors_headers(self):
        """发送 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    def handle_request(self):
        """处理请求"""
        try:
            app = get_app()
            if app is None:
                self.send_json_response(500, {
                    'error': 'FastAPI app not initialized',
                    'message': '后端服务初始化失败，请检查日志'
                })
                return
            
            # 使用 TestClient 同步调用 FastAPI 应用
            from starlette.testclient import TestClient
            client = TestClient(app)
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            # 解析路径和查询参数
            path_parts = self.path.split('?', 1)
            path = path_parts[0]
            query_string = path_parts[1] if len(path_parts) > 1 else ''
            
            # 准备请求头
            headers = {}
            for key, value in self.headers.items():
                # 跳过一些不需要的头
                if key.lower() not in ['host', 'connection', 'content-length']:
                    headers[key] = value
            
            # 调用 FastAPI 应用
            try:
                if self.command == 'GET':
                    response = client.get(path, params=query_string, headers=headers)
                elif self.command == 'POST':
                    response = client.post(path, content=body, headers=headers)
                elif self.command == 'PUT':
                    response = client.put(path, content=body, headers=headers)
                elif self.command == 'DELETE':
                    response = client.delete(path, headers=headers)
                else:
                    self.send_json_response(405, {'error': f'Method {self.command} not allowed'})
                    return
                
                # 发送响应
                self.send_response(response.status_code)
                
                # 发送响应头（排除一些不需要的头）
                for key, value in response.headers.items():
                    key_lower = key.lower()
                    if key_lower not in ['content-length', 'transfer-encoding', 'connection']:
                        self.send_header(key, value)
                
                self.send_cors_headers()
                self.end_headers()
                
                # 发送响应体
                self.wfile.write(response.content)
                
            except Exception as e:
                import traceback
                error_msg = str(e)
                error_traceback = traceback.format_exc()
                print(f"Error calling FastAPI: {error_msg}")
                print(error_traceback)
                self.send_json_response(500, {
                    'error': error_msg,
                    'traceback': error_traceback,
                    'message': 'FastAPI 调用失败'
                })
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            error_traceback = traceback.format_exc()
            print(f"Error handling request: {error_msg}")
            print(error_traceback)
            self.send_json_response(500, {
                'error': error_msg,
                'traceback': error_traceback,
                'message': 'Internal server error'
            })
    
    def send_json_response(self, status_code, data):
        """发送 JSON 响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
