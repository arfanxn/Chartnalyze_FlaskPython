from flask import Blueprint, request, jsonify
from datetime import  date
from app.models.user import User
from  app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    user = User()
    user.name = "test"
    user.birth_date = date(2000, 1, 1)
    user.email = "test@test.com" 
    user.set_password("11112222")

    db.session.add(user)
    db.session.commit()

    return jsonify(UserSchema().dump(user)), 200
