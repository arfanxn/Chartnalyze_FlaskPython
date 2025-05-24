from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from app.config import Config

cors = CORS()
db = SQLAlchemy()
mongo = PyMongo()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=Config.LIMITER_DEFAULT_LIMITS)
mail = Mail()
migrate = Migrate()