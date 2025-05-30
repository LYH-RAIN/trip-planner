from fastapi import HTTPException, status

class TripPlannerException(Exception):
    def __init__(self, message: str, code: int = 50001):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AuthenticationError(TripPlannerException):
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 40101)

class PermissionError(TripPlannerException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 40301)

class NotFoundError(TripPlannerException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, 40401)

class ValidationError(TripPlannerException):
    def __init__(self, message: str = "参数错误"):
        super().__init__(message, 40001)
