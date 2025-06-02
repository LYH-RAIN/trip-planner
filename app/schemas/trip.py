from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from decimal import Decimal


class TripBase(BaseModel):
    title: str = Field(..., max_length=128, description="行程标题")
    description: Optional[str] = None
    departure: str = Field(..., max_length=64, description="出发地POI ID")
    destinations: List[str] = Field(..., description="目的地POI ID列表")
    start_datetime: datetime = Field(..., description="开始时间")
    end_datetime: datetime = Field(..., description="结束时间")
    start_timezone: str = Field(default="Asia/Shanghai", description="开始时区")
    end_timezone: str = Field(default="Asia/Shanghai", description="结束时区")
    people_count: int = Field(default=1, ge=1, description="出行人数")
    travel_mode: int = Field(default=1, ge=1, le=2, description="交通方式：1自驾，2公共交通")
    preferences: Optional[List[str]] = None
    budget: Optional[Decimal] = None
    tags: Optional[List[str]] = None
    is_public: int = Field(default=0, ge=0, le=1, description="是否公开：0私密，1公开")


class TripCreate(TripBase):
    pass


class TripCollaboratorInfo(BaseModel):
    user_id: int
    avatar_url: Optional[str] = None
    role: str


class TripListItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    days: int
    travel_mode: int
    people_count: int
    status: int
    is_public: int
    weather_info: Optional[Dict[str, Any]] = Field(None, description="天气信息JSON对象")
    estimated_cost: Optional[Decimal] = None
    budget: Optional[Decimal] = None
    tags: Optional[List[str]] = None
    collaborators: Optional[List[TripCollaboratorInfo]] = None
    collaborator_count: Optional[int] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    days_overview: Optional[List["TripDayOverviewItem"]] = None

    class Config:
        from_attributes = True


class TripListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    trips: List[TripListItemResponse]


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    departure: Optional[str] = None
    destinations: Optional[List[str]] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    start_timezone: Optional[str] = None
    end_timezone: Optional[str] = None
    people_count: Optional[int] = None
    travel_mode: Optional[int] = None
    preferences: Optional[List[str]] = None
    budget: Optional[Decimal] = None
    tags: Optional[List[str]] = None
    is_public: Optional[int] = None
    overview: Optional[str] = None
    estimated_cost: Optional[Decimal] = None


class WeatherInfo(BaseModel):
    condition: Optional[str] = Field(None, description="天气状况")
    temperature: Optional[str] = Field(None, description="温度范围")
    icon: Optional[str] = Field(None, description="天气图标")
    humidity: Optional[str] = Field(None, description="湿度")
    wind: Optional[str] = Field(None, description="风力")
    precipitation: Optional[str] = Field(None, description="降水概率")
    uv_index: Optional[str] = Field(None, description="紫外线指数")
    sunrise: Optional[time] = Field(None, description="日出时间")
    sunset: Optional[time] = Field(None, description="日落时间")


class AccommodationInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    price: Optional[Decimal] = None
    rating: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact: Optional[str] = None
    accommodation_poi_id: Optional[str] = Field(None, description="住宿POI ID")


class PointInfo(BaseModel):
    name: str
    time: Optional[time] = None
    type: Optional[str] = None
    poi_id: Optional[str] = Field(None, description="地点POI ID")


class TripDayOverviewItem(BaseModel):
    day_index: int
    date: date
    title: Optional[str] = None
    city: Optional[str] = None
    is_generated: bool
    estimated_cost: Optional[Decimal] = None
    start_location: Optional[PointInfo] = None
    end_location: Optional[PointInfo] = None
    weather: Optional[WeatherInfo] = None
    attractions: Optional[List[Dict[str, Any]]] = Field(None, description="景点列表，如 [{'name': '南华寺', 'image_url': '...'}]")

    class Config:
        from_attributes = True


class TripFullResponse(TripBase):
    id: int
    user_id: int
    days: int
    overview: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    status: int
    generation_status: Optional[int] = None
    view_count: int
    like_count: int
    share_count: int
    cover_image: Optional[str] = None
    collaborators: Optional[List[TripCollaboratorInfo]] = None
    collaborator_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TripOverviewResponse(BaseModel):
    trip_info: TripFullResponse
    days_overview: List["TripDayOverviewItem"]


class NavigationInfo(BaseModel):
    amap_url: Optional[str] = None
    web_url: Optional[str] = None


class LocationPoint(BaseModel):
    name: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class ItineraryItem(BaseModel):
    time: Optional[str] = None
    type: str
    name: str
    description: Optional[str] = None
    images: Optional[List[str]] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    duration: Optional[int] = Field(None, description="时长(分钟)")
    distance: Optional[Decimal] = Field(None, description="距离(km)")
    mode: Optional[str] = Field(None, alias="transportation_mode", description="交通方式, e.g., driving, walking")
    from_location: Optional[LocationPoint] = Field(None, alias="from")
    to_location: Optional[LocationPoint] = Field(None, alias="to")
    navigation: Optional[NavigationInfo] = None
    amap_poi_id: Optional[str] = None
    price: Optional[Decimal] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class TripDayDetailResponse(BaseModel):
    trip_id: int
    day_index: int
    date: date
    title: Optional[str] = None
    city: Optional[str] = None
    weather: Optional[WeatherInfo] = None
    total_places: Optional[int] = None
    itinerary: List[ItineraryItem]

    class Config:
        from_attributes = True


class TripDayUpdateItineraryItem(BaseModel):
    time: Optional[str] = None
    type: str
    description: Optional[str] = None
    duration: Optional[int] = Field(None, description="时长(分钟)")
    amap_poi_id: str
    price: Optional[Decimal] = None
    next_transport: Optional[str] = Field(None, description="前往下一地点的交通方式")


class TripDayUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = Field(None, description="当日概述")
    city: Optional[str] = None
    theme: Optional[str] = Field(None, description="当日主题")
    estimated_cost: Optional[Decimal] = None
    itinerary: Optional[List[TripDayUpdateItineraryItem]] = Field(None, description="行程安排，只含实际地点")


class TripFoodResponseItem(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[Decimal] = None
    price: Optional[Decimal] = Field(None, description="人均价格")
    description: Optional[str] = None
    recommendation: Optional[str] = None
    business_hours: Optional[str] = None
    is_highlight: bool
    day_index: Optional[int] = None
    amap_poi_id: Optional[str] = None

    class Config:
        from_attributes = True


class TripFoodsResponse(BaseModel):
    trip_id: int
    total: int
    foods: List[TripFoodResponseItem]


class TripCancelRequest(BaseModel):
    confirm: bool = Field(..., description="确认为true以取消行程")


class TripCancelResponseData(BaseModel):
    id: int
    status: int
    cancel_time: datetime


class TripCancelResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: TripCancelResponseData

TripListItemResponse.update_forward_refs()
TripOverviewResponse.update_forward_refs()
