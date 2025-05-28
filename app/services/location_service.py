from app.utils.amap_util import AmapClient


class LocationService:
    @staticmethod
    def get_districts(keywords=None, subdistrict=1):
        """
        获取行政区域
        """
        result = AmapClient.get_districts(keywords, subdistrict)

        if result.get("status") != "1":
            return None, result.get("info", "获取行政区域失败")

        return {"districts": result.get("districts", [])}, None

    @staticmethod
    def search_places(keyword, city=None, page=1, page_size=20):
        """
        搜索地点
        """
        result = AmapClient.search_places(keyword, city, page, page_size)

        if result.get("status") != "1":
            return None, result.get("info", "搜索地点失败")

        pois = result.get("pois", [])
        locations = []

        for poi in pois:
            location = {
                "id": poi.get("id"),
                "name": poi.get("name"),
                "type": poi.get("type").split(";")[0] if poi.get("type") else "",
                "address": poi.get("address"),
                "location": poi.get("location"),
                "district": poi.get("adname"),
                "city": poi.get("cityname"),
                "province": poi.get("pname")
            }

            # 获取图片
            if "photos" in poi and poi["photos"]:
                location["image_url"] = poi["photos"][0].get("url")

            locations.append(location)

        return {
            "total": int(result.get("count", 0)),
            "locations": locations
        }, None

    @staticmethod
    def get_place_detail(place_id):
        """
        获取地点详情
        """
        result = AmapClient.get_place_detail(place_id)

        if result.get("status") != "1":
            return None, result.get("info", "获取地点详情失败")

        pois = result.get("pois", [])
        if not pois:
            return None, "地点不存在"

        poi = pois[0]
        detail = {
            "id": poi.get("id"),
            "name": poi.get("name"),
            "type": poi.get("type").split(";")[0] if poi.get("type") else "",
            "type_code": poi.get("typecode"),
            "address": poi.get("address"),
            "location": poi.get("location"),
            "district": poi.get("adname"),
            "city": poi.get("cityname"),
            "province": poi.get("pname"),
            "tel": poi.get("tel"),
            "website": poi.get("website"),
            "business_hours": poi.get("business_hours")
        }

        # 评分和价格
        if "biz_ext" in poi:
            detail["rating"] = float(poi["biz_ext"].get("rating", 0))
            detail["price"] = float(poi["biz_ext"].get("cost", 0))

        # 图片
        if "photos" in poi and poi["photos"]:
            detail["images"] = [photo.get("url") for photo in poi["photos"]]

        # 标签
        if "tag" in poi:
            detail["tags"] = poi["tag"].split(",")

        return detail, None

    @staticmethod
    def search_around(location, radius=3000, types=None, page=1, page_size=20):
        """
        周边搜索
        """
        result = AmapClient.search_around(location, radius, types, page, page_size)

        if result.get("status") != "1":
            return None, result.get("info", "周边搜索失败")

        pois = result.get("pois", [])
        locations = []

        for poi in pois:
            location_item = {
                "id": poi.get("id"),
                "name": poi.get("name"),
                "type": poi.get("type").split(";")[0] if poi.get("type") else "",
                "address": poi.get("address"),
                "location": poi.get("location"),
                "distance": int(poi.get("distance", 0)),
                "district": poi.get("adname"),
                "city": poi.get("cityname"),
                "province": poi.get("pname"),
                "tel": poi.get("tel"),
                "business_hours": poi.get("business_hours")
            }

            # 评分和价格
            if "biz_ext" in poi:
                location_item["rating"] = float(poi["biz_ext"].get("rating", 0))
                location_item["price"] = float(poi["biz_ext"].get("cost", 0))

            locations.append(location_item)

        return {
            "total": int(result.get("count", 0)),
            "locations": locations
        }, None
