from app.extensions import db
from datetime import datetime
import bcrypt
import ulid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(16), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    roles = db.relationship(
        'Role', 
        secondary='role_user',  # Use table name as string
        back_populates='users'  # Match the name in Role model
    )

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.password = hashed_password

    def check_password(self, password):
        return bcrypt.checkpw(password=password, hashed_password=self.password)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'birth_date': self.birth_date.isoformat() if self.birth_date is not None else None,
            'email': self.email,
            'email_verified_at': self.email_verified_at.isoformat() if self.email_verified_at is not None else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None
        }
