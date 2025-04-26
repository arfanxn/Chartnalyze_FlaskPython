from app.controllers.test_controller import test_bp
from app.controllers.apis import api_bp

def register_blueprints(app):
    # Register test blueprint directly
    app.register_blueprint(test_bp)
    
    # Register API blueprint
    app.register_blueprint(api_bp)