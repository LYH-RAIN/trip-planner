from app import db
from datetime import datetime


class TripDay(db.Model):
    __tablename__ = 'trip_days'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.BigInteger, db.ForeignKey('trips.id'), nullable=False, comment='行程ID')
    day_index = db.Column(db.Integer, nullable=False, comment='第几天')
    date = db.Column(db.Date, nullable=False, comment='具体日期')
    title = db.Column(db.String(128), comment='当天标题')
    summary = db.Column(db.Text, comment='当天概述')
    city = db.Column(db.String(64), comment='当天所在城市')
    weather = db.Column(db.String(32), comment='天气')
    temperature = db.Column(db.String(16), comment='温度范围')
    accommodation = db.Column(db.String(255), comment='住宿地点')
    accommodation_price = db.Column(db.Numeric(10, 2), comment='住宿费用')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    places = db.relationship('TripPlace', backref='day', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, with_places=False, with_foods=False):
        result = {
            'day_index': self.day_index,
            'date': self.date.strftime('%Y-%m-%d'),
            'title': self.title,
            'summary': self.summary,
            'city': self.city,
            'weather': self.weather,
            'temperature': self.temperature,
            'accommodation': self.accommodation,
            'accommodation_price': float(self.accommodation_price) if self.accommodation_price else None
        }

        if with_places:
            from app.models.trip_place import TripPlace
            places = TripPlace.query.filter_by(day_id=self.id).order_by(TripPlace.visit_order).all()
            result['places'] = [place.to_dict() for place in places]

        if with_foods:
            from app.models.trip_food import TripFood
            foods = TripFood.query.filter_by(day_id=self.id).all()
            result['foods'] = [food.to_dict() for food in foods]

        return result
