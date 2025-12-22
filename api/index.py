"""
Vercel Serverless Function 入口
标准位置：根目录的 api/ 目录
"""
import json
from http.server import BaseHTTPRequestHandler
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
jubianai_path = project_root / "jubianai"
if str(jubianai_path) not in sys.path:
    sys.path.insert(0, str(jubianai_path))
    sys.path.insert(0, str(project_root))

class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime 的标准 handler 类"""
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        path = self.path.split('?')[0]
        
        # 只处理 API 路径
        if not path.startswith('/api/'):
            # 非 API 路径返回 404（应该由静态文件处理）
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found', 'path': path, 'message': 'This endpoint only handles /api/* requests'}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return
        
        # 尝试调用 FastAPI 处理所有 API 路由
        try:
            from jubianai.backend.api import app
            from starlette.testclient import TestClient
            
            client = TestClient(app)
            fastapi_response = client.get(path)
            
            # 发送响应
            self.send_response(fastapi_response.status_code)
            
            # 复制响应头
            for header_name, header_value in fastapi_response.headers.items():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(header_name, header_value)
            
            # 确保 CORS 头
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 发送响应体
            self.wfile.write(fastapi_response.content)
            
        except ImportError as e:
            # 如果无法导入 FastAPI，返回简单的响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 简单的健康检查
            if path == '/api/health':
                response = {'status': 'ok', 'message': '后端服务运行正常'}
            elif path == '/api/v1/assets/list':
                response = {'assets': [], 'count': 0}
            elif path == '/api/v1/assets/characters':
                response = {'characters': [], 'count': 0}
            else:
                self.send_response(404)
                response = {'error': 'Not found', 'path': path, 'message': f'FastAPI not available: {str(e)}'}
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            # 其他错误
            import traceback
            error_traceback = traceback.format_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'error': str(e),
                'message': '处理请求时出错',
                'traceback': error_traceback[:500]
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        path = self.path.split('?')[0]
        
        # 只处理 API 路径
        if not path.startswith('/api/'):
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'error': 'Not found', 'path': path}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        try:
            data = json.loads(body.decode('utf-8')) if body else {}
        except:
            data = {}
        
        # 尝试调用 FastAPI 处理所有 POST 请求
        try:
            from jubianai.backend.api import app
            from starlette.testclient import TestClient
            
            client = TestClient(app)
            fastapi_response = client.post(path, json=data)
            
            # 发送响应
            self.send_response(fastapi_response.status_code)
            
            # 复制响应头
            for header_name, header_value in fastapi_response.headers.items():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(header_name, header_value)
            
            # 确保 CORS 头
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 发送响应体
            self.wfile.write(fastapi_response.content)
            return
            
        except ImportError as e:
            # 如果无法导入 FastAPI，返回错误
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'error': f'FastAPI not available: {str(e)}',
                'message': '后端服务配置错误',
                'path': path
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            # 其他错误
            import traceback
            error_traceback = traceback.format_exc()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'error': str(e),
                'message': '处理请求时出错',
                'traceback': error_traceback[:500],
                'path': path
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


