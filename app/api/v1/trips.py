from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.trip import (
    TripCreate, TripResponse, TripListResponse,
    TripOverviewResponse, TripDayDetailResponse, TripDayUpdate,
    TripFoodsResponse
)
from app.services.trip_service import TripService
from app.core.exceptions import NotFoundError, PermissionError, ValidationError

router = APIRouter()

@router.post("", response_model=TripResponse)
def create_trip(
    trip_data: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建行程"""
    try:
        trip_service = TripService(db)
        result = trip_service.create_trip(trip_data, current_user.id)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建行程失败: {str(e)}")

@router.get("", response_model=TripListResponse)
def get_trips(
    status: Optional[str] = Query(None, description="行程状态"),
    id: Optional[int] = Query(None, description="行程ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=50, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取行程列表"""
    try:
        trip_service = TripService(db)
        result = trip_service.get_trips(current_user.id, status, id, page, page_size)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行程列表失败: {str(e)}")

@router.get("/{trip_id}/overview", response_model=TripOverviewResponse)
def get_trip_overview(
    trip_id: int = Path(..., description="行程ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取行程总览"""
    try:
        trip_service = TripService(db)
        result = trip_service.get_trip_overview(trip_id, current_user.id)
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行程总览失败: {str(e)}")

@router.get("/{trip_id}/days/{day_index}", response_model=TripDayDetailResponse)
def get_trip_day_detail(
    trip_id: int = Path(..., description="行程ID"),
    day_index: int = Path(..., description="第几天"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取行程日程详情"""
    try:
        trip_service = TripService(db)
        result = trip_service.get_trip_day_detail(trip_id, day_index, current_user.id)
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行程详情失败: {str(e)}")

@router.put("/{trip_id}/days/{day_index}", response_model=TripDayDetailResponse)
def update_trip_day(
    day_data: TripDayUpdate,
    trip_id: int = Path(..., description="行程ID"),
    day_index: int = Path(..., description="第几天"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改行程日程详情"""
    try:
        trip_service = TripService(db)
        result = trip_service.update_trip_day(trip_id, day_index, day_data, current_user.id)
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改行程失败: {str(e)}")

@router.get("/{trip_id}/foods", response_model=TripFoodsResponse)
def get_trip_foods(
    trip_id: int = Path(..., description="行程ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取行程美食攻略"""
    try:
        trip_service = TripService(db)
        result = trip_service.get_trip_foods(trip_id, current_user.id)
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取美食攻略失败: {str(e)}")

@router.post("/{trip_id}/cancel")
def cancel_trip(
    trip_id: int = Path(..., description="行程ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消行程"""
    try:
        trip_service = TripService(db)
        result = trip_service.cancel_trip(trip_id, current_user.id)
        return {"code": 0, "message": "success", "data": result}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消行程失败: {str(e)}")
