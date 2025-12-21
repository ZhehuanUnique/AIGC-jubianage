"""
Vercel Serverless Function 入口
使用 ASGI 适配器调用 FastAPI 应用
"""
import os
import sys
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import asyncio

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 延迟导入 FastAPI 应用
app = None
try:
    from backend.api import app as fastapi_app
    app = fastapi_app
except Exception as e:
    print(f"Warning: Failed to import FastAPI app: {e}")
    import traceback
    traceback.print_exc()

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
    
    def send_cors_headers(self):
        """发送 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    def handle_request(self):
        """处理请求"""
        try:
            if app is None:
                self.send_json_response(500, {
                    'error': 'FastAPI app not initialized',
                    'message': '后端服务初始化失败，请检查日志'
                })
                return
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            # 解析路径和查询参数
            path_parts = self.path.split('?', 1)
            path = path_parts[0]
            query_string = path_parts[1].encode() if len(path_parts) > 1 else b''
            
            # 构建 ASGI scope
            headers = []
            for key, value in self.headers.items():
                headers.append((key.lower().encode(), value.encode()))
            
            scope = {
                'type': 'http',
                'method': self.command,
                'path': path,
                'query_string': query_string,
                'headers': headers,
                'server': ('localhost', 8000),
                'client': ('127.0.0.1', 0),
                'scheme': 'https',
            }
            
            # 创建消息接收器
            message_queue = asyncio.Queue()
            
            async def receive():
                if not message_queue.empty():
                    return await message_queue.get()
                return {'type': 'http.request', 'body': body, 'more_body': False}
            
            # 创建响应收集器
            response_status = None
            response_headers = []
            response_body_parts = []
            
            async def send(message):
                nonlocal response_status, response_headers
                if message['type'] == 'http.response.start':
                    response_status = message['status']
                    response_headers = message['headers']
                elif message['type'] == 'http.response.body':
                    response_body_parts.append(message.get('body', b''))
            
            # 运行 ASGI 应用
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # 将初始请求消息放入队列
            message_queue.put_nowait({
                'type': 'http.request',
                'body': body,
                'more_body': False
            })
            
            # 调用 ASGI 应用
            coro = app(scope, receive, send)
            loop.run_until_complete(coro)
            
            # 发送响应
            if response_status:
                self.send_response(response_status)
                for key, value in response_headers:
                    if key.lower() not in [b'content-length', b'transfer-encoding']:
                        self.send_header(key.decode(), value.decode())
                self.send_cors_headers()
                self.end_headers()
                
                # 发送响应体
                response_body = b''.join(response_body_parts)
                self.wfile.write(response_body)
            else:
                self.send_json_response(500, {
                    'error': 'No response from FastAPI app',
                    'message': '应用未返回响应'
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
