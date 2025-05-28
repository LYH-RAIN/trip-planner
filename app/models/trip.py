from app import db
from datetime import datetime
import json


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    title = db.Column(db.String(128), nullable=False, comment='行程标题')
    description = db.Column(db.Text, comment='行程描述')
    cover_image = db.Column(db.String(255), comment='封面图片')
    start_date = db.Column(db.Date, nullable=False, comment='开始日期')
    end_date = db.Column(db.Date, nullable=False, comment='结束日期')
    days = db.Column(db.Integer, nullable=False, comment='行程天数')
    departure = db.Column(db.String(64), nullable=False, comment='出发地')
    destinations = db.Column(db.Text, comment='目的地JSON，包含名称和停留天数')
    travel_mode = db.Column(db.SmallInteger, default=1, comment='交通方式：1自驾，2公共交通')
    people_count = db.Column(db.Integer, default=1, comment='出行人数')
    preferences = db.Column(db.Text, comment='偏好JSON')
    overview = db.Column(db.Text, comment='行程总览')
    status = db.Column(db.SmallInteger, default=0, comment='状态：0规划中，1已完成，2已取消')
    view_count = db.Column(db.Integer, default=0, comment='浏览次数')
    like_count = db.Column(db.Integer, default=0, comment='点赞次数')
    share_count = db.Column(db.Integer, default=0, comment='分享次数')
    is_public = db.Column(db.SmallInteger, default=0, comment='是否公开：0私密，1公开')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    days_detail = db.relationship('TripDay', backref='trip', lazy='dynamic', cascade='all, delete-orphan')
    places = db.relationship('TripPlace', backref='trip', lazy='dynamic', cascade='all, delete-orphan')
    foods = db.relationship('TripFood', backref='trip', lazy='dynamic', cascade='all, delete-orphan')

    def get_destinations(self):
        if self.destinations:
            return json.loads(self.destinations)
        return []

    def set_destinations(self, destinations):
        self.destinations = json.dumps(destinations)

    def get_preferences(self):
        if self.preferences:
            return json.loads(self.preferences)
        return []

    def set_preferences(self, preferences):
        self.preferences = json.dumps(preferences)

    def to_dict(self, simple=True):
        result = {
            'id': self.id,
            'title': self.title,
            'cover_image': self.cover_image,
            'startDate': self.start_date.strftime('%Y-%m-%d'),
            'endDate': self.end_date.strftime('%Y-%m-%d'),
            'days': self.days,
            'destinations': self.get_destinations(),
            'status': self.status,
            'createdAt': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        if not simple:
            result.update({
                'description': self.description,
                'departure': self.departure,
                'travelMode': self.travel_mode,
                'peopleCount': self.people_count,
                'preferences': self.get_preferences(),
                'overview': self.overview,
                'is_public': self.is_public,
                'view_count': self.view_count,
                'like_count': self.like_count,
                'share_count': self.share_count
            })

        return result
