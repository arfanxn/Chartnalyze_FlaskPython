from app.extensions import db
from sqlalchemy import inspect
from datetime import datetime
import ulid

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    name = db.Column(db.String(50), nullable=False, unique=True)
    iso_code = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    users = db.relationship('User', lazy='dynamic', back_populates='country')

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

        # Relationships
        insp = inspect(self)
        if (insp.attrs.users.loaded and self.users):
            data['users'] = [user.to_json() for user in self.users]

        return data
