from app.resources import Resource
from app.models import Follow
from sqlalchemy import inspect  # Add this import
from app.config import Config

class FollowResource(Resource): 
    def __init__(self, model: Follow):
        self.model = model

    def to_json(self):
        model = self.model

        data = {
            'id': model.id,
            'follower_id': model.follower_id,
            'followed_id': model.followed_id,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat() if model.updated_at is not None else None,
        }

        ins = inspect(model)

        if 'follower' not in ins.unloaded:
            from app.resources import UserResource
            data['follower']  = UserResource(model.follower).to_json() if model.follower is not None else None

        if 'followed' not in ins.unloaded:
            from app.resources import UserResource
            data['followed']  = UserResource(model.followed).to_json() if model.followed is not None else None

        return data