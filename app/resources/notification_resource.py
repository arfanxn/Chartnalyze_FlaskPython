from app.resources import Resource
from app.models import Notification
from sqlalchemy import inspect

class NotificationResource(Resource): 
    def __init__(self, model: Notification):
        self.model = model

    def to_json(self):
        model = self.model

        data = {
            'id': model.id,
            'notifiable_id': model.notifiable_id,
            'notifiable_type': model.notifiable_type,
            'type': model.type,
            'title': model.title if model.title is not None else None,
            'message': model.message,
            'data': model.data if model.data is not None else None,
            'read_at': model.read_at.isoformat() if model.read_at is not None else None,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat() if model.updated_at is not None else None,
        }

        # ins = inspect(model)
        # if 'relation' not in ins.unloaded:
        #     from app.resources import RelationResource
        #     data['relation']  = RelationResource.collection(model.relation) 

        return data