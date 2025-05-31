from sqlalchemy import Column, String, Text, DateTime, Integer, BigInteger, DECIMAL, JSON, Index, Time, Date, ForeignKey
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
    budget = Column(DECIMAL(10, 2), comment="预算")
    estimated_cost = Column(DECIMAL(10, 2), comment="预估费用")
    weather_info = Column(Text, comment="天气信息JSON")
    tags = Column(JSON, comment="标签列表")
    status = Column(Integer, default=0, comment="状态：0规划中，1已完成，2已取消")
    view_count = Column(Integer, default=0, comment="浏览次数")
    like_count = Column(Integer, default=0, comment="点赞次数")
    share_count = Column(Integer, default=0, comment="分享次数")
    is_public = Column(Integer, default=0, comment="是否公开：0私密，1公开")

    # 关系
    user = relationship("User", back_populates="trips")
    trip_days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")
    places = relationship("TripPlace", back_populates="trip", cascade="all, delete-orphan")
    foods = relationship("TripFood", back_populates="trip", cascade="all, delete-orphan")
    transportations = relationship("TripTransportation", back_populates="trip", cascade="all, delete-orphan")
    favorites = relationship("UserFavorite", back_populates="trip")
    reviews = relationship("TripReview", back_populates="trip")
    shares = relationship("TripShare", back_populates="trip")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
        Index('idx_public', 'is_public', 'status'),
        Index('idx_start_datetime', 'start_datetime'),
        Index('idx_created_at', 'created_at'),
    )


class TripDay(BaseModel):
    __tablename__ = "trip_days"

    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")
    day_index = Column(Integer, nullable=False, comment="第几天")
    date = Column(Date, nullable=False, comment="具体日期")
    datetime = Column(DateTime, nullable=False, comment="具体日期时间")
    timezone = Column(String(64), default="Asia/Shanghai", comment="时区")
    title = Column(String(128), comment="当天标题")
    summary = Column(Text, comment="当天概述")
    city = Column(String(64), comment="当天所在城市")
    theme = Column(String(128), comment="当天主题")

    # 天气信息
    weather_condition = Column(String(32), comment="天气状况")
    temperature = Column(String(16), comment="温度范围")
    weather_icon = Column(String(32), comment="天气图标")
    humidity = Column(String(16), comment="湿度")
    wind = Column(String(32), comment="风力")
    precipitation = Column(String(16), comment="降水概率")
    uv_index = Column(String(16), comment="紫外线指数")
    sunrise = Column(Time, comment="日出时间")
    sunset = Column(Time, comment="日落时间")

    # 住宿信息
    accommodation_name = Column(String(255), comment="住宿名称")
    accommodation_address = Column(String(255), comment="住宿地址")
    accommodation_price = Column(DECIMAL(10, 2), comment="住宿费用")
    accommodation_rating = Column(DECIMAL(2, 1), comment="住宿评分")
    accommodation_latitude = Column(DECIMAL(10, 6), comment="住宿纬度")
    accommodation_longitude = Column(DECIMAL(10, 6), comment="住宿经度")
    accommodation_contact = Column(String(64), comment="住宿联系电话")

    # 起终点信息
    start_point_name = Column(String(255), comment="起点名称")
    start_point_time = Column(Time, comment="起点时间")
    start_point_type = Column(String(32), comment="起点类型")
    end_point_name = Column(String(255), comment="终点名称")
    end_point_time = Column(Time, comment="终点时间")
    end_point_type = Column(String(32), comment="终点类型")

    estimated_cost = Column(DECIMAL(10, 2), comment="当日预估费用")
    is_generated = Column(Integer, default=0, comment="是否已生成详细行程：0否，1是")
    place_count = Column(Integer, default=0, comment="景点数量")
    food_count = Column(Integer, default=0, comment="美食数量")

    # 关系
    trip = relationship("Trip", back_populates="trip_days")
    places = relationship("TripPlace", back_populates="day", cascade="all, delete-orphan")
    foods = relationship("TripFood", back_populates="day", cascade="all, delete-orphan")
    transportations = relationship("TripTransportation", back_populates="day", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_trip_id', 'trip_id'),
        Index('uk_trip_day', 'trip_id', 'day_index', unique=True),
    )


