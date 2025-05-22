from app.resources import Resource
from app.models import Country
from sqlalchemy import inspect

class CountryResource(Resource): 
    def __init__(self, model: Country):
        self.model = model

    def to_json(self):
        model = self.model

        data = {
            'id': model.id,
            'name': model.name,
            'iso_code': model.iso_code,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat() if model.updated_at is not None else None,
        }

        ins = inspect(model)
        if 'users' not in ins.unloaded:
            from app.resources import UserResource
            data['users']  = UserResource.collection(model.users) 

        return data