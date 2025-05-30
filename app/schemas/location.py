from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class LocationBase(BaseModel):
    id: str = Field(..., description="地点ID")
    name: str = Field(..., description="地点名称")
    type: str = Field(..., description="地点类型")
    address: Optional[str] = None
    location: str = Field(..., description="坐标，格式：经度,纬度")
    district: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None


class LocationSearchResponse(LocationBase):
    image_url: Optional[str] = None


class LocationDetailResponse(LocationBase):
    type_code: Optional[str] = None
    tel: Optional[str] = None
    website: Optional[str] = None
    business_hours: Optional[str] = None
    rating: Optional[Decimal] = None
    price: Optional[Decimal] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    transportation: Optional[str] = None
    tips: Optional[str] = None


class LocationAroundResponse(LocationBase):
    distance: int = Field(..., description="距离中心点的距离(米)")
    tel: Optional[str] = None
    business_hours: Optional[str] = None
    rating: Optional[Decimal] = None
    price: Optional[Decimal] = None


class LocationSearchRequest(BaseModel):
    keyword: str = Field(..., description="搜索关键词")
    city: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=50)


class LocationAroundRequest(BaseModel):
    location: str = Field(..., description="中心点坐标，格式：经度,纬度")
    radius: int = Field(default=3000, ge=100, le=50000, description="搜索半径(米)")
    type: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=50)


class LocationListResponse(BaseModel):
    total: int
    locations: List[LocationSearchResponse]


class LocationAroundListResponse(BaseModel):
    total: int
    locations: List[LocationAroundResponse]
