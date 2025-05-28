from app import db
from datetime import datetime


class AIModelCall(db.Model):
    __tablename__ = 'ai_model_calls'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    trip_id = db.Column(db.BigInteger, db.ForeignKey('trips.id'), comment='关联行程ID')
    prompt = db.Column(db.Text, nullable=False, comment='输入提示词')
    response = db.Column(db.Text, comment='AI返回结果')
    model_name = db.Column(db.String(64), comment='模型名称')
    call_type = db.Column(db.String(32), comment='调用类型：trip_generate, trip_update, etc')
    status = db.Column(db.SmallInteger, default=0, comment='状态：0处理中，1成功，2失败')
    error_message = db.Column(db.String(255), comment='错误信息')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关联关系
    user = db.relationship('User', backref='ai_calls')
    trip = db.relationship('Trip', backref='ai_calls')
