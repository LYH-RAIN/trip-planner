import pytest
from datetime import date, timedelta
from app import db
from app.models.user import User
from app.models.trip import Trip
from app.models.trip_day import TripDay
from app.models.trip_place import TripPlace
from app.models.trip_food import TripFood


class TestDatabaseIntegration:
    def test_trip_cascade_delete(self, app, test_user):
        """测试行程级联删除"""
        with app.app_context():
            # 创建行程
            start_date = date.today()
            end_date = start_date + timedelta(days=2)

            trip = Trip(
                user_id=test_user.id,
                title='Cascade Test Trip',
                start_date=start_date,
                end_date=end_date,
                days=3,
                departure='广州'
            )
            db.session.add(trip)
            db.session.commit()

            trip_id = trip.id

            # 创建行程日程
            day = TripDay(
                trip_id=trip_id,
                day_index=1,
                date=start_date,
                title='DAY1',
                city='广州'
            )
            db.session.add(day)
            db.session.commit()

            day_id = day.id

            # 创建行程景点
            place = TripPlace(
                trip_id=trip_id,
                day_id=day_id,
                day_index=1,
                visit_order=1,
                name='测试景点',
                address='测试地址',
                city='广州'
            )
            db.session.add(place)

            # 创建行程美食
            food = TripFood(
                trip_id=trip_id,
                day_id=day_id,
                day_index=1,
                name='测试美食',
                address='测试地址',
                city='广州'
            )
            db.session.add(food)
            db.session.commit()

            # 验证创建成功
            assert TripDay.query.filter_by(trip_id=trip_id).count() == 1
            assert TripPlace.query.filter_by(trip_id=trip_id).count() == 1
            assert TripFood.query.filter_by(trip_id=trip_id).count() == 1

            # 删除行程
            db.session.delete(trip)
            db.session.commit()

            # 验证级联删除
            assert TripDay.query.filter_by(trip_id=trip_id).count() == 0
            assert TripPlace.query.filter_by(trip_id=trip_id).count() == 0
            assert TripFood.query.filter_by(trip_id=trip_id).count() == 0

    def test_complex_queries(self, app, test_trip):
        """测试复杂查询"""
        with app.app_context():
            # 添加一些测试数据
            day1 = TripDay.query.filter_by(trip_id=test_trip.id, day_index=1).first()
            day2 = TripDay.query.filter_by(trip_id=test_trip.id, day_index=2).first()

            # 添加景点
            places = [
                TripPlace(trip_id=test_trip.id, day_id=day1.id, day_index=1, visit_order=1,
                          name='景点1', city='广州', is_highlight=1),
                TripPlace(trip_id=test_trip.id, day_id=day1.id, day_index=1, visit_order=2,
                          name='景点2', city='广州', is_highlight=0),
                TripPlace(trip_id=test_trip.id, day_id=day2.id, day_index=2, visit_order=1,
                          name='景点3', city='韶关', is_highlight=1)
            ]
            db.session.add_all(places)

            # 添加美食
            foods = [
                TripFood(trip_id=test_trip.id, day_id=day1.id, day_index=1,
                         name='美食1', city='广州', is_highlight=1),
                TripFood(trip_id=test_trip.id, day_id=day2.id, day_index=2,
                         name='美食2', city='韶关', is_highlight=0)
            ]
            db.session.add_all(foods)
            db.session.commit()

            # 测试查询：获取行程亮点
            highlights = TripPlace.query.filter_by(
                trip_id=test_trip.id, is_highlight=1
            ).order_by(TripPlace.day_index).all()

            assert len(highlights) == 2
            assert highlights[0].name == '景点1'
            assert highlights[1].name == '景点3'

            # 测试查询：获取特定城市的景点
            shaoguan_places = TripPlace.query.filter_by(
                trip_id=test_trip.id, city='韶关'
            ).all()

            assert len(shaoguan_places) == 1
            assert shaoguan_places[0].name == '景点3'

            # 测试查询：获取美食亮点
            food_highlights = TripFood.query.filter_by(
                trip_id=test_trip.id, is_highlight=1
            ).all()

            assert len(food_highlights) == 1
            assert food_highlights[0].name == '美食1'

            # 测试连接查询：获取特定日程的景点和美食
            from sqlalchemy import text

            sql = text("""
                SELECT p.name as place_name, f.name as food_name
                FROM trip_places p
                LEFT JOIN trip_foods f ON p.day_id = f.day_id
                WHERE p.trip_id = :trip_id AND p.day_index = 1
                ORDER BY p.visit_order
            """)

            result = db.session.execute(sql, {'trip_id': test_trip.id}).fetchall()

            assert len(result) == 2
            assert result[0].place_name == '景点1'
            assert result[0].food_name == '美食1'
            assert result[1].place_name == '景点2'
            assert result[1].food_name == '美食1'
