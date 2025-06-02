from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserLogin, UserLoginResponse
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError

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
