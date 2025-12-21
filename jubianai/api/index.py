"""
Vercel Serverless Function 入口
完全简化版本，直接处理所有请求
"""
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime 的标准 handler 类"""
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path.split('?')[0]
        
        if path == '/' or path == '/health':
            response = {'status': 'ok', 'message': '后端服务运行正常'}
        elif path == '/api/v1/assets/list':
            response = {'assets': [], 'count': 0}
        elif path == '/api/v1/assets/characters':
            response = {'characters': [], 'count': 0}
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'error': 'Not found', 'path': path}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path.split('?')[0]
        
        if path == '/api/v1/video/generate':
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            try:
                data = json.loads(body.decode('utf-8'))
            except:
                data = {}
            
            # 尝试调用 FastAPI - 添加更详细的错误处理
            try:
                import sys
                from pathlib import Path
                
                # 添加项目根目录到路径
                project_root = Path(__file__).parent.parent
                if str(project_root) not in sys.path:
                    sys.path.insert(0, str(project_root))
                
                # 尝试导入
                try:
                    from backend.api import app
                except ImportError as e:
                    # 如果导入失败，返回详细错误
                    response = {
                        'success': False,
                        'error': f'Failed to import FastAPI app: {str(e)}',
                        'message': '后端服务配置错误',
                        'sys_path': sys.path[:3]  # 只返回前3个路径，避免太长
                    }
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    return
                
                # 尝试使用 TestClient
                try:
                    from starlette.testclient import TestClient
                except ImportError as e:
                    response = {
                        'success': False,
                        'error': f'Failed to import TestClient: {str(e)}',
                        'message': '缺少 starlette 依赖'
                    }
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    return
                
                client = TestClient(app)
                response = client.post('/api/v1/video/generate', json=data)
                
                self.send_response(response.status_code)
                for key, value in response.headers.items():
                    if key.lower() not in ['content-length', 'transfer-encoding', 'connection']:
                        self.send_header(key, value)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response.content)
                return
                
            except Exception as e:
                import traceback
                error_traceback = traceback.format_exc()
                response = {
                    'success': False,
                    'error': str(e),
                    'message': '视频生成失败',
                    'traceback': error_traceback[:500]  # 只返回前500字符
                }
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'error': 'Not found', 'path': path}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
