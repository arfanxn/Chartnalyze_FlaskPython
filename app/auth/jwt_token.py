from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, request

def create_jwt_token(user_id):
    return create_access_token(identity=user_id)

def jwt_protected():
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
