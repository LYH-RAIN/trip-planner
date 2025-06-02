from flask_jwt_extended import create_access_token
from datetime import datetime

def generate_token(user_id):
    """
    鐢熸垚JWT浠ょ墝
    """
    return create_access_token(identity=user_id)
