from flask import Flask

def register_test_commands(app: Flask):

    @app.cli.command('test_command')
    def test_command():
        with app.app_context():
            print('Test command...')