class TripPlace(BaseModel):
    __tablename__ = "trip_places"

    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")
    day_id = Column(BigInteger, ForeignKey('trip_days.id'), nullable=False, comment="行程日程ID")
    day_index = Column(Integer, nullable=False, comment="第几天")
    visit_order = Column(Integer, nullable=False, comment="当天访问顺序")
    name = Column(String(128), nullable=False, comment="景点名称")
    address = Column(String(255), comment="详细地址")
    city = Column(String(64), comment="所在城市")
    category = Column(String(32), comment="分类")
    image_url = Column(String(255), comment="图片URL")
    images = Column(JSON, comment="图片列表")
    rating = Column(DECIMAL(2, 1), comment="评分")
    price = Column(DECIMAL(10, 2), comment="门票价格")
    start_time = Column(Time, comment="开始时间")
    end_time = Column(Time, comment="结束时间")
    duration = Column(Integer, comment="游玩时长(分钟)")
    transportation = Column(String(32), comment="交通方式")
    transportation_details = Column(Text, comment="交通详情")
    distance = Column(DECIMAL(10, 2), comment="与上一地点距离(km)")
    estimated_time = Column(Integer, comment="预计交通时间(分钟)")
    latitude = Column(DECIMAL(10, 6), comment="纬度")
    longitude = Column(DECIMAL(10, 6), comment="经度")
    amap_poi_id = Column(String(64), comment="高德POI ID")
    amap_navigation_url = Column(String(512), comment="高德导航链接")
    web_navigation_url = Column(String(512), comment="网页导航链接")
    booking_required = Column(Integer, default=0, comment="是否需要预订")
    booking_url = Column(String(255), comment="预订链接")
    contact = Column(String(64), comment="联系电话")
    notes = Column(Text, comment="备注")
    is_highlight = Column(Integer, default=0, comment="是否为行程亮点：0否，1是")

    # 关系
    trip = relationship("Trip", back_populates="places")
    day = relationship("TripDay", back_populates="places")

    __table_args__ = (
        Index('idx_trip_id', 'trip_id'),
        Index('idx_day_id', 'day_id'),
        Index('idx_trip_day', 'trip_id', 'day_index'),
        Index('idx_amap_poi_id', 'amap_poi_id'),
        Index('idx_is_highlight', 'is_highlight'),
    )


class TripFood(BaseModel):
    __tablename__ = "trip_foods"

    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")
    day_id = Column(BigInteger, ForeignKey('trip_days.id'), comment="行程日程ID")
    day_index = Column(Integer, comment="第几天")
    visit_order = Column(Integer, comment="当天访问顺序")
    name = Column(String(128), nullable=False, comment="美食名称")
    address = Column(String(255), comment="详细地址")
    city = Column(String(64), comment="所在城市")
    category = Column(String(32), comment="分类")
    image_url = Column(String(255), comment="图片URL")
    images = Column(JSON, comment="图片列表")
    rating = Column(DECIMAL(2, 1), comment="评分")
    price = Column(DECIMAL(10, 2), comment="人均价格")
    start_time = Column(Time, comment="用餐时间")
    duration = Column(Integer, comment="用餐时长(分钟)")
    latitude = Column(DECIMAL(10, 6), comment="纬度")
    longitude = Column(DECIMAL(10, 6), comment="经度")
    amap_poi_id = Column(String(64), comment="高德POI ID")
    amap_navigation_url = Column(String(512), comment="高德导航链接")
    web_navigation_url = Column(String(512), comment="网页导航链接")
    contact = Column(String(64), comment="联系电话")
    description = Column(Text, comment="描述")
    recommendation = Column(Text, comment="推荐理由")
    business_hours = Column(String(255), comment="营业时间")
    is_highlight = Column(Integer, default=0, comment="是否为行程亮点：0否，1是")

    # 关系
    trip = relationship("Trip", back_populates="foods")
    day = relationship("TripDay", back_populates="foods")

    __table_args__ = (
        Index('idx_trip_id', 'trip_id'),
        Index('idx_day_id', 'day_id'),
        Index('idx_trip_day', 'trip_id', 'day_index'),
        Index('idx_amap_poi_id', 'amap_poi_id'),
        Index('idx_is_highlight', 'is_highlight'),
    )


