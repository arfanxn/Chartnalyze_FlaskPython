from app.extensions import db
from app.models import User, Role
from database.seeders.seeder import Seeder
from datetime import date

class UserSeeder(Seeder):

    def run(self):
        super().run()

        roles = Role.query.all()

        user_list = [
            {
                'username': 'root',
                'roles': [role for role in roles if role.name == 'root']
            },
            {
                'username': 'analyst',
                'roles': [role for role in roles if role.name == 'analyst']
            },
            {
                'username': 'user',
                'roles': [role for role in roles if role.name == 'user']
            }
        ]

        for user_map in user_list: 
            user = User()
            user.name = user_map['username'].capitalize()
            user.username = user_map['username']
            user.birth_date = date(2000, 1, 1)
            user.email = user_map['username']+'@chartnalyze.edu'
            user.password = '11112222'
            user.roles.extend(user_map['roles'])
            db.session.add(user)        

        db.session.commit()