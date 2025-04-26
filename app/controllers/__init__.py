from flask import Blueprint
from app.controllers.apis.user_controller import user_bp
from app.controllers.test_controller import test_bp
from app.exceptions.validation_exception import ValidationException
from http import HTTPStatus

def register_blueprints(app):
    # Register the test blueprint
    app.register_blueprint(test_bp)

    # Register the API blueprint
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api_bp.register_blueprint(user_bp)
    
    # Error handler specifically for ValidationException within the API blueprint
    @api_bp.errorhandler(ValidationException)
    def handle_validation_error(e: ValidationException):
        status = HTTPStatus.UNPROCESSABLE_ENTITY
        return {
            'message': str(e),
            'errors': e.errors,
            'status': status
        }, status

    # Register API blueprint to app
    app.register_blueprint(api_bp)
