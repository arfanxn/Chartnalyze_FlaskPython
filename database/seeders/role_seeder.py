from app.extensions import db
from app.models import Role, Permission
from database.seeders.seeder import Seeder
from datetime import date

class RoleSeeder(Seeder):

    def run(self):
        permissions = Permission.query.all()

        # TODO add permissions to analyst and user 
        role_map  = {
            'root': permissions,
            'analyst': [],
            'user': []
        }

        for role_name, permissions in role_map.items():
            role = Role()
            role.name = role_name
            role.permissions.extend(permissions)
            db.session.add(role)
        db.session.commit()
