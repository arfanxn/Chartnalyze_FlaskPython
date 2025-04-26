from functools import wraps
from flask import request, g, jsonify
from http import HTTPStatus
from app.models.user import User
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        unauthorized_response = {
            "message": "Unauthorized action.",
            "status": HTTPStatus.UNAUTHORIZED
        }, HTTPStatus.UNAUTHORIZED

        try:
            # Verify the JWT token in the request
            verify_jwt_in_request() 
            
            # Get the user ID from the JWT token
            user_id = get_jwt_identity()

            # Check if the user exists in the database
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return unauthorized_response

            # Set the user in `g` for use in the route function
            g.user = user

        except Exception as e:
            # You can log the exception for debugging purposes
            return unauthorized_response

        # Proceed with the original function if everything is fine
        return f(*args, **kwargs)
    return decorated
