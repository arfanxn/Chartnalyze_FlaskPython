from functools import wraps
from flask import g
from app.models import User
from werkzeug.exceptions import Forbidden
from http import HTTPStatus

def authorized(permissions):
    """
    Decorator for routes that require specific permissions.

    Args:
        permissions: A string, Permission instance, or a list of them.

    Raises:
        Forbidden: If the user is not logged in or does not have the required permissions.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            error_message = 'Forbidden action'

            # Check if the user is logged in
            if not hasattr(g, 'user'):
                raise Forbidden(error_message)

            user:User = g.user

            # Check if the user has the required permissions
            if not user.has_permissions(permissions):
                raise Forbidden(error_message)

            # If the checks pass, call the original route
            return f(*args, **kwargs)
        return decorated
    return decorator
