import pytest
import json
from datetime import date, timedelta


class TestTripFlow:
    """测试完整的行程流程"""

    def test_complete_trip_flow(self, client, auth_headers, test_user, db, monkeypatch):
        """测试完整的行程创建和查询流程"""
        # 1. 创建行程
        trip_data = {
            'title': 'Flow Test Trip',
            'departure': '广州',
            'destinations': ['韶关', '清远'],
            'startDate': date.today().strftime('%Y-%m-%d'),
            'endDate': (date.today() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'peopleCount': 2,
            'travelMode': 1,
            'preferences': ['自然风光', '摄影', '美食']
        }

        response = client.post(
            '/api/v1/trips',
            json=trip_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0

        trip_id = data['data']['id']

        # 2. 获取行程列表
        response = client.get(
            '/api/v1/trips',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['total'] >= 1

        # 确认新创建的行程在列表中
        found = False
        for trip in data['data']['list']:
            if trip['id'] == trip_id:
                found = True
                assert trip['title'] == 'Flow Test Trip'
                break

        assert found, "新创建的行程未在列表中找到"

        # 3. 获取行程详情
        response = client.get(
            f'/api/v1/trips/{trip_id}',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['id'] == trip_id
        assert data['data']['title'] == 'Flow Test Trip'
        assert len(data['data']['days_detail']) == 4

        # 4. 获取行程总览
        response = client.get(
            f'/api/v1/trips/{trip_id}/overview',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['id'] == trip_id
        assert len(data['data']['days_summary']) == 4

        # 5. 获取行程日程详情
        response = client.get(
            f'/api/v1/trips/{trip_id}/days/1',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['day_index'] == 1

        # 6. 取消行程
        response = client.post(
            f'/api/v1/trips/{trip_id}/cancel',
            json={'confirm': True},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['data']['id'] == trip_id
        assert data['data']['status'] == 2  # 已取消
