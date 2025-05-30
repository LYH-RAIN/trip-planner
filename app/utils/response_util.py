def success_response(data=None, message="success"):
    """
    成功响应
    """
    return {
        "code": 0,
        "message": message,
        "data": data
    }

def error_response(code=1, message="error", data=None):
    """
    错误响应
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }
