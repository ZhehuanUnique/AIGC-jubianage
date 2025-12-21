"""
Vercel Serverless Function 入口
简化版本，直接处理请求
"""
import os
import sys
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
            path = self.path.split('?')[0]  # 移除查询参数
            
            # 健康检查
            if path == '/' or path == '/health':
                self.send_json_response(200, {
                    'status': 'ok',
                    'message': '后端服务运行正常'
                })
                return
            
            # 资产管理列表 - 简化版本，直接返回空列表
            if path == '/api/v1/assets/list':
                self.send_json_response(200, {
                    'assets': [],
                    'count': 0
                })
                return
            
            # 角色列表
            if path == '/api/v1/assets/characters':
                self.send_json_response(200, {
                    'characters': [],
                    'count': 0
                })
                return
            
            # 视频生成 - 尝试调用 FastAPI
            if path == '/api/v1/video/generate':
                self.handle_video_generate()
                return
            
            # 视频状态查询
            if path.startswith('/api/v1/video/status/'):
                task_id = path.split('/')[-1]
                self.send_json_response(200, {
                    'status': 'pending',
                    'task_id': task_id,
                    'message': '任务处理中'
                })
                return
            
            # 其他路径返回 404
            self.send_json_response(404, {
                'error': 'Not found',
                'path': path
            })
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            error_traceback = traceback.format_exc()
            print(f"Error: {error_msg}")
            print(error_traceback)
            self.send_json_response(500, {
                'error': error_msg,
                'message': 'Internal server error'
            })
    
    def handle_video_generate(self):
        """处理视频生成请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            # 解析 JSON
            try:
                data = json.loads(body.decode('utf-8'))
            except:
                data = {}
            
            # 尝试调用 FastAPI
            try:
                from backend.api import app
                from starlette.testclient import TestClient
                
                client = TestClient(app)
                response = client.post('/api/v1/video/generate', json=data)
                
                # 发送响应
                self.send_response(response.status_code)
                for key, value in response.headers.items():
                    if key.lower() not in ['content-length', 'transfer-encoding', 'connection']:
                        self.send_header(key, value)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(response.content)
                return
                
            except Exception as e:
                # 如果 FastAPI 调用失败，返回错误
                import traceback
                print(f"FastAPI error: {e}")
                print(traceback.format_exc())
                self.send_json_response(500, {
                    'error': str(e),
                    'message': '视频生成服务暂时不可用'
                })
                return
                
        except Exception as e:
            import traceback
            print(f"Error in handle_video_generate: {e}")
            print(traceback.format_exc())
            self.send_json_response(500, {
                'error': str(e),
                'message': '处理视频生成请求时出错'
            })
    
    def send_json_response(self, status_code, data):
        """发送 JSON 响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
