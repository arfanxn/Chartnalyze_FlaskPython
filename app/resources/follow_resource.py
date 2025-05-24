from app.resources import Resource
from app.models import Follow
from sqlalchemy import inspect  # Add this import
from app.config import Config

class FollowResource(Resource): 
    def __init__(self, entity: Follow):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'follower_id': entity.follower_id,
            'followed_id': entity.followed_id,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        ins = inspect(entity)

        if 'follower' not in ins.unloaded:
            from app.resources import UserResource
            data['follower']  = UserResource(entity.follower).to_json() if entity.follower is not None else None

        if 'followed' not in ins.unloaded:
            from app.resources import UserResource
            data['followed']  = UserResource(entity.followed).to_json() if entity.followed is not None else None

        return data