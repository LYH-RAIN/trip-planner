from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, date, time
from app.models.trip import Trip, TripDay, TripPlace, TripFood, TripTransportation
from app.models.user import User
from app.schemas.trip import (
    TripCreate, TripUpdate, TripResponse, TripListResponse,
    TripOverviewResponse, TripDayResponse, TripDayDetailResponse,
    TripDayUpdate, TripFoodsResponse, TripFoodResponse,
    ItineraryItem, WeatherInfo, AccommodationInfo, PointInfo,
    NavigationInfo, LocationPoint
)
from app.core.exceptions import NotFoundError, PermissionError, ValidationError
from app.services.weather_service import WeatherService


class TripService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()

    def create_trip(self, trip_data: TripCreate, user_id: int) -> TripResponse:
        """创建行程"""
        # 计算行程天数
        days = (trip_data.end_datetime.date() - trip_data.start_datetime.date()).days + 1

        # 创建行程
        trip = Trip(
            user_id=user_id,
            days=days,
            **trip_data.dict()
        )

        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)

        # 创建每日行程框架
        self._create_trip_days(trip)

        return TripResponse.from_orm(trip)

    def get_trips(
            self,
            user_id: int,
            status: Optional[str] = None,
            trip_id: Optional[int] = None,
            page: int = 1,
            page_size: int = 20
    ) -> TripListResponse:
        """获取行程列表"""
        query = self.db.query(Trip).filter(Trip.user_id == user_id)

        # 状态筛选
        if status and status != "all":
            status_map = {
                "planning": 0,
                "completed": 1,
                "cancelled": 2
            }
            if status in status_map:
                query = query.filter(Trip.status == status_map[status])

        # 特定行程
        if trip_id:
            query = query.filter(Trip.id == trip_id)

        # 分页
        total = query.count()
        trips = query.order_by(desc(Trip.created_at)).offset((page - 1) * page_size).limit(page_size).all()

        return TripListResponse(
            total=total,
            trips=[TripResponse.from_orm(trip) for trip in trips]
        )

    def get_trip_overview(self, trip_id: int, user_id: int) -> TripOverviewResponse:
        """获取行程总览"""
        trip = self._get_trip_with_permission(trip_id, user_id)

        # 获取行程天数信息
        days = self.db.query(TripDay).filter(TripDay.trip_id == trip_id).order_by(TripDay.day_index).all()

        # 获取亮点景点
        highlights = self.db.query(TripPlace).filter(
            and_(TripPlace.trip_id == trip_id, TripPlace.is_highlight == 1)
        ).all()

        total_highlights = [
            {
                "name": place.name,
                "image_url": place.image_url,
                "day_index": place.day_index
            }
            for place in highlights
        ]

        return TripOverviewResponse(
            trip_info=TripResponse.from_orm(trip),
            days_list=[self._build_trip_day_response(day) for day in days],
            total_highlights=total_highlights
        )

    def get_trip_day_detail(self, trip_id: int, day_index: int, user_id: int) -> TripDayDetailResponse:
        """获取行程日程详情"""
        trip = self._get_trip_with_permission(trip_id, user_id)

        day = self.db.query(TripDay).filter(
            and_(TripDay.trip_id == trip_id, TripDay.day_index == day_index)
        ).first()

        if not day:
            raise NotFoundError("行程日程不存在")

        # 构建行程安排
        itinerary = self._build_itinerary(day)

        return TripDayDetailResponse(
            trip_id=trip_id,
            date=day.date,
            title=day.title,
            city=day.city,
            weather=self._build_weather_info(day),
            total_places=day.place_count,
            itinerary=itinerary
        )

    def update_trip_day(self, trip_id: int, day_index: int, day_data: TripDayUpdate,
                        user_id: int) -> TripDayDetailResponse:
        """更新行程日程"""
        trip = self._get_trip_with_permission(trip_id, user_id)

        day = self.db.query(TripDay).filter(
            and_(TripDay.trip_id == trip_id, TripDay.day_index == day_index)
        ).first()

        if not day:
            raise NotFoundError("行程日程不存在")

        # 更新基本信息
        for field, value in day_data.dict(exclude_unset=True,
                                          exclude={"accommodation", "start_point", "end_point", "weather",
                                                   "itinerary"}).items():
            setattr(day, field, value)

        # 更新住宿信息
        if day_data.accommodation:
            acc = day_data.accommodation
            day.accommodation_name = acc.name
            day.accommodation_address = acc.address
            day.accommodation_price = acc.price
            day.accommodation_rating = acc.rating
            day.accommodation_latitude = acc.latitude
            day.accommodation_longitude = acc.longitude
            day.accommodation_contact = acc.contact

        # 更新起终点信息
        if day_data.start_point:
            day.start_point_name = day_data.start_point.name
            day.start_point_time = day_data.start_point.time
            day.start_point_type = day_data.start_point.type

        if day_data.end_point:
            day.end_point_name = day_data.end_point.name
            day.end_point_time = day_data.end_point.time
            day.end_point_type = day_data.end_point.type

        # 更新天气信息
        if day_data.weather:
            weather = day_data.weather
            day.weather_condition = weather.condition
            day.temperature = weather.temperature
            day.weather_icon = weather.icon
            day.humidity = weather.humidity
            day.wind = weather.wind
            day.precipitation = weather.precipitation
            day.uv_index = weather.uv_index
            day.sunrise = weather.sunrise
            day.sunset = weather.sunset

        # 更新完整行程安排
        if day_data.itinerary:
            self._update_day_itinerary(day, day_data.itinerary)

        self.db.commit()
        self.db.refresh(day)

        return self.get_trip_day_detail(trip_id, day_index, user_id)

    def get_trip_foods(self, trip_id: int, user_id: int) -> TripFoodsResponse:
        """获取行程美食攻略"""
        trip = self._get_trip_with_permission(trip_id, user_id)

        foods = self.db.query(TripFood).filter(TripFood.trip_id == trip_id).order_by(TripFood.day_index,
                                                                                     TripFood.visit_order).all()

        return TripFoodsResponse(
            trip_id=trip_id,
            total=len(foods),
            foods=[TripFoodResponse.from_orm(food) for food in foods]
        )

    def cancel_trip(self, trip_id: int, user_id: int) -> Dict[str, Any]:
        """取消行程"""
        trip = self._get_trip_with_permission(trip_id, user_id)

        trip.status = 2  # 已取消
        self.db.commit()

        return {
            "id": trip_id,
            "status": 2,
            "cancel_time": datetime.utcnow()
        }

    def _get_trip_with_permission(self, trip_id: int, user_id: int) -> Trip:
        """获取行程并检查权限"""
        trip = self.db.query(Trip).filter(Trip.id == trip_id).first()

        if not trip:
            raise NotFoundError("行程不存在")

        if trip.user_id != user_id and trip.is_public != 1:
            raise PermissionError("无权限访问此行程")

        return trip

    def _create_trip_days(self, trip: Trip):
        """创建行程天数框架"""
        current_date = trip.start_datetime.date()

        for day_index in range(1, trip.days + 1):
            day = TripDay(
                trip_id=trip.id,
                day_index=day_index,
                date=current_date,
                datetime=datetime.combine(current_date, time(9, 0)),  # 默认9点开始
                timezone=trip.start_timezone,
                title=f"DAY{day_index}",
                city=trip.destinations[0] if trip.destinations else trip.departure
            )

            self.db.add(day)
            current_date += timedelta(days=1)

        self.db.commit()

    def _build_trip_day_response(self, day: TripDay) -> TripDayResponse:
        """构建行程日程响应"""
        return TripDayResponse(
            day_index=day.day_index,
            date=day.date,
            datetime=day.datetime,
            timezone=day.timezone,
            title=day.title,
            summary=day.summary,
            city=day.city,
            theme=day.theme,
            weather=self._build_weather_info(day),
            accommodation=self._build_accommodation_info(day),
            start_point=self._build_point_info(day, "start"),
            end_point=self._build_point_info(day, "end"),
            estimated_cost=day.estimated_cost,
            is_generated=bool(day.is_generated),
            place_count=day.place_count,
            food_count=day.food_count
        )

    def _build_weather_info(self, day: TripDay) -> Optional[WeatherInfo]:
        """构建天气信息"""
        if not day.weather_condition:
            return None

        return WeatherInfo(
            condition=day.weather_condition,
            temperature=day.temperature,
            icon=day.weather_icon,
            humidity=day.humidity,
            wind=day.wind,
            precipitation=day.precipitation,
            uv_index=day.uv_index,
            sunrise=day.sunrise,
            sunset=day.sunset
        )

    def _build_accommodation_info(self, day: TripDay) -> Optional[AccommodationInfo]:
        """构建住宿信息"""
        if not day.accommodation_name:
            return None

        return AccommodationInfo(
            name=day.accommodation_name,
            address=day.accommodation_address,
            price=day.accommodation_price,
            rating=day.accommodation_rating,
            latitude=day.accommodation_latitude,
            longitude=day.accommodation_longitude,
            contact=day.accommodation_contact
        )

    def _build_point_info(self, day: TripDay, point_type: str) -> Optional[PointInfo]:
        """构建起终点信息"""
        if point_type == "start":
            if not day.start_point_name:
                return None
            return PointInfo(
                name=day.start_point_name,
                time=day.start_point_time,
                type=day.start_point_type
            )
        else:
            if not day.end_point_name:
                return None
            return PointInfo(
                name=day.end_point_name,
                time=day.end_point_time,
                type=day.end_point_type
            )

    def _build_itinerary(self, day: TripDay) -> List[ItineraryItem]:
        """构建行程安排"""
        itinerary = []

        # 获取当天的景点、美食、交通
        places = self.db.query(TripPlace).filter(TripPlace.day_id == day.id).order_by(TripPlace.visit_order).all()
        foods = self.db.query(TripFood).filter(TripFood.day_id == day.id).order_by(TripFood.visit_order).all()
        transportations = self.db.query(TripTransportation).filter(TripTransportation.day_id == day.id).order_by(
            TripTransportation.transport_order).all()

        # 合并并按时间排序
        all_items = []

        # 添加住宿（开始）
        if day.accommodation_name and day.start_point_time:
            all_items.append({
                "time": day.start_point_time,
                "type": "accommodation",
                "data": {
                    "name": day.accommodation_name,
                    "description": "酒店出发",
                    "latitude": day.accommodation_latitude,
                    "longitude": day.accommodation_longitude
                }
            })

        # 添加景点
        for place in places:
            if place.start_time:
                all_items.append({
                    "time": place.start_time,
                    "type": "place",
                    "data": place
                })

        # 添加美食
        for food in foods:
            if food.start_time:
                all_items.append({
                    "time": food.start_time,
                    "type": "food",
                    "data": food
                })

        # 添加交通
        for transport in transportations:
            if transport.start_time:
                all_items.append({
                    "time": transport.start_time,
                    "type": "transportation",
                    "data": transport
                })

        # 按时间排序
        all_items.sort(key=lambda x: x["time"])

        # 构建响应
        for item in all_items:
            itinerary_item = self._build_itinerary_item(item["type"], item["data"])
            if itinerary_item:
                itinerary.append(itinerary_item)

        return itinerary

    def _build_itinerary_item(self, item_type: str, data) -> Optional[ItineraryItem]:
        """构建行程项目"""
        if item_type == "place":
            return ItineraryItem(
                time=data.start_time.strftime("%H:%M"),
                type="place",
                name=data.name,
                description=f"门票：{data.price}元/人 | 建议游览{data.duration}分钟" if data.price and data.duration else None,
                images=data.images or ([data.image_url] if data.image_url else None),
                latitude=data.latitude,
                longitude=data.longitude,
                amap_poi_id=data.amap_poi_id,
                category=data.category,
                rating=data.rating,
                price=data.price,
                contact=data.contact,
                is_highlight=bool(data.is_highlight)
            )
        elif item_type == "food":
            return ItineraryItem(
                time=data.start_time.strftime("%H:%M"),
                type="food",
                name=data.name,
                description=f"人均：{data.price}元 | {data.recommendation}" if data.price and data.recommendation else None,
                images=data.images or ([data.image_url] if data.image_url else None),
                latitude=data.latitude,
                longitude=data.longitude,
                amap_poi_id=data.amap_poi_id,
                category=data.category,
                rating=data.rating,
                price=data.price,
                contact=data.contact,
                is_highlight=bool(data.is_highlight)
            )
        elif item_type == "transportation":
            return ItineraryItem(
                time=data.start_time.strftime("%H:%M"),
                type="transportation",
                name="交通",
                description=data.description,
                duration=data.duration,
                distance=data.distance,
                transportation_mode=data.transportation_mode,
                from_location=LocationPoint(
                    name=data.from_name,
                    latitude=data.from_latitude,
                    longitude=data.from_longitude
                ),
                to_location=LocationPoint(
                    name=data.to_name,
                    latitude=data.to_latitude,
                    longitude=data.to_longitude
                ),
                navigation=NavigationInfo(
                    amap_url=data.amap_navigation_url,
                    web_url=data.web_navigation_url
                )
            )
        elif item_type == "accommodation":
            return ItineraryItem(
                time=data.get("time", "").strftime("%H:%M") if isinstance(data.get("time"), time) else str(
                    data.get("time", "")),
                type="accommodation",
                name=data.get("name", ""),
                description=data.get("description", ""),
                latitude=data.get("latitude"),
                longitude=data.get("longitude")
            )

        return None

    def _update_day_itinerary(self, day: TripDay, itinerary: List[ItineraryItem]):
        """更新当天完整行程安排"""
        # 删除原有的景点、美食、交通安排
        self.db.query(TripPlace).filter(TripPlace.day_id == day.id).delete()
        self.db.query(TripFood).filter(TripFood.day_id == day.id).delete()
        self.db.query(TripTransportation).filter(TripTransportation.day_id == day.id).delete()

        place_order = 1
        food_order = 1
        transport_order = 1

        for item in itinerary:
            if item.type == "place":
                place = TripPlace(
                    trip_id=day.trip_id,
                    day_id=day.id,
                    day_index=day.day_index,
                    visit_order=place_order,
                    name=item.name,
                    address=item.description,
                    category=item.category,
                    images=item.images,
                    rating=item.rating,
                    price=item.price,
                    start_time=datetime.strptime(item.time, "%H:%M").time(),
                    duration=item.duration,
                    latitude=item.latitude,
                    longitude=item.longitude,
                    amap_poi_id=item.amap_poi_id,
                    contact=item.contact,
                    is_highlight=1 if item.is_highlight else 0
                )
                self.db.add(place)
                place_order += 1

            elif item.type == "food":
                food = TripFood(
                    trip_id=day.trip_id,
                    day_id=day.id,
                    day_index=day.day_index,
                    visit_order=food_order,
                    name=item.name,
                    address=item.description,
                    category=item.category,
                    images=item.images,
                    rating=item.rating,
                    price=item.price,
                    start_time=datetime.strptime(item.time, "%H:%M").time(),
                    duration=item.duration,
                    latitude=item.latitude,
                    longitude=item.longitude,
                    amap_poi_id=item.amap_poi_id,
                    contact=item.contact,
                    is_highlight=1 if item.is_highlight else 0
                )
                self.db.add(food)
                food_order += 1

            elif item.type == "transportation":
                transport = TripTransportation(
                    trip_id=day.trip_id,
                    day_id=day.id,
                    day_index=day.day_index,
                    transport_order=transport_order,
                    from_name=item.from_location.name if item.from_location else "",
                    from_latitude=item.from_location.latitude if item.from_location else None,
                    from_longitude=item.from_location.longitude if item.from_location else None,
                    to_name=item.to_location.name if item.to_location else "",
                    to_latitude=item.to_location.latitude if item.to_location else None,
                    to_longitude=item.to_location.longitude if item.to_location else None,
                    start_time=datetime.strptime(item.time, "%H:%M").time(),
                    duration=item.duration,
                    distance=item.distance,
                    transportation_mode=item.transportation_mode,
                    description=item.description,
                    amap_navigation_url=item.navigation.amap_url if item.navigation else None,
                    web_navigation_url=item.navigation.web_url if item.navigation else None
                )
                self.db.add(transport)
                transport_order += 1

        # 更新统计信息
        day.place_count = place_order - 1
        day.food_count = food_order - 1
        day.is_generated = 1
