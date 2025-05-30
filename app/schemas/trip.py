from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from decimal import Decimal


class TripBase(BaseModel):
    title: str = Field(..., max_length=128, description="行程标题")
    description: Optional[str] = None
    departure: str = Field(..., max_length=64, description="出发地")
    destinations: List[str] = Field(..., description="目的地城市列表")
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
    condition: Optional[str] = None
    temperature: Optional[str] = None
    icon: Optional[str] = None
    humidity: Optional[str] = None
    wind: Optional[str] = None
    precipitation: Optional[str] = None
    uv_index: Optional[str] = None
    sunrise: Optional[time] = None
    sunset: Optional[time] = None


class AccommodationInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    price: Optional[Decimal] = None
    rating: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact: Optional[str] = None


class PointInfo(BaseModel):
    name: str
    time: Optional[time] = None
    type: str


class TripDayResponse(BaseModel):
    day_index: int
    date: date
    datetime: datetime
    timezone: str
    title: Optional[str] = None
    summary: Optional[str] = None
    city: Optional[str] = None
    theme: Optional[str] = None
    weather: Optional[WeatherInfo] = None
    accommodation: Optional[AccommodationInfo] = None
    start_point: Optional[PointInfo] = None
    end_point: Optional[PointInfo] = None
    estimated_cost: Optional[Decimal] = None
    is_generated: bool
    place_count: int
    food_count: int

    class Config:
        from_attributes = True


class TripResponse(TripBase):
    id: int
    user_id: int
    days: int
    overview: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    status: int
    view_count: int
    like_count: int
    share_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TripListResponse(BaseModel):
    total: int
    trips: List[TripResponse]


class NavigationInfo(BaseModel):
    amap_url: Optional[str] = None
    web_url: Optional[str] = None


class LocationPoint(BaseModel):
    name: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class ItineraryItem(BaseModel):
    time: str
    type: str  # accommodation, transportation, place, food
    name: str
    description: Optional[str] = None
    images: Optional[List[str]] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    duration: Optional[int] = None
    distance: Optional[Decimal] = None
    transportation_mode: Optional[str] = None
    from_location: Optional[LocationPoint] = None
    to_location: Optional[LocationPoint] = None
    navigation: Optional[NavigationInfo] = None
    amap_poi_id: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Decimal] = None
    price: Optional[Decimal] = None
    contact: Optional[str] = None
    is_highlight: Optional[bool] = None


class TripDayDetailResponse(BaseModel):
    trip_id: int
    date: date
    title: Optional[str] = None
    city: Optional[str] = None
    weather: Optional[WeatherInfo] = None
    total_places: int
    itinerary: List[ItineraryItem]


class TripDayUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    city: Optional[str] = None
    theme: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    accommodation: Optional[AccommodationInfo] = None
    start_point: Optional[PointInfo] = None
    end_point: Optional[PointInfo] = None
    weather: Optional[WeatherInfo] = None
    itinerary: Optional[List[ItineraryItem]] = None


class TripOverviewResponse(BaseModel):
    trip_info: TripResponse
    days_list: List[TripDayResponse]
    total_highlights: List[Dict[str, Any]]


class TripFoodResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[Decimal] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    recommendation: Optional[str] = None
    business_hours: Optional[str] = None
    is_highlight: bool
    day_index: Optional[int] = None

    class Config:
        from_attributes = True


class TripFoodsResponse(BaseModel):
    trip_id: int
    total: int
    foods: List[TripFoodResponse]
