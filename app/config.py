import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://username:password@localhost/trip_planner'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    AMAP_KEY = os.environ.get('AMAP_KEY') or 'your-amap-key'
    WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID') or 'your-wechat-app-id'
    WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET') or 'your-wechat-app-secret'
