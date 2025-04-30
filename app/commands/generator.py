import click
import os
import secrets
from dotenv import load_dotenv, set_key
from flask import Flask

def register_generator_commands(app: Flask):
    @app.cli.command('generate-secret-key')
    @click.option('--length', type=int, default=32, help='Length of the secret key')
    @click.option('--env-file', type=str, default='.env', help='Path to the .env file')
    @click.option('--key-name', type=str, default='SECRET_KEY', help='Name of the secret key in the .env file')
    def generate_secret_key(length, env_file, key_name):
        with app.app_context():
            print('Generating secret key...')
            try:
                secret_key = secrets.token_urlsafe(length)

                if os.path.exists(env_file):
                    load_dotenv(env_file)
                    set_key(env_file, key_name, secret_key)
                else:
                    set_key(env_file, key_name, secret_key)

                print(f"Secret key generated in: {env_file}")
            except Exception as e:
                print('Error:', str(e))

