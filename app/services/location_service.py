import httpx
from typing import List, Optional
from app.core.config import settings
from app.core.exceptions import ValidationError
from app.schemas.location import (
    LocationSearchResponse, LocationDetailResponse, LocationAroundResponse,
    LocationListResponse, LocationAroundListResponse
)


class LocationService:
    def __init__(self):
        self.base_url = settings.AMAP_BASE_URL
        self.api_key = settings.AMAP_API_KEY

    async def search_locations(
            self,
            keyword: str,
            city: Optional[str] = None,
            page: int = 1,
            page_size: int = 20
    ) -> LocationListResponse:
        """搜索地点"""
        url = f"{self.base_url}/place/text"
        params = {
            "key": self.api_key,
            "keywords": keyword,
            "types": "",
            "city": city or "",
            "children": 1,
            "offset": page_size,
            "page": page,
            "extensions": "all"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if data.get("status") != "1":
                raise ValidationError(f"搜索失败: {data.get('info')}")

            pois = data.get("pois", [])
            total = int(data.get("count", 0))

            locations = []
            for poi in pois:
                location = LocationSearchResponse(
                    id=poi.get("id"),
                    name=poi.get("name"),
                    type=poi.get("type"),
                    address=poi.get("address"),
                    location=poi.get("location"),
                    district=poi.get("adname"),
                    city=poi.get("cityname"),
                    province=poi.get("pname"),
                    image_url=self._get_poi_image(poi)
                )
                locations.append(location)

            return LocationListResponse(total=total, locations=locations)

    async def get_location_detail(self, location_id: str) -> LocationDetailResponse:
        url = f"{self.base_url}/place/detail"
        params = {
            "key": self.api_key,
            "id": location_id,
            "extensions": "all"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if data.get("status") != "1":
                raise ValidationError(f"鑾峰彇璇︽儏澶辫触: {data.get('info')}")

            pois = data.get("pois", [])
            if not pois:
                raise ValidationError("地点不存在")

            poi = pois[0]

            return LocationDetailResponse(
                id=poi.get("id"),
                name=poi.get("name"),
                type=poi.get("type"),
                type_code=poi.get("typecode"),
                address=poi.get("address"),
                location=poi.get("location"),
                district=poi.get("adname"),
                city=poi.get("cityname"),
                province=poi.get("pname"),
                tel=poi.get("tel"),
                website=poi.get("website"),
                business_hours=self._format_business_hours(poi.get("business")),
                rating=self._parse_rating(poi.get("rating")),
                price=self._parse_price(poi.get("cost")),
                images=self._get_poi_images(poi),
                tags=self._parse_tags(poi.get("tag")),
                description=poi.get("introduction"),
                transportation=poi.get("traffic"),
                tips=poi.get("tips")
            )

    async def search_around(
            self,
            location: str,
            radius: int = 3000,
            search_type: Optional[str] = None,
            page: int = 1,
            page_size: int = 20
    ) -> LocationAroundListResponse:
        url = f"{self.base_url}/place/around"
        params = {
            "key": self.api_key,
            "location": location,
            "radius": radius,
            "types": self._get_type_code(search_type) if search_type else "",
            "sortrule": "distance",
            "offset": page_size,
            "page": page,
            "extensions": "all"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if data.get("status") != "1":
                raise ValidationError(f": {data.get('info')}")

            pois = data.get("pois", [])
            total = int(data.get("count", 0))

            locations = []
            for poi in pois:
                location_item = LocationAroundResponse(
                    id=poi.get("id"),
                    name=poi.get("name"),
                    type=poi.get("type"),
                    address=poi.get("address"),
                    location=poi.get("location"),
                    district=poi.get("adname"),
                    city=poi.get("cityname"),
                    province=poi.get("pname"),
                    distance=int(poi.get("distance", 0)),
                    tel=poi.get("tel"),
                    business_hours=self._format_business_hours(poi.get("business")),
                    rating=self._parse_rating(poi.get("rating")),
                    price=self._parse_price(poi.get("cost"))
                )
                locations.append(location_item)

            return LocationAroundListResponse(total=total, locations=locations)

    def _get_poi_image(self, poi: dict) -> Optional[str]:
        photos = poi.get("photos", [])
        if photos:
            return photos[0].get("url")
        return None

    def _get_poi_images(self, poi: dict) -> List[str]:
        photos = poi.get("photos", [])
        return [photo.get("url") for photo in photos if photo.get("url")]

    def _format_business_hours(self, business: dict) -> Optional[str]:
        if not business:
            return None
        return business.get("opentime")

    def _parse_rating(self, rating: str) -> Optional[float]:
        if not rating:
            return None
        try:
            return float(rating)
        except:
            return None

    def _parse_price(self, cost: str) -> Optional[float]:
        if not cost:
            return None
        try:
            return float(cost)
        except:
            return None

    def _parse_tags(self, tag: str) -> List[str]:
        if not tag:
            return []
        return [t.strip() for t in tag.split(";") if t.strip()]

    def _get_type_code(self, search_type: str) -> str:
        """"""
        type_mapping = {
            "餐饮": "050000",
            "住宿": "100000",
            "景点": "110000",
            "购物": "060000",
            "生活服务": "070000",
            "交通设施": "150000"
        }
        return type_mapping.get(search_type, "")
