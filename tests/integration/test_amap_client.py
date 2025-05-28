import pytest
import os
from app.utils.amap_util import AmapClient

# 跳过真实API测试，除非明确设置环境变量
skip_real_api = pytest.mark.skipif(
    not os.environ.get('TEST_WITH_REAL_AMAP_API'),
    reason="需要设置TEST_WITH_REAL_AMAP_API环境变量才能运行真实API测试"
)


class TestAmapClient:
    @skip_real_api
    def test_get_districts_real(self, app):
        """测试真实高德API获取行政区域"""
        with app.app_context():
            result = AmapClient.get_districts(keywords='广东省')

            assert result['status'] == '1'
            districts = result.get('districts', [])
            assert len(districts) > 0

            # 验证返回的数据包含广东省
            found = False
            for district in districts:
                if district.get('name') == '广东省':
                    found = True
                    break

            assert found, "未找到广东省"

    @skip_real_api
    def test_search_places_real(self, app):
        """测试真实高德API搜索地点"""
        with app.app_context():
            result = AmapClient.search_places(keyword='丹霞山', city='韶关')

            assert result['status'] == '1'
            assert int(result.get('count', 0)) > 0

            # 验证返回的数据包含丹霞山
            found = False
            for poi in result.get('pois', []):
                if '丹霞山' in poi.get('name'):
                    found = True
                    break

            assert found, "未找到丹霞山"

    @skip_real_api
    def test_get_place_detail_real(self, app):
        """测试真实高德API获取地点详情"""
        with app.app_context():
            # 先搜索获取ID
            search_result = AmapClient.search_places(keyword='丹霞山', city='韶关')
            assert search_result['status'] == '1'

            pois = search_result.get('pois', [])
            if not pois:
                pytest.skip("未找到丹霞山，跳过测试")

            place_id = pois[0]['id']

            # 获取详情
            result = AmapClient.get_place_detail(place_id)

            assert result['status'] == '1'
            assert len(result.get('pois', [])) > 0
            assert '丹霞山' in result['pois'][0]['name']

    @skip_real_api
    def test_search_around_real(self, app):
        """测试真实高德API周边搜索"""
        with app.app_context():
            # 丹霞山坐标
            location = '113.736513,25.022758'

            result = AmapClient.search_around(location=location, radius=5000, types='餐饮')

            assert result['status'] == '1'
            assert int(result.get('count', 0)) >= 0  # 可能没有结果，但应该正常返回
