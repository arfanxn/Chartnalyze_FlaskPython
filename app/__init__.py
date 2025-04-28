from flask import Flask
from app.extensions import limiter, db, jwt, migrate
from app.config import Config
from app.controllers import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    limiter.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    register_blueprints(app)

    return app
