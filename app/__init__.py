from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    from app.api import auth_bp, location_bp, trip_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(location_bp, url_prefix='/api/v1/locations')
    app.register_blueprint(trip_bp, url_prefix='/api/v1/trips')

    return app
