from database.seeders.user_seeder import UserSeeder
from database.seeders.seeder import Seeder

def run ():
    seeders = [
        Seeder(),
        UserSeeder()
    ]

    for seeder in seeders:
            seeder.run()