from app.resources import Resource
from app.models import Country
from sqlalchemy import inspect

class CountryResource(Resource): 
    def __init__(self, entity: Country):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'name': entity.name,
            'iso_code': entity.iso_code,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        ins = inspect(entity)
        if 'users' not in ins.unloaded:
            from app.resources import UserResource
            data['users']  = UserResource.collection(entity.users) 

        return data