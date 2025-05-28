import os
import pytest
import tempfile
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db as _db
from app.models.user import User
from app.models.trip import Trip


# 测试配置类
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    AMAP_KEY = os.environ.get('TEST_AMAP_KEY', 'test-amap-key')
    WECHAT_APP_ID = 'test-wechat-app-id'
    WECHAT_APP_SECRET = 'test-wechat-app-secret'


@pytest.fixture(scope='session')
def app():
    """创建并配置一个Flask应用实例用于测试"""
    app = create_app(TestConfig)

    # 创建应用上下文
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """提供数据库会话"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """提供测试客户端"""
    return app.test_client()


@pytest.fixture(scope='function')
def test_user(db):
    """创建测试用户"""
    user = User(
        open_id='test_open_id',
        nickname='Test User',
        avatar_url='http://example.com/avatar.jpg',
        gender=1
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def auth_headers(app, test_user):
    """创建带有JWT令牌的认证头"""
    from flask_jwt_extended import create_access_token

    with app.app_context():
        access_token = create_access_token(identity=test_user.id)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        return headers


@pytest.fixture(scope='function')
def test_trip(db, test_user):
    """创建测试行程"""
    from datetime import date, timedelta

    start_date = date.today()
    end_date = start_date + timedelta(days=3)

    trip = Trip(
        user_id=test_user.id,
        title='Test Trip',
        start_date=start_date,
        end_date=end_date,
        days=4,
        departure='广州',
        status=0
    )
    trip.set_destinations(['韶关', '清远'])
    trip.set_preferences(['自然风光', '摄影'])

    db.session.add(trip)
    db.session.commit()

    # 创建行程日程
    from app.models.trip_day import TripDay
    for i in range(4):
        day_date = start_date + timedelta(days=i)
        trip_day = TripDay(
            trip_id=trip.id,
            day_index=i + 1,
            date=day_date,
            title=f'DAY{i + 1}',
            city='广州' if i == 0 else '韶关' if i < 3 else '清远'
        )
        db.session.add(trip_day)

    db.session.commit()
    return trip
