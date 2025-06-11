from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from app.extensions import cors, db, mongo, jwt, limiter, mail, migrate
from app.config import Config
from app.controllers import register_blueprints
from app.commands import register_commands

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Initialize extensions

    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    mongo.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register commands
    register_commands(app)

    # Register Blueprints
    register_blueprints(app)

    return app
