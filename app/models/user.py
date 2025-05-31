from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Text, Index, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    open_id = Column(String(64), unique=True, nullable=False, comment="微信OpenID")
    union_id = Column(String(64), comment="微信UnionID")
    nickname = Column(String(64), comment="用户昵称")
    avatar_url = Column(String(255), comment="头像URL")
    gender = Column(Integer, comment="性别：0未知，1男，2女")
    country = Column(String(64), comment="国家")
    province = Column(String(64), comment="省份")
    city = Column(String(64), comment="城市")
    phone = Column(String(20), comment="手机号")
    status = Column(Integer, default=1, comment="用户状态：0禁用，1正常")
    vip_level = Column(Integer, default=0, comment="VIP等级：0普通，1VIP，2SVIP")
    last_login_at = Column(DateTime, comment="最后登录时间")

    # 关系
    trips = relationship("Trip", back_populates="user")
    favorites = relationship("UserFavorite", back_populates="user")
    reviews = relationship("TripReview", back_populates="user")

    __table_args__ = (
        Index('idx_open_id', 'open_id'),
        Index('idx_union_id', 'union_id'),
        Index('idx_status', 'status'),
    )


class UserFavorite(BaseModel):
    __tablename__ = "user_favorites"

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="用户ID")
    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")

    # 关系
    user = relationship("User", back_populates="favorites")
    trip = relationship("Trip", back_populates="favorites")

    __table_args__ = (
        Index('uk_user_trip', 'user_id', 'trip_id', unique=True),
        Index('idx_user_id', 'user_id'),
        Index('idx_trip_id', 'trip_id'),
    )
