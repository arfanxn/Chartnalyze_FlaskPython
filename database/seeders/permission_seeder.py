from app.extensions import db
from app.models import Permission
from database.seeders.seeder import Seeder
from datetime import date

class PermissionSeeder(Seeder):

    def run(self):
        permissionNames = [
            '*', 
            'users.index', 'users.show', 'users.store', 'users.update', 'users.destroy',
            'roles.index', 'roles.show', 'roles.store', 'roles.update', 'roles.destroy',
            'permissions.index', 'permissions.show', 'permissions.store', 'permissions.update', 'permissions.destroy'
        ]
        for permissionName in permissionNames:
            permission = Permission()
            permission.name = permissionName
            db.session.add(permission)
        db.session.commit()
        