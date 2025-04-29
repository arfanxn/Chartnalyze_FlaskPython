# seeders.py
from flask import Flask

def register_test_commands(app: Flask):

    @app.cli.command('demo')
    def demo():
        with app.app_context():
            print('Demo...')
