from sqlalchemy import Column, String, Text, DateTime, Integer, BigInteger, Decimal, JSON, Index, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Trip(BaseModel):
    __tablename__ = "trips"

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="创建用户ID")
    title = Column(String(128), nullable=False, comment="行程标题")
    description = Column(Text, comment="行程描述")
    cover_image = Column(String(255), comment="封面图片")
    start_datetime = Column(DateTime, nullable=False, comment="开始时间")
    end_datetime = Column(DateTime, nullable=False, comment="结束时间")
    start_timezone = Column(String(64), default="Asia/Shanghai", comment="开始时区")
    end_timezone = Column(String(64), default="Asia/Shanghai", comment="结束时区")
    days = Column(Integer, nullable=False, comment="行程天数")
    departure = Column(String(64), nullable=False, comment="出发地")
    destinations = Column(JSON, comment="目的地城市列表")
    travel_mode = Column(Integer, default=1, comment="交通方式：1自驾，2公共交通")
    people_count = Column(Integer, default=1, comment="出行人数")
    preferences = Column(JSON, comment="偏好列表")
    overview = Column(Text, comment="行程总览")
    budget = Column(Decimal(10, 2), comment="预算")
    estimated_cost = Column(Decimal(10, 2), comment="预估费用")
    weather_info = Column(Text, comment="天气信息JSON")
    tags = Column(JSON, comment="标签列表")
    status = Column(Integer, default=0, comment="状态：0规划中，1已完成，2已取消")
    view_count = Column(Integer, default=0, comment="浏览次数")
    like_count = Column(Integer, default=0, comment="点赞次数")
    share_count = Column(Integer, default=0, comment="分享次数")
    is_public = Column(Integer, default=0, comment="是否公开：0私密，1公开")

    # 关系
    user = relationship("User", back_populates="trips")
    days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")
    places = relationship("TripPlace", back_populates="trip", cascade="all, delete-orphan")
    foods = relationship("TripFood", back_populates="trip", cascade="all, delete-orphan")
    transportations = relationship("TripTransportation", back_populates="trip", cascade="all, delete-orphan")
    favorites = relationship("UserFavorite", back_populates="trip")
    reviews = relationship("TripReview", back_populates="trip")
    shares = relationship("TripShare", back_populates="trip")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
        Index('idx_public', 'is_public',
