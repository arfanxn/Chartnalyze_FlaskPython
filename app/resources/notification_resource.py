from app.resources import Resource
from app.models import Notification
from sqlalchemy import inspect

class NotificationResource(Resource): 
    def __init__(self, entity: Notification):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'notifiable_id': entity.notifiable_id,
            'notifiable_type': entity.notifiable_type,
            'type': entity.type,
            'title': entity.title if entity.title is not None else None,
            'message': entity.message,
            'data': entity.data if entity.data is not None else None,
            'read_at': entity.read_at.isoformat() if entity.read_at is not None else None,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        # ins = inspect(entity)
        # if 'relation' not in ins.unloaded:
        #     from app.resources import RelationResource
        #     data['relation']  = RelationResource.collection(entity.relation) 

        return data