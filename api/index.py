"""
Vercel Serverless Function 入口（简化版）
只提供健康检查和简单的 API 代理，不导入 FastAPI 以避免超过大小限制
"""
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime 的标准 handler 类"""
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        path = self.path.split('?')[0]
        
        # 只处理 API 路径
        if not path.startswith('/api/'):
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found', 'path': path}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return
        
        # 简单的健康检查
        if path == '/api/health' or path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'ok',
                'message': 'API 服务运行正常（简化版）',
                'note': '后端 API 需要单独部署，请使用独立的后端服务地址'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return
        
        # 其他 API 路径返回提示信息
        self.send_response(503)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            'error': 'Service Unavailable',
            'message': '后端 API 需要单独部署',
            'path': path,
            'note': '请将后端 API 部署到 Railway、Render 或其他平台，然后在 Streamlit 中配置 BACKEND_URL'
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
        
        # 返回提示信息
        self.send_response(503)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            'error': 'Service Unavailable',
            'message': '后端 API 需要单独部署',
            'path': path,
            'note': '请将后端 API 部署到 Railway、Render 或其他平台，然后在 Streamlit 中配置 BACKEND_URL'
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


