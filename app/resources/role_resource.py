from app.resources import Resource
from app.models import Role, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class RoleResource(Resource): 
    def __init__(self, entity: Role):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'name': entity.name,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        ins = inspect(entity)

        if 'permissions' not in ins.unloaded:
            from app.resources import PermissionResource
            data['permissions']  = PermissionResource.collection(entity.permissions) if entity.permissions is not None and len(entity.permissions) > 0 else []

        return data