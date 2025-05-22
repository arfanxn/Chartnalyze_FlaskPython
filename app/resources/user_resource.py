from app.resources import Resource
from app.models import User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class UserResource(Resource): 
    def __init__(self, model: User):
        self.model = model

    def to_json(self):
        data = {
            'id': self.id,
            'country_id': self.country_id,
            'name': self.name,
            'username': self.username,
            'birth_date': self.birth_date.isoformat() if self.birth_date is not None else None,
            'email': self.email,
            'email_verified_at': self.email_verified_at.isoformat() if self.email_verified_at is not None else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

        ins = inspect(self.model)
        if 'avatar' not in ins.unloaded:
            avatar = self.avatar
            data['avatar_url']  = f"{Config.APP_URL}/public/images/avatars/{avatar.file_name}"

        return data