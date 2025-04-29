from database.seeders.permission_seeder import PermissionSeeder
from database.seeders.role_seeder import RoleSeeder
from database.seeders.user_seeder import UserSeeder
from database.seeders.seeder import Seeder

def run ():
    seeders = [
        Seeder(),
        PermissionSeeder(),
        RoleSeeder(),
        UserSeeder(),
    ]

    for seeder in seeders:
            seeder.run()