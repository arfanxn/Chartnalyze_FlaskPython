from app.config import Config   
from app.extensions import db
from app.models import User, Country, Role
from app.enums.role_enums import RoleName
from database.seeders.seeder import Seeder
from faker import Faker

fake = Faker()

class UserSeeder(Seeder):

    def run(self):
        super().run()

        countries = db.session.query(Country.id).all()
        roles = Role.query.all()

        users = []

        for i in range(len(roles)):
            role = roles[i]

            for j in range(5):
                country_id = fake.random_element(elements=countries).id if fake.boolean() else None
                created_at = fake.date_time_between(start_date='-1y', end_date='now')
                email_verified_at = fake.date_time_between(start_date=created_at, end_date='now') if fake.boolean() else None

                user = User()
                user.country_id = country_id
                user.name = fake.name()
                user.birth_date = fake.date_of_birth()
                
                # the first user in each role group will have the role name as their username and email
                # so that we can easily login as each role when testing
                if j == 0:
                    user.username = role.name
                    user.email = f"{role.name}@{Config.APP_NAME}.edu".lower()
                else :
                    user.username = fake.user_name()[:16]
                    user.email = fake.email()

                user.email_verified_at = email_verified_at
                user.password = '11112222'   
                user.created_at = created_at
                user.roles.extend([role]) 

                users.append(user)

        try:
            db.session.add_all(users)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
