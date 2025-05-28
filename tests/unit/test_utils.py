import pytest
from unittest.mock import patch, MagicMock
from app.utils.response_util import success_response, error_response
from app.utils.jwt_util import generate_token
from app.utils.amap_util import AmapClient


class TestResponseUtil:
    def test_success_response(self):
        """测试成功响应"""
        response = success_response(data={'id': 1}, message='success')
        assert response['code'] == 0
        assert response['message'] == 'success'
        assert response['data']['id'] == 1

    def test_error_response(self):
        """测试错误响应"""
        response = error_response(code=400, message='Bad Request')
        assert response['code'] == 400
        assert response['message'] == 'Bad Request'
        assert response['data'] is None


class TestJwtUtil:
    def test_generate_token(self, app):
        """测试生成JWT令牌"""
        with app.app_context():
            token = generate_token(1)
            assert token is not None
            assert isinstance(token, str)


class TestAmapUtil:
    @patch('app.utils.amap_util.requests.get')
    def test_get_districts(self, mock_get, app):
        """测试获取行政区域"""
        # 模拟高德API响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '1',
            'districts': [
                {
                    'name': '广东省',
                    'level': 'province',
                    'districts': [
                        {
                            'name': '广州市',
                            'level': 'city'
                        }
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response

        with app.app_context():
            result = AmapClient.get_districts(keywords='广东')

            # 验证请求参数
            args, kwargs = mock_get.call_args
            assert 'district' in kwargs['params']['keywords']

            # 验证结果
            assert result['status'] == '1'
            assert result['districts'][0]['name'] == '广东省'

    @patch('app.utils.amap_util.requests.get')
    def test_search_places(self, mock_get, app):
        """测试搜索地点"""
        # 模拟高德API响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '1',
            'count': '2',
            'pois': [
                {
                    'id': 'B0FFHCF6VV',
                    'name': '丹霞山',
                    'type': '风景名胜;风景区;国家级风景区',
                    'address': '广东省韶关市仁化县丹霞山镇',
                    'location': '113.736513,25.022758',
                    'pname': '广东省',
                    'cityname': '韶关市',
                    'adname': '仁化县'
                },
                {
                    'id': 'B0FFG9KCPD',
                    'name': '南华寺',
                    'type': '风景名胜;寺庙道观;寺庙',
                    'address': '广东省韶关市曲江区马坝镇',
                    'location': '113.601624,24.969615',
                    'pname': '广东省',
                    'cityname': '韶关市',
                    'adname': '曲江区'
                }
            ]
        }
        mock_get.return_value = mock_response

        with app.app_context():
            result = AmapClient.search_places(keyword='丹霞山', city='韶关')

            # 验证请求参数
            args, kwargs = mock_get.call_args
            assert kwargs['params']['keywords'] == '丹霞山'

            # 验证结果
            assert result['status'] == '1'
            assert result['count'] == '2'
            assert result['pois'][0]['name'] == '丹霞山'
