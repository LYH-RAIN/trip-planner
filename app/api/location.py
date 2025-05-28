from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.location_service import LocationService
from app.utils.response_util import success_response, error_response

location_bp = Blueprint('location', __name__)


@location_bp.route('/districts', methods=['GET'])
@jwt_required()
def get_districts():
    """
    获取行政区域
    """
    keywords = request.args.get('keywords')
    subdistrict = int(request.args.get('subdistrict', 1))

    result, error = LocationService.get_districts(keywords, subdistrict)
    if error:
        return jsonify(error_response(code=400, message=error)), 400

    return jsonify(success_response(data=result))


@location_bp.route('/search', methods=['GET'])
@jwt_required()
def search_places():
    """
    搜索地点
    """
    keyword = request.args.get('keyword')
    city = request.args.get('city')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))

    if not keyword:
        return jsonify(error_response(code=400, message="缺少参数keyword")), 400

    result, error = LocationService.search_places(keyword, city, page, page_size)
    if error:
        return jsonify(error_response(code=400, message=error)), 400

    return jsonify(success_response(data=result))


@location_bp.route('/detail', methods=['GET'])
@jwt_required()
def get_place_detail():
    """
    获取地点详情
    """
    place_id = request.args.get('id')

    if not place_id:
        return jsonify(error_response(code=400, message="缺少参数id")), 400

    result, error = LocationService.get_place_detail(place_id)
    if error:
        return jsonify(error_response(code=400, message=error)), 400

    return jsonify(success_response(data=result))


@location_bp.route('/around', methods=['GET'])
@jwt_required()
def search_around():
    """
    周边搜索
    """
    location = request.args.get('location')
    radius = int(request.args.get('radius', 3000))
    types = request.args.get('type')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))

    if not location:
        return jsonify(error_response(code=400, message="缺少参数location")), 400

    result, error = LocationService.search_around(location, radius, types, page, page_size)
    if error:
        return jsonify(error_response(code=400, message=error)), 400

    return jsonify(success_response(data=result))
