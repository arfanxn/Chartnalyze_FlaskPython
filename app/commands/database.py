# seeders.py
from flask import Flask
from database import seeders

def register_database_commands(app: Flask):

    @app.cli.command('db-seed')
    def db_seed():
        with app.app_context():
            print('Seeding database...')
            seeders.run_registered_seeders()
            print('Database seeded')