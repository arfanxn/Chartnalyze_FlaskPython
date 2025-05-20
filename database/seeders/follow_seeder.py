from app.extensions import db
from app.models import User, Follow, Role, RoleUser
from app.enums.role_enums import RoleName
from database.seeders.seeder import Seeder
from faker import Faker

fake = Faker()

class FollowSeeder(Seeder):

    def run(self):
        super().run()

        analyst_users = User.query.filter(User.roles.any(Role.name == RoleName.ANALYST.value)).all()
        users = User.query.filter(User.roles.any(Role.name == RoleName.USER.value)).all()

        follows = []

        for analyst_user in analyst_users:
            for user in users:
                if fake.boolean == False: continue

                follow = Follow()
                follow.follower_id = user.id,
                follow.followed_id = analyst_user.id,
                follows.append(follow)

        try:
            db.session.bulk_save_objects(follows)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
