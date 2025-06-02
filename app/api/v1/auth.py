from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserLogin, UserLoginResponse
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/wechat/login", response_model=UserLoginResponse)
async def wechat_login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):

    try:
        auth_service = AuthService(db)
        result = await auth_service.wechat_login(login_data.code)
        return result
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"��¼ʧ��: {str(e)}")

@router.post("/test-login", response_model=UserLoginResponse)
async def test_login(
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    # if not settings.DEBUG:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="asdasdasdasdad")
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(user_id)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=None
    )
    return UserLoginResponse(
        token=access_token,
        user=UserResponse.from_orm(user),
        is_new_user=False
    )
