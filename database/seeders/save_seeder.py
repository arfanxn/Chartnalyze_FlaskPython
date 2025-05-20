from app.extensions import db
from app.models import User, Post, Save
from app.enums.save_enums import SaveableType
from database.seeders.seeder import Seeder
from faker import Faker

fake = Faker()

class SaveSeeder(Seeder):

    def run(self):
        super().run()

        users = User.query.all()
        posts = Post.query.all()

        saves = []

        for user in users:
            for post in posts:
                if fake.boolean() == False: 
                    continue

                save = Save()
                save.user_id = user.id
                save.saveable_id = post.id
                save.saveable_type = SaveableType.POST.value
                saves.append(save)

        try:
            db.session.bulk_save_objects(saves)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


