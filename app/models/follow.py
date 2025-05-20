from app.extensions import db
from datetime import datetime
import ulid

class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    follower_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    follower = db.relationship('User', foreign_keys=[follower_id])
    followed = db.relationship('User', foreign_keys=[followed_id])


    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'iso_code': self.iso_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
