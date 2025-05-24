from flask import Blueprint
from .user_controller import user_bp
from .otp_controller import otp_bp
from .follow_controller import follow_bp    
from .role_controller import role_bp
from .permission_controller import permission_bp
from .notification_controller import notification_bp
from .watched_asset_controller import watched_asset_bp
from app.exceptions import ValidationException, HttpException
from app.helpers.response_helpers import create_response_tuple
from http import HTTPStatus

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register module blueprints under API blueprint
api_bp.register_blueprint(otp_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(follow_bp)
api_bp.register_blueprint(role_bp)
api_bp.register_blueprint(permission_bp)
api_bp.register_blueprint(notification_bp)
api_bp.register_blueprint(watched_asset_bp)

# Register error handlers for the API blueprint
@api_bp.errorhandler(ValidationException)
def handle_validation_error(e: ValidationException):
    return create_response_tuple(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        message=str(e),
        additionals={'errors': e.errors}
    )

@api_bp.errorhandler(HttpException)
def handle_http_error(e: HttpException):
    return create_response_tuple(
        status=e.status,
        message=str(e),
        additionals=e.additionals if e.additionals is not None else None
    )

@api_bp.errorhandler(429)
def handle_limit_error(error):
    return create_response_tuple(
        status=HTTPStatus.TOO_MANY_REQUESTS,
        message=f"Too many requests, {error.description}, please try again later",
    )