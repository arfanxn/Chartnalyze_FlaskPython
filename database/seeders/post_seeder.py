from app.extensions import db
from app.models import User, Post, Role, RoleUser
from app.enums.role_enums import RoleName
from database.seeders.seeder import Seeder
from faker import Faker

fake = Faker()

class PostSeeder(Seeder):

    def run(self):
        super().run()

        users = User.query.options(db.joinedload(User.roles)).all()

        posts = []

        for user in users:

            post_count = fake.random_int(min=0, max=5, step=1)

            for _ in range(post_count):
                title = ' '.join(fake.words(nb=fake.random_int(min=1, max=4))) if fake.boolean() else None
                paragraph_count = fake.random_int(min=1, max=5, step=1)
                body = '\n\n'.join(fake.paragraphs(nb=paragraph_count))

                post = Post()
                post.user_id = user.id,
                post.title = title
                post.slug = fake.slug()
                post.body = body
                
                posts.append(post)

        try:
            db.session.bulk_save_objects(posts)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
