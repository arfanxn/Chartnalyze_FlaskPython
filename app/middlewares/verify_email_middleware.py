from functools import wraps
from flask import g
from app.exceptions.http_exception import HttpException
from app.models.user import User
from http import HTTPStatus

def verify_email(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user: User = g.user
        if user == None:
            raise HttpException(message='Unauthorized action', status=HTTPStatus.UNAUTHORIZED)

        if user.email_verified_at == None:
            raise HttpException(message='Email not verified', status=HTTPStatus.FORBIDDEN)
        
        return func(*args, **kwargs)
    return wrapper