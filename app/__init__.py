from flask import Flask, Blueprint
from app.extensions import db, jwt, migrate
from app.config import Config
from app.controllers.apis.user_controller import user_bp
from app.controllers.test_controller import test_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # testing 
    app.register_blueprint(test_bp)

    # apis
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api_bp.register_blueprint(user_bp)

    app.register_blueprint(api_bp)

    return app
