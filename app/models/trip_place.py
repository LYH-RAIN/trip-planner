from app import db
from datetime import datetime


class TripPlace(db.Model):
    __tablename__ = 'trip_places'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.BigInteger, db.ForeignKey('trips.id'), nullable=False, comment='行程ID')
    day_id = db.Column(db.BigInteger, db.ForeignKey('trip_days.id'), nullable=False, comment='行程日程ID')
    day_index = db.Column(db.Integer, nullable=False, comment='第几天')
    visit_order = db.Column(db.Integer, nullable=False, comment='当天访问顺序')
    name = db.Column(db.String(128), nullable=False, comment='景点名称')
    address = db.Column(db.String(255), comment='详细地址')
    city = db.Column(db.String(64), comment='所在城市')
    category = db.Column(db.String(32), comment='分类')
    image_url = db.Column(db.String(255), comment='图片URL')
    rating = db.Column(db.Numeric(2, 1), comment='评分')
    price = db.Column(db.Numeric(10, 2), comment='门票价格')
    start_time = db.Column(db.Time, comment='开始时间')
    end_time = db.Column(db.Time, comment='结束时间')
    duration = db.Column(db.Integer, comment='游玩时长(分钟)')
    transportation = db.Column(db.String(32), comment='交通方式')
    transportation_details = db.Column(db.Text, comment='交通详情')
    distance = db.Column(db.Numeric(10, 2), comment='与上一地点距离(km)')
    notes = db.Column(db.Text, comment='备注')
    is_highlight = db.Column(db.SmallInteger, default=0, comment='是否为亮点：0否，1是')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'category': self.category,
            'image_url': self.image_url,
            'rating': float(self.rating) if self.rating else None,
            'price': float(self.price) if self.price else None,
            'visit_order': self.visit_order,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'duration': self.duration,
            'transportation': self.transportation,
            'transportation_details': self.transportation_details,
            'distance': float(self.distance) if self.distance else None,
            'notes': self.notes,
            'is_highlight': bool(self.is_highlight)
        }