class TripTransportation(BaseModel):
    __tablename__ = "trip_transportations"

    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")
    day_id = Column(BigInteger, ForeignKey('trip_days.id'), nullable=False, comment="行程日程ID")
    day_index = Column(Integer, nullable=False, comment="第几天")
    transport_order = Column(Integer, nullable=False, comment="当天交通顺序")
    from_name = Column(String(255), nullable=False, comment="起点名称")
    from_latitude = Column(DECIMAL(10, 6), comment="起点纬度")
    from_longitude = Column(DECIMAL(10, 6), comment="起点经度")
    to_name = Column(String(255), nullable=False, comment="终点名称")
    to_latitude = Column(DECIMAL(10, 6), comment="终点纬度")
    to_longitude = Column(DECIMAL(10, 6), comment="终点经度")
    start_time = Column(Time, comment="出发时间")
    duration = Column(Integer, comment="交通时长(分钟)")
    distance = Column(DECIMAL(10, 2), comment="距离(km)")
    transportation_mode = Column(String(32), comment="交通方式")
    description = Column(Text, comment="交通描述")
    amap_navigation_url = Column(String(512), comment="高德导航链接")
    web_navigation_url = Column(String(512), comment="网页导航链接")

    # 关系
    trip = relationship("Trip", back_populates="transportations")
    day = relationship("TripDay", back_populates="transportations")

    __table_args__ = (
        Index('idx_trip_id', 'trip_id'),
        Index('idx_day_id', 'day_id'),
        Index('idx_trip_day', 'trip_id', 'day_index'),
    )


class TripShare(BaseModel):
    __tablename__ = "trip_shares"

    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="分享用户ID")
    share_type = Column(Integer, nullable=False, comment="分享类型：1微信，2朋友圈，3链接，4二维码")
    share_url = Column(String(255), comment="分享链接")
    share_code = Column(String(32), comment="分享码")
    view_count = Column(Integer, default=0, comment="查看次数")
    expires_at = Column(DateTime, comment="过期时间")

    # 关系
    trip = relationship("Trip", back_populates="shares")

    __table_args__ = (
        Index('idx_trip_id', 'trip_id'),
        Index('idx_user_id', 'user_id'),
        Index('idx_share_code', 'share_code'),
    )


class TripReview(BaseModel):
    __tablename__ = "trip_reviews"

    trip_id = Column(BigInteger, ForeignKey('trips.id'), nullable=False, comment="行程ID")
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="评价用户ID")
    rating = Column(Integer, nullable=False, comment="评分1-5")
    content = Column(Text, comment="评价内容")
    images = Column(JSON, comment="评价图片列表")

    # 关系
    trip = relationship("Trip", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    __table_args__ = (
        Index('idx_trip_id', 'trip_id'),
        Index('idx_user_id', 'user_id'),
        Index('idx_rating', 'rating'),
    )


class AIModelCall(BaseModel):
    __tablename__ = "ai_model_calls"

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="用户ID")
    trip_id = Column(BigInteger, ForeignKey('trips.id'), comment="关联行程ID")
    prompt = Column(Text, nullable=False, comment="输入提示词")
    response = Column(Text, comment="AI返回结果")
    model_name = Column(String(64), comment="模型名称")
    call_type = Column(String(32), comment="调用类型")
    status = Column(Integer, default=0, comment="状态：0处理中，1成功，2失败")
    error_message = Column(String(255), comment="错误信息")
    tokens_used = Column(Integer, comment="使用的token数量")
    cost = Column(DECIMAL(10, 4), comment="调用费用")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_trip_id', 'trip_id'),
        Index('idx_call_type', 'call_type'),
        Index('idx_created_at', 'created_at'),
    )
