from app.extensions import db
from app.models import Permission
from app.enums.permission_enums import PermissionName
from database.seeders.seeder import Seeder

class PermissionSeeder(Seeder):

    def run(self):
        super().run()
        
        permissionNames = [perm.value for perm in PermissionName]

        permissions = []
        for permissionName in permissionNames:
            permission = Permission()
            permission.name = permissionName
            permissions.append(permission)

        db.session.bulk_save_objects(permissions)
        db.session.commit()
        