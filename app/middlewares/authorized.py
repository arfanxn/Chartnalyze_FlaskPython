from functools import wraps
from flask import g
from app.models import User
from app.exceptions import HttpException
from http import HTTPStatus

def authorized(permissions):
    """
    Decorator for routes that require specific permissions.

    Args:
        permissions: A string, Permission instance, or a list of them.

    Raises:
        HttpException: If the user is not logged in or does not have the required permissions.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Check if the user is logged in
            if not hasattr(g, 'user'):
                raise HttpException(
                    status=HTTPStatus.FORBIDDEN,
                    message='Forbidden action'
                )

            user:User = g.user

            # Check if the user has the required permissions
            if not user.has_permissions(permissions):
                raise HttpException(
                    status=HTTPStatus.FORBIDDEN,
                    message='Forbidden action'
                )

            # If the checks pass, call the original route
            return f(*args, **kwargs)
        return decorated
    return decorator
