from app.enums.save_enums import SaveableType
from app.resources import Resource
from app.models import Save
from sqlalchemy import inspect

class SaveResource(Resource): 
    def __init__(self, entity: Save):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'user_id': entity.user_id,
            'saveable_id': entity.saveable_id,
            'saveable_type': entity.saveable_type,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        ins = inspect(entity)

        if 'user' not in ins.unloaded:
            from app.resources import UserResource
            data['user']  = UserResource(entity.user).to_json()

        if 'saveable_post' not in ins.unloaded and entity.saveable_type == SaveableType.POST.value:
            from app.resources import PostResource
            data['saveable'] = PostResource(entity.saveable).to_json()  if entity.saveable is not None else None

        return data