import requests
from flask import current_app


class AmapClient:
    """楂樺痉鍦板浘API瀹㈡埛绔�"""

    @staticmethod
    def get_districts(keywords=None, subdistrict=1):
        """
        获取行政区域
        """
        url = "https://restapi.amap.com/v3/config/district"
        params = {
            "key": current_app.config["AMAP_KEY"],
            "subdistrict": subdistrict,
            "extensions": "base"
        }

        if keywords:
            params["keywords"] = keywords

        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def search_places(keyword, city=None, page=1, page_size=20):
        """
        搜索地点
        """
        url = "https://restapi.amap.com/v3/place/text"
        params = {
            "key": current_app.config["AMAP_KEY"],
            "keywords": keyword,
            "offset": page_size,
            "page": page,
            "extensions": "all"
        }

        if city:
            params["city"] = city

        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def get_place_detail(place_id):
        """
        获取地点详情
        """
        url = "https://restapi.amap.com/v3/place/detail"
        params = {
            "key": current_app.config["AMAP_KEY"],
            "id": place_id,
            "extensions": "all"
        }

        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def search_around(location, radius=3000, types=None, page=1, page_size=20):
        """
        周边搜索
        """
        url = "https://restapi.amap.com/v3/place/around"
        params = {
            "key": current_app.config["AMAP_KEY"],
            "location": location,
            "radius": radius,
            "offset": page_size,
            "page": page,
            "extensions": "all"
        }

        if types:
            params["types"] = types

        response = requests.get(url, params=params)
        return response.json()
