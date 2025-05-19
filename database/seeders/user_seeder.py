from app.extensions import db
from app.models import User, Country, Role
from database.seeders.seeder import Seeder
from datetime import date

class UserSeeder(Seeder):

    def run(self):
        super().run()

        indonesia_country = Country.query.filter_by(iso_code='ID').first()

        roles = Role.query.all()
        root_role = [role for role in roles if role.name == 'root'][0]
        analyst_role = [role for role in roles if role.name == 'analyst'][0]
        user_role = [role for role in roles if role.name == 'user'][0]


        user_list = [
            {
                'username': 'root',
                'roles': [root_role]
            },
            {
                'username': 'analyst',
                'roles': [analyst_role]
            },
            {
                'username': 'user',
                'roles': [user_role]
            }
        ]

        for user_dict in user_list: 
            user = User()
            user.country_id = indonesia_country.id
            user.name = user_dict['username'].capitalize()
            user.username = user_dict['username']
            user.birth_date = date(2000, 1, 1)
            user.email = user_dict['username']+'@chartnalyze.edu'
            user.password = '11112222'
            user.roles.extend(user_dict['roles'])
            db.session.add(user)        

        db.session.commit()