def success_response(data=None, message="success"):
    """
    鎴愬姛鍝嶅簲
    """
    return {
        "code": 0,
        "message": message,
        "data": data
    }

def error_response(code=1, message="error", data=None):
    """
    閿欒��鍝嶅簲
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }
