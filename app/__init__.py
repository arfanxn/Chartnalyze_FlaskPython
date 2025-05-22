from flask import Flask
from app.extensions import cors,db, jwt, limiter, mail, migrate
from app.config import Config
from app.controllers import register_blueprints
from app.commands import register_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions

    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register commands
    register_commands(app)

    # Register Blueprints
    register_blueprints(app)

    return app
