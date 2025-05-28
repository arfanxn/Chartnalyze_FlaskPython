from app.repositories import PermissionRepository
from app.services import Service
from app.models import Permission
from werkzeug.exceptions import NotFound

permission_repository = PermissionRepository()

class PermissionService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (self) -> tuple[list[Permission], dict]:
        permissions, meta = permission_repository.paginate()
        return (permissions, meta)
    
    def show(self, permission_id: str) -> tuple[Permission]:
        permission = permission_repository.show(permission_id=permission_id)
        if permission is None:
            raise NotFound('Permission not found')
        return (permission, )