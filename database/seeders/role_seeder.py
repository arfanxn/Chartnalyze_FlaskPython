from app.extensions import db
from app.models import Role, Permission
from app.enums.role_enums import RoleName
from database.seeders.seeder import Seeder
from datetime import date

class RoleSeeder(Seeder):

    def run(self):
        super().run()

        permissions = Permission.query.all()

        # TODO add permissions to analyst and user 
        role_map  = {
            RoleName.ADMIN.value: permissions,
            RoleName.ANALYST.value: [],
            RoleName.USER.value: []
        }

        for name, permissions in role_map.items():
            role = Role()
            role.name = name
            role.permissions.extend(permissions)
            db.session.add(role)
        db.session.commit()
