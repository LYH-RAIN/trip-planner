import pytest
from unittest.mock import patch, MagicMock
from datetime import date, datetime
from app.services.auth_service import AuthService
from app.services.trip_service import TripService
from app.models.user import User
from app.models.trip import Trip
from app.models.trip_day import TripDay


class TestAuthService:
    @patch('app.services.auth_service.requests.get')
    def test_wechat_login_success(self, mock_get, db):
        """测试微信登录成功"""
        # 模拟微信API响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'openid': 'test_openid_new',
            'session_key': 'test_session_key'
        }
        mock_get.return_value = mock_response

        # 调用服务
        result, error = AuthService.wechat_login('test_code')

        # 验证结果
        assert error is None
        assert 'token' in result
        assert result['user']['isNewUser'] is True

        # 验证用户是否创建
        user = User.query.filter_by(open_id='test_openid_new').first()
        assert user is not None

    @patch('app.services.auth_service.requests.get')
    def test_wechat_login_error(self, mock_get, db):
        """测试微信登录失败"""
        # 模拟微信API错误响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'errcode': 40029,
            'errmsg': 'invalid code'
        }
        mock_get.return_value = mock_response

        # 调用服务
        result, error = AuthService.wechat_login('invalid_code')

        # 验证结果
        assert result is None
        assert error == 'invalid code'


class TestTripService:
    def test_create_trip(self, db, test_user):
        """测试创建行程"""
        trip_data = {
            'title': 'New Trip',
            'departure': '广州',
            'destinations': ['深圳', '珠海'],
            'startDate': '2023-06-01',
            'endDate': '2023-06-03',
            'peopleCount': 2,
            'travelMode': 1,
            'preferences': ['美食', '购物']
        }

        result = TripService.create_trip(test_user.id, trip_data)

        assert result['title'] == 'New Trip'
        assert result['startDate'] == '2023-06-01'
        assert result['endDate'] == '2023-06-03'

        # 验证数据库中的行程
        trip = Trip.query.filter_by(title='New Trip').first()
        assert trip is not None
        assert trip.days == 3
        assert trip.departure == '广州'
        assert trip.people_count == 2

        # 验证行程日程
        days = TripDay.query.filter_by(trip_id=trip.id).all()
        assert len(days) == 3

    def test_get_trip_list(self, db, test_trip):
        """测试获取行程列表"""
        # 创建另一个行程
        trip2 = Trip(
            user_id=test_trip.user_id,
            title='Another Trip',
            start_date=date(2023, 7, 1),
            end_date=date(2023, 7, 5),
            days=5,
            departure='深圳',
            status=1  # 已完成
        )
        db.session.add(trip2)
        db.session.commit()

        # 获取所有行程
        result = TripService.get_trip_list(test_trip.user_id)
        assert result['total'] == 2

        # 获取已完成的行程
        result = TripService.get_trip_list(test_trip.user_id, status='completed')
        assert result['total'] == 1
        assert result['list'][0]['title'] == 'Another Trip'

    def test_get_trip_detail(self, db, test_trip):
        """测试获取行程详情"""
        result, error = TripService.get_trip_detail(test_trip.id, test_trip.user_id)

        assert error is None
        assert result['id'] == test_trip.id
        assert result['title'] == test_trip.title
        assert len(result['days_detail']) == 4

    def test_cancel_trip(self, db, test_trip):
        """测试取消行程"""
        result, error = TripService.cancel_trip(test_trip.id, test_trip.user_id)

        assert error is None
        assert result['id'] == test_trip.id
        assert result['status'] == 2  # 已取消

        # 验证数据库中的状态
        trip = Trip.query.get(test_trip.id)
        assert trip.status == 2
