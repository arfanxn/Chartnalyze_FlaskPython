from app.extensions import db
from datetime import datetime, timedelta
from app.config import Config
import random
import ulid
import math

class Otp(db.Model):
    __tablename__ = 'otps'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    email = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Integer(), nullable=False, default=lambda: random.randint(100000, 999999))  # 6-digit OTP code
    used_at = db.Column(db.DateTime, nullable=True)
    revoked_at = db.Column(db.DateTime, nullable=True)
    expired_at = db.Column(db.DateTime, nullable=False, default=datetime.now() + timedelta(minutes=Config.OTP_EXPIRATION_MINUTES))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def expiration_minutes(self):
        return math.ceil((self.expired_at - datetime.now()).total_seconds() / 60)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'code': self.code,
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'revoked_at': self.revoked_at.isoformat() if self.revoked_at else None,
            'expired_at': self.expired_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
