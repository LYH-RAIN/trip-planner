import pytest
import json
from datetime import datetime, date
from app.models.user import User
from app.models.trip import Trip
from app.models.trip_day import TripDay
from app.models.trip_place import TripPlace
from app.models.trip_food import TripFood


class TestUserModel:
    def test_user_creation(self, db):
        """测试用户创建"""
        user = User(
            open_id='test_open_id_1',
            nickname='Test User 1',
            avatar_url='http://example.com/avatar1.jpg',
            gender=1
        )
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(open_id='test_open_id_1').first()
        assert saved_user is not None
        assert saved_user.nickname == 'Test User 1'
        assert saved_user.gender == 1

    def test_user_to_dict(self, test_user):
        """测试用户转字典"""
        user_dict = test_user.to_dict()
        assert user_dict['id'] == test_user.id
        assert user_dict['nickname'] == test_user.nickname
        assert user_dict['avatarUrl'] == test_user.avatar_url
        assert user_dict['gender'] == test_user.gender


class TestTripModel:
    def test_trip_creation(self, db, test_user):
        """测试行程创建"""
        start_date = date(2023, 5, 1)
        end_date = date(2023, 5, 3)

        trip = Trip(
            user_id=test_user.id,
            title='Weekend Trip',
            start_date=start_date,
            end_date=end_date,
            days=3,
            departure='广州',
            status=0
        )
        trip.set_destinations(['深圳', '珠海'])
        trip.set_preferences(['美食', '购物'])

        db.session.add(trip)
        db.session.commit()

        saved_trip = Trip.query.filter_by(title='Weekend Trip').first()
        assert saved_trip is not None
        assert saved_trip.days == 3
        assert saved_trip.departure == '广州'
        assert '深圳' in saved_trip.get_destinations()
        assert '美食' in saved_trip.get_preferences()

    def test_trip_to_dict(self, test_trip):
        """测试行程转字典"""
        trip_dict = test_trip.to_dict()
        assert trip_dict['id'] == test_trip.id
        assert trip_dict['title'] == test_trip.title
        assert trip_dict['days'] == test_trip.days

        # 测试详细字典
        detailed_dict = test_trip.to_dict(simple=False)
        assert 'description' in detailed_dict
        assert 'preferences' in detailed_dict
        assert 'overview' in detailed_dict


class TestTripDayModel:
    def test_trip_day_creation(self, db, test_trip):
        """测试行程日程创建"""
        # 获取第一天
        day = TripDay.query.filter_by(trip_id=test_trip.id, day_index=1).first()
        assert day is not None
        assert day.title == 'DAY1'
        assert day.city == '广州'

        # 修改日程
        day.summary = '抵达韶关，游览南华寺'
        day.weather = '晴'
        day.temperature = '25°-30°'
        db.session.commit()

        updated_day = TripDay.query.get(day.id)
        assert updated_day.summary == '抵达韶关，游览南华寺'
        assert updated_day.weather == '晴'

    def test_trip_day_to_dict(self, db, test_trip):
        """测试行程日程转字典"""
        day = TripDay.query.filter_by(trip_id=test_trip.id, day_index=1).first()

        # 添加一个景点
        place = TripPlace(
            trip_id=test_trip.id,
            day_id=day.id,
            day_index=1,
            visit_order=1,
            name='测试景点',
            address='测试地址',
            city='广州',
            category='景点',
            is_highlight=1
        )
        db.session.add(place)
        db.session.commit()

        day_dict = day.to_dict(with_places=True)
        assert day_dict['day_index'] == 1
        assert day_dict['city'] == '广州'
        assert len(day_dict['places']) == 1
        assert day_dict['places'][0]['name'] == '测试景点'
