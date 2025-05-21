from app.extensions import db
from app.models import Role, Permission
from app.enums.role_enums import RoleName
from app.enums.permission_enums import PermissionName   
from database.seeders.seeder import Seeder
from datetime import date

class RoleSeeder(Seeder):

    def run(self):
        super().run()

        analyst_permission_names = [
            # TODO: add more permissions
            PermissionName.USERS_INDEX.value,
            PermissionName.USERS_SHOW.value,
        ]
        user_permission_names = [
            # TODO: add more permissions
            PermissionName.USERS_INDEX.value,
            PermissionName.USERS_SHOW.value,
        ]

        permissions = Permission.query.all()
        analyst_permissions = Permission.query.filter(Permission.name.in_(analyst_permission_names)).all()
        user_permissions = Permission.query.filter(Permission.name.in_(user_permission_names)).all()

        role_map  = {
            RoleName.ADMIN.value: permissions,
            RoleName.ANALYST.value: analyst_permissions,
            RoleName.USER.value: user_permissions,
        }

        for name, permissions in role_map.items():
            role = Role()
            role.name = name
            role.permissions.extend(permissions)
            db.session.add(role)
        db.session.commit()
