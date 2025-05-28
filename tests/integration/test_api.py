import pytest
import json
from flask import url_for


class TestAuthAPI:
    @pytest.mark.parametrize('endpoint', [
        '/api/v1/trips',
        '/api/v1/locations/districts'
    ])
    def test_auth_required(self, client, endpoint):
        """测试需要认证的端点"""
        response = client.get(endpoint)
        assert response.status_code == 401

    def test_wechat_login(self, client, monkeypatch):
        """测试微信登录API"""

        # 模拟AuthService.wechat_login方法
        def mock_wechat_login(code):
            return {
                'token': 'test_token',
                'user': {
                    'id': 1,
                    'nickname': 'Test User',
                    'avatarUrl': 'http://example.com/avatar.jpg',
                    'isNewUser': False
                }
            }, None

        from app.services.auth_service import AuthService
        monkeypatch.setattr(AuthService, 'wechat_login', mock_wechat_login)

        response = client.post(
            '/api/v1/auth/wechat/login',
            json={'code': 'test_code'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['token'] == 'test_token'
        assert data['data']['user']['nickname'] == 'Test User'


class TestLocationAPI:
    def test_get_districts(self, client, auth_headers, monkeypatch):
        """测试获取行政区域API"""

        # 模拟LocationService.get_districts方法
        def mock_get_districts(keywords, subdistrict):
            return {
                'districts': [
                    {
                        'id': '440000',
                        'name': '广东省',
                        'center': '113.280637,23.125178',
                        'level': 'province',
                        'children': [
                            {
                                'id': '440100',
                                'name': '广州市',
                                'center': '113.280637,23.125178',
                                'level': 'city'
                            }
                        ]
                    }
                ]
            }, None

        from app.services.location_service import LocationService
        monkeypatch.setattr(LocationService, 'get_districts', mock_get_districts)

        response = client.get(
            '/api/v1/locations/districts?keywords=广东省',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['districts'][0]['name'] == '广东省'

    def test_search_places(self, client, auth_headers, monkeypatch):
        """测试搜索地点API"""

        # 模拟LocationService.search_places方法
        def mock_search_places(keyword, city, page, page_size):
            return {
                'total': 2,
                'locations': [
                    {
                        'id': 'B0FFHCF6VV',
                        'name': '丹霞山',
                        'type': '景点',
                        'address': '广东省韶关市仁化县丹霞山镇',
                        'location': '113.736513,25.022758',
                        'district': '仁化县',
                        'city': '韶关市',
                        'province': '广东省'
                    }
                ]
            }, None

        from app.services.location_service import LocationService
        monkeypatch.setattr(LocationService, 'search_places', mock_search_places)

        response = client.get(
            '/api/v1/locations/search?keyword=丹霞山&city=韶关',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['total'] == 2
        assert data['data']['locations'][0]['name'] == '丹霞山'


class TestTripAPI:
    def test_create_trip(self, client, auth_headers, monkeypatch):
        """测试创建行程API"""

        # 模拟TripService.create_trip方法
        def mock_create_trip(user_id, trip_data):
            return {
                'id': 1,
                'title': trip_data['title'],
                'startDate': trip_data['startDate'],
                'endDate': trip_data['endDate']
            }

        from app.services.trip_service import TripService
        monkeypatch.setattr(TripService, 'create_trip', mock_create_trip)

        response = client.post(
            '/api/v1/trips',
            json={
                'title': 'Test Trip',
                'departure': '广州',
                'destinations': ['韶关', '清远'],
                'startDate': '2023-05-07',
                'endDate': '2023-05-10',
                'peopleCount': 2,
                'travelMode': 1,
                'preferences': ['自然风光', '摄影', '美食']
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['title'] == 'Test Trip'

    def test_get_trip_list(self, client, auth_headers, monkeypatch):
        """测试获取行程列表API"""

        # 模拟TripService.get_trip_list方法
        def mock_get_trip_list(user_id, status, page, page_size):
            return {
                'total': 1,
                'list': [
                    {
                        'id': 1,
                        'title': 'Test Trip',
                        'cover_image': 'https://example.com/cover.jpg',
                        'startDate': '2023-05-07',
                        'endDate': '2023-05-10',
                        'days': 4,
                        'destinations': ['韶关', '清远'],
                        'status': 0,
                        'createdAt': '2023-04-20T12:00:00Z'
                    }
                ]
            }

        from app.services.trip_service import TripService
        monkeypatch.setattr(TripService, 'get_trip_list', mock_get_trip_list)

        response = client.get(
            '/api/v1/trips?status=all',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['total'] == 1
        assert data['data']['list'][0]['title'] == 'Test Trip'
