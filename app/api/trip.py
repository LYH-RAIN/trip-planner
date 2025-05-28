from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.trip_service import TripService
from app.utils.response_util import success_response, error_response

trip_bp = Blueprint('trip', __name__)


@trip_bp.route('', methods=['POST'])
@jwt_required()
def create_trip():
    """
    创建行程
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    # 验证必填参数
    required_fields = ['title', 'departure', 'startDate', 'endDate']
    for field in required_fields:
        if field not in data:
            return jsonify(error_response(code=400, message=f"缺少参数{field}")), 400

    result = TripService.create_trip(user_id, data)

    return jsonify(success_response(data=result))


@trip_bp.route('', methods=['GET'])
@jwt_required()
def get_trip_list():
    """
    获取行程列表
    """
    user_id = get_jwt_identity()
    status = request.args.get('status', 'all')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    result = TripService.get_trip_list(user_id, status, page, page_size)

    return jsonify(success_response(data=result))


@trip_bp.route('/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip_detail(trip_id):
    """
    获取行程详情
    """
    user_id = get_jwt_identity()

    result, error = TripService.get_trip_detail(trip_id, user_id)
    if error:
        return jsonify(error_response(code=404, message=error)), 404

    return jsonify(success_response(data=result))


@trip_bp.route('/<int:trip_id>/overview', methods=['GET'])
@jwt_required()
def get_trip_overview(trip_id):
    """
    获取行程总览
    """
    user_id = get_jwt_identity()

    result, error = TripService.get_trip_overview(trip_id, user_id)
    if error:
        return jsonify(error_response(code=404, message=error)), 404

    return jsonify(success_response(data=result))


@trip_bp.route('/<int:trip_id>/days/<int:day_index>', methods=['GET'])
@jwt_required()
def get_trip_day_detail(trip_id, day_index):
    """
    获取行程日程详情
    """
    user_id = get_jwt_identity()

    result, error = TripService.get_trip_day_detail(trip_id, day_index, user_id)
    if error:
        return jsonify(error_response(code=404, message=error)), 404

    return jsonify(success_response(data=result))


@trip_bp.route('/<int:trip_id>/foods', methods=['GET'])
@jwt_required()
def get_trip_foods(trip_id):
    """
    获取行程美食攻略
    """
    user_id = get_jwt_identity()

    result, error = TripService.get_trip_foods(trip_id, user_id)
    if error:
        return jsonify(error_response(code=404, message=error)), 404

    return jsonify(success_response(data=result))


@trip_bp.route('/<int:trip_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_trip(trip_id):
    """
    取消行程
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('confirm'):
        return jsonify(error_response(code=400, message="请确认取消行程")), 400

    result, error = TripService.cancel_trip(trip_id, user_id)
    if error:
        return jsonify(error_response(code=404, message=error)), 404

    return jsonify(success_response(data=result))
