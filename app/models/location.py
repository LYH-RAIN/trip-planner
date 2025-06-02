from sqlalchemy import Column, String, Text, DECIMAL, Integer, BigInteger, DateTime, Index, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON as MysqlJSON # Assuming MySQL
from .base import BaseModel


class Location(BaseModel):
    """地点信息表（本地缓存）"""
    __tablename__ = "locations"

    amap_poi_id = Column(String(64), unique=True, nullable=False, comment="高德POI ID")
    name = Column(String(128), nullable=False, comment="地点名称")
    type = Column(String(32), comment="地点类型")
    type_code = Column(String(16), comment="类型代码")
    address = Column(String(255), comment="详细地址") # Changed DECIMAL to String, address is not usually a number
    latitude = Column(DECIMAL(10, 6), comment="纬度")
    longitude = Column(DECIMAL(10, 6), comment="经度")
    district = Column(String(64), comment="区县")
    city = Column(String(64), comment="城市")
    province = Column(String(64), comment="省份")
    tel = Column(String(64), comment="联系电话")
    website = Column(String(255), comment="官网")
    business_hours = Column(String(255), comment="营业时间")
    rating = Column(DECIMAL(2, 1), comment="评分")
    price = Column(DECIMAL(10, 2), comment="价格")
    images = Column(MysqlJSON, comment="图片列表") # Changed to MysqlJSON
    tags = Column(MysqlJSON, comment="标签列表") # Changed to MysqlJSON
    description = Column(Text, comment="描述")
    introduction = Column(Text, comment="详细介绍")
    transportation = Column(Text, comment="交通信息")
    tips = Column(Text, comment="游玩提示")

    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    search_count = Column(Integer, default=0, comment="搜索次数")

    # 数据来源和更新
    data_source = Column(String(32), default="amap", comment="数据来源")
    last_sync_at = Column(DateTime, comment="最后同步时间")

    __table_args__ = (
        Index('idx_amap_poi_id', 'amap_poi_id'),
        Index('idx_name', 'name'),
        Index('idx_city_type', 'city', 'type'),
        Index('idx_location', 'latitude', 'longitude'),
        Index('idx_rating', 'rating'),
    )


class LocationCategory(BaseModel):
    """地点分类表"""
    __tablename__ = "location_categories"

    code = Column(String(16), unique=True, nullable=False, comment="分类代码")
    name = Column(String(64), nullable=False, comment="分类名称")
    parent_code = Column(String(16), comment="父分类代码")
    level = Column(Integer, default=1, comment="分类层级")
    sort_order = Column(Integer, default=0, comment="排序")
    icon = Column(String(64), comment="图标")
    description = Column(String(255), comment="描述")
    is_active = Column(Integer, default=1, comment="是否启用")

    __table_args__ = (
        Index('idx_code', 'code'),
        Index('idx_parent_code', 'parent_code'),
        Index('idx_level', 'level'),
    )


class LocationSearchLog(BaseModel):
    """地点搜索日志表"""
    __tablename__ = "location_search_logs"

    user_id = Column(BigInteger, ForeignKey('users.id'), comment="用户ID") # Added ForeignKey
    keyword = Column(String(128), nullable=False, comment="搜索关键词")
    city = Column(String(64), comment="搜索城市")
    search_type = Column(String(32), comment="搜索类型")
    result_count = Column(Integer, default=0, comment="结果数量")
    ip_address = Column(String(45), comment="IP地址")
    user_agent = Column(String(255), comment="用户代理")
    
    # user = relationship("User") # Optional: if you need to access user from log

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_keyword', 'keyword'),
        Index('idx_created_at', 'created_at'),
    )


class UserLocationHistory(BaseModel):
    """用户地点浏览历史表"""
    __tablename__ = "user_location_history"

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="用户ID") # Added ForeignKey
    location_id = Column(BigInteger, ForeignKey('locations.id'), comment="地点ID") # Added ForeignKey
    amap_poi_id = Column(String(64), comment="高德POI ID")
    location_name = Column(String(128), comment="地点名称")
    view_type = Column(String(32), comment="浏览类型：search, detail, around")
    view_duration = Column(Integer, comment="浏览时长(秒)")

    # 关系
    # user = relationship("User") # Optional
    location = relationship("Location", foreign_keys=[location_id])

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_location_id', 'location_id'),
        Index('idx_amap_poi_id', 'amap_poi_id'),
        Index('idx_created_at', 'created_at'),
    )


class LocationRecommendation(BaseModel):
    """地点推荐表"""
    __tablename__ = "location_recommendations"

    location_id = Column(BigInteger, ForeignKey('locations.id'), nullable=False, comment="地点ID") # Added ForeignKey
    amap_poi_id = Column(String(64), comment="高德POI ID")
    recommendation_type = Column(String(32), comment="推荐类型：hot, nearby, similar")
    target_city = Column(String(64), comment="目标城市")
    target_category = Column(String(32), comment="目标分类")
    score = Column(DECIMAL(3, 2), comment="推荐分数")
    reason = Column(String(255), comment="推荐理由")
    is_active = Column(Integer, default=1, comment="是否启用")

    # 关系
    location = relationship("Location", foreign_keys=[location_id])

    __table_args__ = (
        Index('idx_location_id', 'location_id'),
        Index('idx_amap_poi_id', 'amap_poi_id'),
        Index('idx_type_city', 'recommendation_type', 'target_city'),
        Index('idx_score', 'score'),
    )
