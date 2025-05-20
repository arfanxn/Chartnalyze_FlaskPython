from app.extensions import db
from app.models import User, Role, Post, Comment, Like
from app.enums.role_enums import RoleName
from app.enums.comment_enums import CommentableType
from app.enums.like_enums import LikeableType
from database.seeders.seeder import Seeder
from sqlalchemy.sql.expression import func
from faker import Faker

fake = Faker()

class LikeSeeder(Seeder):

    def run(self):
        super().run()

        users = User.query.all()

        posts = Post.query.all()
        
        for user in users:
            likes = []

            for post in posts:
                if fake.boolean() == False: continue
                
                like = Like()
                like.user_id = user.id
                like.likeable_id = post.id
                like.likeable_type = LikeableType.POST.value
                likes.append(like)

                comments = Comment.query.filter(
                    Comment.commentable_id == post.id,
                    Comment.commentable_type == CommentableType.POST.value
                ).order_by(func.rand()).limit(5).all()

                for comment in comments:
                    if fake.boolean() == False: continue
                    
                    like = Like()
                    like.user_id = user.id
                    like.likeable_id = comment.id
                    like.likeable_type = LikeableType.COMMENT.value
                    likes.append(like)

            try: 
                db.session.bulk_save_objects(likes)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e