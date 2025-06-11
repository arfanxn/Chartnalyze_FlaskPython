from app.resources import Resource
from app.models import Activity
from sqlalchemy import inspect 

class ActivityResource(Resource): 
    def __init__(self, entity: Activity):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'user_id': entity.user_id,
            'user_agent': entity.user_agent,
            'user_ip_address': entity.user_ip_address,
            'type': entity.type,
            'description': entity.description,
            'subject_id': entity.subject_id,
            'subject_type': entity.subject_type,
            'properties': entity.properties,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at else None
        }
        
        ins = inspect(entity)

        if 'subject_user' not in ins.unloaded:
            from app.resources import UserResource
            data['subject']  = UserResource(entity.subject).to_json() if entity.subject is not None else None

        if 'user' not in ins.unloaded:
            from app.resources import UserResource
            data['user']  = UserResource(entity.user).to_json() if entity.user is not None else None

        return data