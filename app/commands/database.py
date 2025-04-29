# seeders.py
from flask import Flask
from database import seeders

def register_database_commands(app: Flask):

    @app.cli.command('seed-database')
    def seed_database():
        with app.app_context():
            print('Seeding database...')
            seeders.run()
            print('Database seeded.')