from app.resources import Resource
from app.models import User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class UserResource(Resource): 
    def __init__(self, model: User):
        self.model = model

    def to_json(self):
        model = self.model

        data = {
            'id': model.id,
            'country_id': model.country_id,
            'name': model.name,
            'username': model.username,
            'birth_date': model.birth_date.isoformat() if model.birth_date is not None else None,
            'email': model.email,
            'email_verified_at': model.email_verified_at.isoformat() if model.email_verified_at is not None else None,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat() if model.updated_at is not None else None,
        }

        ins = inspect(model)
        if 'avatar' not in ins.unloaded:
            avatar = self.avatar
            data['avatar_url']  = f"{Config.APP_URL}/public/images/avatars/{avatar.file_name}"

        return data