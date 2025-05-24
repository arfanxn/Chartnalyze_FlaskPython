from functools import wraps
from flask import g
from app.models.user import User
from werkzeug.exceptions import Unauthorized, Forbidden

def email_verified(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user: User = g.user
        if user == None:
            raise Unauthorized('Unauthorized action')

        if user.email_verified_at == None:
            raise Forbidden('Email not verified')
        
        return func(*args, **kwargs)
    return wrapper