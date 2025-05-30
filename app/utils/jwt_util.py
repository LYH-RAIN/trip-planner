from flask_jwt_extended import create_access_token
from datetime import datetime

def generate_token(user_id):
    """
    生成JWT令牌
    """
    return create_access_token(identity=user_id)
