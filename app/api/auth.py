from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.response_util import success_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/wechat/login', methods=['POST'])
def wechat_login():
    """
    微信登录
    """
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify(error_response(code=400, message="缺少参数code")), 400

    result, error = AuthService.wechat_login(code)
    if error:
        return jsonify(error_response(code=400, message=error)), 400

    return jsonify(success_response(data=result))


@auth_bp.route('/user/info', methods=['PUT'])
@jwt_required()
def update_user_info():
    """
    更新用户信息
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    result, error = AuthService.update_user_info(user_id, data)
    if error:
        return jsonify(error_response(code=400, message=error)), 400

    return jsonify(success_response(data=result))
