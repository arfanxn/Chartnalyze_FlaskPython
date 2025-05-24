from app.resources import Resource
from app.models import Permission, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class PermissionResource(Resource): 
    def __init__(self, entity: Permission):
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

        if 'roles' not in ins.unloaded:
            from app.resources import RoleResource
            data['roles']  = RoleResource.collection(entity.roles) if entity.roles is not None and len(entity.roles) > 0 else []

        return data