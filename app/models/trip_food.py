from app import db
from datetime import datetime


class TripFood(db.Model):
    __tablename__ = 'trip_foods'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.BigInteger, db.ForeignKey('trips.id'), nullable=False, comment='行程ID')
    day_id = db.Column(db.BigInteger, db.ForeignKey('trip_days.id'), comment='行程日程ID')
    day_index = db.Column(db.Integer, comment='第几天')
    name = db.Column(db.String(128), nullable=False, comment='美食名称')
    address = db.Column(db.String(255), comment='详细地址')
    city = db.Column(db.String(64), comment='所在城市')
    category = db.Column(db.String(32), comment='分类')
    image_url = db.Column(db.String(255), comment='图片URL')
    rating = db.Column(db.Numeric(2, 1), comment='评分')
    price = db.Column(db.Numeric(10, 2), comment='人均价格')
    description = db.Column(db.Text, comment='描述')
    recommendation = db.Column(db.Text, comment='推荐理由')
    business_hours = db.Column(db.String(255), comment='营业时间')
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
            'description': self.description,
            'recommendation': self.recommendation,
            'business_hours': self.business_hours,
            'is_highlight': bool(self.is_highlight),
            'day_index': self.day_index
        }
