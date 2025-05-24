from functools import wraps
from flask import g
from app.extensions import db
from app.models.user import User
from werkzeug.exceptions import Unauthorized
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        error_message = 'Unauthorized action'

        # Verify the JWT token in the request
        verify_jwt_in_request() 
        
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Check if the user exists in the database
        user = User.query.options(db.joinedload(User.roles)).filter_by(id=user_id).first()
        if not user:
            raise Unauthorized(error_message)

        # Set the user in `g` for use in the route function
        g.user = user

        # Proceed with the original function if everything is fine
        return f(*args, **kwargs)
    return decorated
