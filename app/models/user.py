from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(64), unique=True, comment='微信OpenID')
    union_id = db.Column(db.String(64), comment='微信UnionID')
    nickname = db.Column(db.String(64), comment='用户昵称')
    avatar_url = db.Column(db.String(255), comment='头像URL')
    gender = db.Column(db.SmallInteger, comment='性别：0未知，1男，2女')
    country = db.Column(db.String(64), comment='国家')
    province = db.Column(db.String(64), comment='省份')
    city = db.Column(db.String(64), comment='城市')
    phone = db.Column(db.String(20), comment='手机号')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    last_login_at = db.Column(db.DateTime, comment='最后登录时间')

    # 关联关系
    trips = db.relationship('Trip', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'avatarUrl': self.avatar_url,
            'gender': self.gender,
            'country': self.country,
            'province': self.province,
            'city': self.city
        }
