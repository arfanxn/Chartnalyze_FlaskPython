from app.resources import Resource
from app.models import User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class UserResource(Resource): 
    def __init__(self, entity: User):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'country_id': entity.country_id,
            'name': entity.name,
            'username': entity.username,
            'birth_date': entity.birth_date.isoformat() if entity.birth_date is not None else None,
            'email': entity.email,
            'email_verified_at': entity.email_verified_at.isoformat() if entity.email_verified_at is not None else None,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        ins = inspect(entity)

        if 'roles' not in ins.unloaded:
            from app.resources import RoleResource
            role = entity.role
            data['role'] = RoleResource(role).to_json()

        if 'avatar' not in ins.unloaded:
            avatar = entity.avatar    
            data['avatar_url']  = f"{Config.API_URL}/public/images/avatars/{avatar.file_name}" if avatar is not None else None

        if 'country' not in ins.unloaded:
            from app.resources import CountryResource
            data['country']  = CountryResource(entity.country).to_json() if entity.country is not None else None

        if 'posts' not in ins.unloaded:
            from app.resources import PostResource
            data['posts']  = PostResource.collection(entity.posts)

        return data