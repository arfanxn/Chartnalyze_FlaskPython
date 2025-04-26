from flask import Blueprint
from .user_controller import user_bp
from app.exceptions.validation_exception import ValidationException
from app.exceptions.http_exception import HttpException
from app.helpers.response_helpers import create_response_tuple
from http import HTTPStatus

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register user blueprint under API blueprint
api_bp.register_blueprint(user_bp)

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