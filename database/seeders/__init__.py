from database.seeders.country_seeder import CountrySeeder
from database.seeders.permission_seeder import PermissionSeeder
from database.seeders.role_seeder import RoleSeeder
from database.seeders.user_seeder import UserSeeder
from database.seeders.notification_seeder import NotificationSeeder
from database.seeders.seeder import Seeder

_registered_seeders: list[Seeder] = [
    CountrySeeder(),
    PermissionSeeder(),
    RoleSeeder(),
    UserSeeder(),
    NotificationSeeder(),
]

def run_registered_seeders ():
    for seeder in _registered_seeders:
        seeder.run()