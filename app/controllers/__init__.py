from app.controllers.apis import api_bp
from app.controllers.test_controller import test_bp
from app.helpers.file_helpers import get_public_folder_path
from flask import Blueprint, send_from_directory

# Create web blueprint
web_bp = Blueprint('web', __name__, url_prefix='/')

# Register module blueprints under web blueprint
web_bp.register_blueprint(test_bp)

@web_bp.route('/public/<path:filename>', methods=['GET'])
def serve_public(filename):
    return send_from_directory(get_public_folder_path(), filename)

def register_blueprints(app):
    # Register test blueprint directly
    app.register_blueprint(web_bp)
    
    # Register API blueprint
    app.register_blueprint(api_bp)