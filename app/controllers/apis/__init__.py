from flask import Blueprint
from .user_controller import user_bp
from .otp_controller import otp_bp
from .follow_controller import follow_bp    
from .role_controller import role_bp
from .permission_controller import permission_bp
from .notification_controller import notification_bp
from .watched_asset_controller import watched_asset_bp
from .post_controller import post_bp
from .comment_controller import comment_bp
from .like_controller import like_bp
from .save_controller import save_bp
from .activity_controller import activity_bp
from .dashboard_controller import dashboard_bp
from werkzeug.exceptions import HTTPException, UnprocessableEntity, TooManyRequests
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
api_bp.register_blueprint(post_bp)
api_bp.register_blueprint(comment_bp)
api_bp.register_blueprint(like_bp)
api_bp.register_blueprint(save_bp)
api_bp.register_blueprint(activity_bp)
api_bp.register_blueprint(dashboard_bp)

@api_bp.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity_error(e: UnprocessableEntity):
    status = HTTPStatus.UNPROCESSABLE_ENTITY
    errors = e.description

    if not isinstance(errors, dict):
        message = errors
        return create_response_tuple(status=status,message=message)
    
    for m in errors.values().__iter__().__next__():
        message=m
        break
    return create_response_tuple(
        status=status,
        message=message,
        additionals={'errors': errors}
    )

@api_bp.errorhandler(TooManyRequests)
def handle_too_many_requests_error(error: TooManyRequests):
    return create_response_tuple(
        status=HTTPStatus.TOO_MANY_REQUESTS,
        message=f"Too many requests, {error.description}, please try again later",
    )

@api_bp.errorhandler(HTTPException)
def handle_http_error(e: HTTPException):
    return create_response_tuple(
        status=e.code,
        message=e.description
    )