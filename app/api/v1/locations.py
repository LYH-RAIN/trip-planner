from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.schemas.location import (
    LocationListResponse, LocationDetailResponse, LocationAroundListResponse
)
from app.services.location_service import LocationService
from app.core.exceptions import ValidationError

router = APIRouter()

@router.get("/search", response_model=LocationListResponse)
async def search_locations(
    keyword: str = Query(..., description="搜索关键词"),
    city: Optional[str] = Query(None, description="城市名称"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=50, description="每页数量")
):
    """搜索地点"""
    try:
        location_service = LocationService()
        result = await location_service.search_locations(keyword, city, page, page_size)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@router.get("/detail", response_model=LocationDetailResponse)
async def get_location_detail(
    id: str = Query(..., description="地点ID")
):
    """获取地点详情"""
    try:
        location_service = LocationService()
        result = await location_service.get_location_detail(id)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详情失败: {str(e)}")

@router.get("/around", response_model=LocationAroundListResponse)
async def search_around(
    location: str = Query(..., description="中心点坐标，格式：经度,纬度"),
    radius: int = Query(3000, ge=100, le=50000, description="搜索半径(米)"),
    type: Optional[str] = Query(None, description="搜索类型"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=50, description="每页数量")
):
    """周边搜索"""
    try:
        location_service = LocationService()
        result = await location_service.search_around(location, radius, type, page, page_size)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"周边搜索失败: {str(e)}")
