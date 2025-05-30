from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    open_id: str = Field(..., description="微信OpenID")
    union_id: Optional[str] = None


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    open_id: str
    union_id: Optional[str] = None
    status: int
    vip_level: int
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    code: str = Field(..., description="微信授权code")


class UserLoginResponse(BaseModel):
    token: str
    user: UserResponse
    is_new_user: bool = False
