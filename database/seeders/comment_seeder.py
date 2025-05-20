from app.extensions import db
from app.models import User, Post, Role, Comment
from app.enums.role_enums import RoleName
from app.enums.comment_enums import CommentableType
from database.seeders.seeder import Seeder
from faker import Faker
import ulid

fake = Faker()

class CommentSeeder(Seeder):

    def run(self):
        """
        Seeds comments for posts and replies to comments.

        Comments are divided into two types: analyst comments and user comments.
        Analyst comments are replies to posts and are limited to 10 per post.
        User comments are replies to posts or other comments and are limited to 20 per post.
        Replies to comments are limited to 5 replies per comment for analysts and 10 replies per comment for users.

        The comment body is a single sentence.

        The seed data is saved to the database after generation.
        If any error occurs during generation or saving, the transaction is rolled back and the error is re-raised.
        """
        # Call parent run method (if it contains any setup logic)
        super().run()

        # Query all users who have the 'ANALYST' role
        analyst_users = User.query.filter(User.roles.any(Role.name == RoleName.ANALYST.value)).all()
        # Query all users who have the 'USER' role
        users = User.query.filter(User.roles.any(Role.name == RoleName.USER.value)).all()

        # Get all posts to seed comments for
        posts = Post.query.all()

        # Initialize list to hold Comment objects before bulk insert
        comments = []

        # Loop through each post to generate comments
        for post in posts:

            # Generate random number of analyst comments for this post (between 1 and 10)
            analyst_comment_count = fake.random_int(min=1, max=5, step=1)
            # Generate random number of user comments for this post (between 10 and 20)
            user_comment_count = fake.random_int(min=1, max=5, step=1)
            # Total comments for this post
            comment_count = analyst_comment_count + user_comment_count

            # Create each comment
            for i in range(comment_count):
                # Assign user either from analyst group or user group based on index
                if i < analyst_comment_count:
                    user = fake.random_element(elements=analyst_users)
                else:
                    user = fake.random_element(elements=users)

                # Generate a random sentence as the comment body
                body = fake.sentence()

                # Create a new Comment instance and set its properties
                comment = Comment()
                comment.id = ulid.new().str
                comment.user_id = user.id,
                comment.commentable_id = post.id
                comment.commentable_type = CommentableType.POST.value
                comment.parent_id = None  # top-level comment, no parent
                comment.body = body
                
                # Add comment to list for bulk saving later
                comments.append(comment)

        # Attempt to bulk save all comments at once for performance
        try:
            db.session.bulk_save_objects(comments)
            db.session.commit()
        except Exception as e:
            # Rollback on failure to keep DB consistent
            db.session.rollback()
            # Re-raise error for further handling/logging
            raise e
        
        # Initialize list to hold replies to comments
        rcs = []
        
        # Loop through each comment (typo in original: should be 'comments' plural)
        for comment in comments:

            # Generate random number of analyst replies per comment (1-5)
            analyst_rc_count = fake.random_int(min=1, max=5, step=1)
            # Generate random number of user replies per comment (5-10)
            user_rc_count = fake.random_int(min=1, max=5, step=1)
            # Total replies for this comment
            comment_count = analyst_rc_count + user_rc_count

            # Create each reply comment
            for i in range(comment_count):
                # Assign user either analyst or user group for the reply
                if i < analyst_rc_count:
                    user = fake.random_element(elements=analyst_users)
                else:
                    user = fake.random_element(elements=users)

                # Generate reply comment body
                body = fake.sentence()

                # Create new Comment instance for reply
                rc = Comment()
                rc.user_id = user.id
                rc.commentable_id = post.id
                rc.commentable_type = CommentableType.POST.value
                rc.parent_id = comment.id  # set parent comment reference
                rc.body = body
                
                # Add reply comment to list for bulk saving
                rcs.append(rc)

        # Bulk save all reply comments with the same commit/rollback pattern
        try:
            db.session.bulk_save_objects(rcs)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
