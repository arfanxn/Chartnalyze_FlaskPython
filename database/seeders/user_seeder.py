from app.extensions import db
from app.models.user import User
from database.seeders.seeder import Seeder
from datetime import date

class UserSeeder(Seeder):

    def run(self):
        # seed default user: root/root
        user = User()
        user.name = 'root'
        user.username = 'root'
        user.birth_date = date(2000, 1, 1)
        user.email = 'root@chartnalyze.edu'
        user.set_password('11112222')
        db.session.add(user)
        db.session.commit()