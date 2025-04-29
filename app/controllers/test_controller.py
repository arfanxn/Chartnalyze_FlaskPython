from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from app.helpers.response_helpers import create_response_tuple
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import  date
from http import HTTPStatus


test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    user: User = User.query.first()
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User found successfully', 
        data={
            'user': user.to_json(),
            'user_roles': user.roles[0].to_json()
        }
    )
    