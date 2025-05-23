from app.resources import Resource
from app.models import Permission, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class PermissionResource(Resource): 
    def __init__(self, model: Permission):
        self.model = model

    def to_json(self):
        model = self.model

        data = {
            'id': model.id,
            'name': model.name,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat() if model.updated_at is not None else None,
        }

        ins = inspect(model)

        if 'roles' not in ins.unloaded:
            from app.resources import RoleResource
            data['roles']  = RoleResource.collection(model.roles) if model.roles is not None and len(model.roles) > 0 else []

        return data