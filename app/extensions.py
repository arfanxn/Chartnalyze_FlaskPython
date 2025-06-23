from google_auth_oauthlib.flow import Flow
from ultralytics import YOLO
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from app.config import Config

# Flask extensions
cors = CORS()
db = SQLAlchemy()
mongo = PyMongo()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=Config.LIMITER_DEFAULT_LIMITS)
mail = Mail()
migrate = Migrate()

# Non Flask extensions
flow = None
candlestick_ml_model = None

def register_extensions(app):
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    mongo.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    global flow
    global candlestick_ml_model

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": Config.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": Config.GOOGLE_OAUTH_CLIENT_SECRET,
                "auth_uri": Config.GOOGLE_OAUTH_AUTH_URI,
                "token_uri": Config.GOOGLE_OAUTH_TOKEN_URI,
                "redirect_uris": Config.GOOGLE_OAUTH_REDIRECT_URIS,
            },
        },
        scopes=Config.GOOGLE_OAUTH_SCOPES,
        redirect_uri=Config.GOOGLE_OAUTH_REDIRECT_URIS[0],
    )

    candlestick_ml_model = YOLO(Config.CANDLESTICK_YOLO_V8_MODEL_PATH.format(root_path=app.root_path))
    if (candlestick_ml_model is None): raise Exception('candlestick_ml_model is None')