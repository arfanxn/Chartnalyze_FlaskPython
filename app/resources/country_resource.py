from app.resources import Resource
from app.models import Country
from sqlalchemy import inspect  # Add this import
from app.config import Config

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
        if 'user' not in ins.unloaded:
            data['user']  = model.user    

        return data