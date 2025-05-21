from app.extensions import db
from app.models import Permission
from app.enums.permission_enums import PermissionName
from database.seeders.seeder import Seeder

class PermissionSeeder(Seeder):

    def run(self):
        super().run()
        
        permissionNames = [
            PermissionName.ALL.value,

            PermissionName.USERS_INDEX.value,
            PermissionName.USERS_SHOW.value,
            PermissionName.USERS_STORE.value,
            PermissionName.USERS_UPDATE.value,
            PermissionName.USERS_DESTROY.value,

            PermissionName.ROLES_INDEX.value,
            PermissionName.ROLES_SHOW.value,
            PermissionName.ROLES_STORE.value,
            PermissionName.ROLES_UPDATE.value,
            PermissionName.ROLES_DESTROY.value,

            PermissionName.PERMISSIONS_INDEX.value,
            PermissionName.PERMISSIONS_SHOW.value,
            PermissionName.PERMISSIONS_STORE.value,
            PermissionName.PERMISSIONS_UPDATE.value,
            PermissionName.PERMISSIONS_DESTROY.value
        ]
        for permissionName in permissionNames:
            permission = Permission()
            permission.name = permissionName
            db.session.add(permission)
        db.session.commit()
        