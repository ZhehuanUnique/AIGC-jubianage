"""
Vercel Serverless Function 入口
使用 Vercel Python runtime 的标准格式
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime 的标准 handler 类"""
    
    def log_message(self, format, *args):
        """重写 log_message 方法，避免日志错误"""
        # Vercel 环境中不需要标准输出日志
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def handle_request(self):
        """处理请求"""
        try:
            path = self.path.split('?')[0]  # 移除查询参数
            
            # 根据路径返回不同的响应
            if path == '/' or path == '':
                self.send_json_response(200, {
                    'message': '视频生成 API 服务',
                    'version': '1.0.0',
                    'status': 'running'
                })
            elif path == '/health':
                self.send_json_response(200, {
                    'status': 'healthy',
                    'database': 'not_configured'
                })
            elif path == '/api/v1/assets/list':
                self.send_json_response(200, {})
            elif path == '/api/v1/assets/characters':
                self.send_json_response(200, {
                    'characters': [],
                    'count': 0
                })
            else:
                self.send_json_response(404, {
                    'error': 'Not found',
                    'path': path
                })
        except Exception as e:
            import traceback
            error_msg = str(e)
            error_traceback = traceback.format_exc()
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
