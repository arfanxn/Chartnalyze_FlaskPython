import os

class Config:
    # The environment variables that are injected into application
    APP_NAME = os.getenv('APP_NAME')
    APP_URL = os.getenv('APP_URL')
    API_KEY= os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'True') == 'True'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_EXPIRE_ON_COMMIT = os.getenv('SQLALCHEMY_EXPIRE_ON_COMMIT', 'True') == 'True'
    MONGO_URI = os.getenv('MONGO_URI')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))  # Make sure PORT is int
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
    OAUTHLIB_RELAX_TOKEN_SCOPE = os.getenv('OAUTHLIB_RELAX_TOKEN_SCOPE', 'True') == 'True'
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT', 'True') == 'True'

    # The environment variables that are used without injection
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    LIMITER_DEFAULT_LIMITS = os.getenv('LIMITER_DEFAULT_LIMITS').split(',')
    OTP_EXPIRATION_MINUTES = int(os.getenv('OTP_EXPIRATION_MINUTES'))
    JWT_EXPIRATION_DAYS = int(os.getenv('JWT_EXPIRATION_DAYS'))
