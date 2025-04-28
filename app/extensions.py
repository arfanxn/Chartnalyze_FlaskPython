from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config

limiter = Limiter(get_remote_address, default_limits=Config.FLASK_DEFAULT_LIMITS)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
