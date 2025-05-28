import requests
from datetime import datetime
from flask import current_app
from app import db
from app.models.user import User
from app.utils.jwt_util import generate_token


class AuthService:
    @staticmethod
    def wechat_login(code):
        """
        微信登录
        """
        # 获取微信openid
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": current_app.config["WECHAT_APP_ID"],
            "secret": current_app.config["WECHAT_APP_SECRET"],
            "js_code": code,
            "grant_type": "authorization_code"
        }

        response = requests.get(url, params=params)
        result = response.json()

        if "errcode" in result and result["errcode"] != 0:
            return None, result["errmsg"]

        open_id = result.get("openid")
        union_id = result.get("unionid")

        if not open_id:
            return None, "获取微信openid失败"

        # 查找或创建用户
        user = User.query.filter_by(open_id=open_id).first()
        is_new_user = False

        if not user:
            user = User(open_id=open_id, union_id=union_id)
            db.session.add(user)
            is_new_user = True

        # 更新登录时间
        user.last_login_at = datetime.now()
        db.session.commit()

        # 生成token
        token = generate_token(user.id)

        return {
            "token": token,
            "user": {
                "id": user.id,
                "nickname": user.nickname,
                "avatarUrl": user.avatar_url,
                "isNewUser": is_new_user
            }
        }, None

    @staticmethod
    def update_user_info(user_id, user_info):
        """
        更新用户信息
        """
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"

        # 更新用户信息
        user.nickname = user_info.get("nickName", user.nickname)
        user.avatar_url = user_info.get("avatarUrl", user.avatar_url)
        user.gender = user_info.get("gender", user.gender)
        user.country = user_info.get("country", user.country)
        user.province = user_info.get("province", user.province)
        user.city = user_info.get("city", user.city)

        db.session.commit()

        return user.to_dict(), None
