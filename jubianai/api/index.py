"""
Vercel Serverless Function 入口 - 最基础版本
"""
import json

def handler(event, context):
    """最简单的 handler 函数"""
    try:
        path = event.get('path', '/')
        
        # 根据路径返回不同的响应
        if path == '/':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'message': '视频生成 API 服务',
                    'version': '1.0.0',
                    'status': 'running'
                })
            }
        elif path == '/health':
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
        elif path == '/api/v1/assets/list':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({})
            }
        elif path == '/api/v1/assets/characters':
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
                'body': json.dumps({'error': 'Not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }
