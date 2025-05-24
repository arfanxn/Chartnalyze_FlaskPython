import hmac
from functools import wraps
from flask import request
from app.config import Config
from werkzeug.exceptions import Unauthorized


def api_key_verified(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get API key from header
        api_key = request.headers.get('X-API-Key')
        
        # Secure comparison to prevent timing attacks
        if not api_key or not hmac.compare_digest(api_key, Config.API_KEY):
            raise Unauthorized("Invalid or missing API key")

        return f(*args, **kwargs)
    return decorated