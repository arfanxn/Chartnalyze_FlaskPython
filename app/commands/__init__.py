from flask import Flask
from app.commands.database import register_database_commands
from app.commands.generator import register_generator_commands
from app.commands.scraper import register_scraper_commands
from app.commands.test import register_test_commands

def register_commands(app: Flask):

    register_database_commands(app)
    register_generator_commands(app)
    register_scraper_commands(app)
    register_test_commands(app)