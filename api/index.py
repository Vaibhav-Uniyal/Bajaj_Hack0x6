import json

def handler(request, context):
    """Simple HTTP handler for Vercel"""
    
    # Get the path from the request
    path = request.get('path', '/')
    
    # Set response headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    # Handle different endpoints
    if path == '/':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Hello World',
                'status': 'deployed'
            })
        }
    
    elif path == '/api/v1/health':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'ok',
                'message': 'API is working'
            })
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({
                'error': 'Not found',
                'path': path
            })
        }
