from app.resources import Resource
from app.models import Activity
from app.enums.activity_enums import CauserType, SubjectType, Type
from sqlalchemy import inspect 

class ActivityResource(Resource): 
    def __init__(self, entity: Activity):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'type': entity.type,
            'description': entity.description,
            'subject_id': entity.subject_id,
            'subject_type': entity.subject_type,
            'causer_id': entity.causer_id,
            'causer_type': entity.causer_type,
            'properties': entity.properties,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at else None
        }
        
        ins = inspect(entity)

        if 'subject_user' not in ins.unloaded:
            from app.resources import UserResource
            data['subject']  = UserResource(entity.subject).to_json() if entity.subject is not None else None

        if 'causer_user' not in ins.unloaded:
            from app.resources import UserResource
            data['causer']  = UserResource(entity.causer).to_json() if entity.causer is not None else None

        return data