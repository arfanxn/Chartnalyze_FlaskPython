from app.resources import Resource
from app.models import Like, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class LikeResource(Resource): 
    def __init__(self, entity: Like):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'user_id': entity.user_id,
            'likeable_id': entity.likeable_id,
            'likeable_type': entity.likeable_type,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        ins = inspect(entity)

        if 'user' not in ins.unloaded:
            from app.resources import UserResource
            data['user']  = UserResource(entity.user).to_json()

        if 'likeable_post' not in ins.unloaded:
            from app.resources import PostResource
            data['likeable'] = PostResource(entity.likeable).to_json()  if entity.likeable is not None else None
        elif 'likeable_comment' not in ins.unloaded:
            from app.resources import CommentResource
            data['likeable'] = CommentResource(entity.likeable).to_json()  if entity.likeable is not None else None

        return data