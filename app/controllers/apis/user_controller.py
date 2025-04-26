from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register(): 
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    user = UserService.create_user(name, email, password)
    return jsonify({"message": "User created successfully", "user": UserSchema().dump(user)}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")
    
    user = UserService.find_by_id(name)
    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401
