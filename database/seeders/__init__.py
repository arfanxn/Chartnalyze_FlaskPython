from database.seeders.permission_seeder import PermissionSeeder
from database.seeders.role_seeder import RoleSeeder
from database.seeders.user_seeder import UserSeeder
from database.seeders.seeder import Seeder

_registered_seeders: list[Seeder] = [
    PermissionSeeder(),
    RoleSeeder(),
    UserSeeder(),
]

def run_registered_seeders ():
    for seeder in _registered_seeders:
        seeder.run()