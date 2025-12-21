"""
Vercel Serverless Function 入口
使用 Vercel Python runtime 的标准格式
"""
import json

def handler(request):
    """
    Vercel Python runtime 的标准 handler 格式
    request 是一个包含请求信息的对象
    """
    try:
        # 获取请求路径 - Vercel 的 request 对象可能有不同的属性
        if hasattr(request, 'path'):
            path = request.path
        elif isinstance(request, dict):
            path = request.get('path', '/')
        else:
            # 尝试从 URL 中提取路径
            path = getattr(request, 'url', '/').split('?')[0] if hasattr(request, 'url') else '/'
        
        # 移除查询参数
        if '?' in path:
            path = path.split('?')[0]
        
        # 根据路径返回不同的响应
        if path == '/' or path == '':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'message': '视频生成 API 服务',
                    'version': '1.0.0',
                    'status': 'running',
                    'path': path
                })
            }
        elif path == '/health' or path.endswith('/health'):
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'status': 'healthy',
                    'database': 'not_configured'
                })
            }
        elif path == '/api/v1/assets/list' or path.endswith('/api/v1/assets/list'):
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({})
            }
        elif path == '/api/v1/assets/characters' or path.endswith('/api/v1/assets/characters'):
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'characters': [],
                    'count': 0
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'error': 'Not found',
                    'path': path,
                    'request_type': str(type(request))
                })
            }
    except Exception as e:
        import traceback
        error_msg = str(e)
        error_traceback = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'error': error_msg,
                'traceback': error_traceback,
                'message': 'Internal server error',
                'request_type': str(type(request)) if 'request' in locals() else 'unknown'
            })
        }
