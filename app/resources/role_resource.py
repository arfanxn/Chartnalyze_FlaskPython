from app.resources import Resource
from app.models import Role, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class RoleResource(Resource): 
    def __init__(self, model: Role):
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

        if 'permissions' not in ins.unloaded:
            from app.resources import PermissionResource
            data['permissions']  = PermissionResource.collection(model.permissions) if model.permissions is not None and len(model.permissions) > 0 else []

        return data