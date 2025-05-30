import httpx
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.security import create_access_token
from app.core.exceptions import AuthenticationError, ValidationError
from app.models.user import User
from app.schemas.user import UserCreate, UserLoginResponse, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    async def wechat_login(self, code: str) -> UserLoginResponse:
        """微信登录"""
        try:
            # 获取微信用户信息
            wechat_user = await self._get_wechat_user_info(code)

            # 查找或创建用户
            user = self.db.query(User).filter(User.open_id == wechat_user["openid"]).first()
            is_new_user = False

            if not user:
                # 创建新用户
                user_data = UserCreate(
                    open_id=wechat_user["openid"],
                    union_id=wechat_user.get("unionid"),
                    nickname=wechat_user.get("nickname"),
                    avatar_url=wechat_user.get("headimgurl"),
                    gender=wechat_user.get("sex", 0),
                    country=wechat_user.get("country"),
                    province=wechat_user.get("province"),
                    city=wechat_user.get("city")
                )
                user = User(**user_data.dict())
                self.db.add(user)
                is_new_user = True
            else:
                # 更新用户信息
                user.nickname = wechat_user.get("nickname", user.nickname)
                user.avatar_url = wechat_user.get("headimgurl", user.avatar_url)
                user.gender = wechat_user.get("sex", user.gender)
                user.country = wechat_user.get("country", user.country)
                user.province = wechat_user.get("province", user.province)
                user.city = wechat_user.get("city", user.city)

            # 更新最后登录时间
            user.last_login_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)

            # 生成JWT token
            access_token = create_access_token(
                data={"sub": str(user.id)},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )

            return UserLoginResponse(
                token=access_token,
                user=UserResponse.from_orm(user),
                is_new_user=is_new_user
            )

        except Exception as e:
            raise AuthenticationError(f"微信登录失败: {str(e)}")

    async def _get_wechat_user_info(self, code: str) -> dict:
        """获取微信用户信息"""
        # 第一步：通过code获取access_token
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        token_params = {
            "appid": settings.WECHAT_APP_ID,
            "secret": settings.WECHAT_APP_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.get(token_url, params=token_params)
            token_data = token_response.json()

            if "errcode" in token_data:
                raise AuthenticationError(f"获取微信access_token失败: {token_data.get('errmsg')}")

            access_token = token_data["access_token"]
            openid = token_data["openid"]

            # 第二步：通过access_token获取用户信息
            user_url = "https://api.weixin.qq.com/sns/userinfo"
            user_params = {
                "access_token": access_token,
                "openid": openid,
                "lang": "zh_CN"
            }

            user_response = await client.get(user_url, params=user_params)
            user_data = user_response.json()

            if "errcode" in user_data:
                raise AuthenticationError(f"获取微信用户信息失败: {user_data.get('errmsg')}")

            return user_data

    def get_user_by_id(self, user_id: int) -> User:
        """根据ID获取用户"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AuthenticationError("用户不存在")
        return user
