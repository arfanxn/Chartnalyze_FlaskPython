from flask import Flask
from app.commands.database import register_database_commands
from app.commands.generator import register_generator_commands

def register_commands(app: Flask):

    register_database_commands(app)
    register_generator_commands(app)