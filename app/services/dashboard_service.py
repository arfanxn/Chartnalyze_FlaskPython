import types
from app.services import Service
from app.models import Role, Permission, User, Follow, Post, Comment, Like, Save
from app.extensions import db
from app.enums.role_enums import RoleName
from app.enums.like_enums import LikeableType
from app.enums.comment_enums import CommentableType 
from app.enums.save_enums import SaveableType


class DashboardService(Service):
    def __init__(self):
        super().__init__()

    def index(self) -> tuple[any]:
        # Role counts subquery
        role_counts = db.session.query(
            db.func.count(Role.id).label('total_all_roles'),
        ).subquery()

        # Role counts subquery
        permission_counts = db.session.query(
            db.func.count(Permission.id).label('total_all_permissions')
        ).subquery()

        # User counts subquery
        user_counts = db.session.query(
            db.func.count(User.id).label('total_all_users'),
            db.func.count(
                db.case(
                    (User.roles.any(Role.name == RoleName.ADMIN.value), 1),
                    else_=None
                )
            ).label('total_admin_users'),
            db.func.count(
                db.case(
                    (User.roles.any(Role.name == RoleName.ANALYST.value), 1),
                    else_=None
                )
            ).label('total_analyst_users'),
            db.func.count(
                db.case(
                    (User.roles.any(Role.name == RoleName.USER.value), 1),
                    else_=None
                )
            ).label('total_user_users')
        ).subquery()

        # Follow counts subquery
        follow_counts = db.session.query(
            db.func.count(Follow.id).label('total_all_follows')
        ).subquery()

        # Post counts subquery
        post_counts = db.session.query(
            db.func.count(Post.id).label('total_all_posts'),
            db.func.count(
                db.case(
                    (Post.user.has(User.roles.any(Role.name == RoleName.ADMIN.value)), 1),
                    else_=None
                )
            ).label('total_admin_posts'),
            db.func.count(
                db.case(
                    (Post.user.has(User.roles.any(Role.name == RoleName.ANALYST.value)), 1),
                    else_=None
                )
            ).label('total_analyst_posts'),
            db.func.count(
                db.case(
                    (Post.user.has(User.roles.any(Role.name == RoleName.USER.value)), 1),
                    else_=None
                )
            ).label('total_user_posts')
        ).subquery()

        # Like counts subquery
        like_counts = db.session.query(
            db.func.count(
                db.case(
                    (Like.likeable_type == LikeableType.POST.value, Like.id),
                    else_=None
                )
            ).label('total_all_post_likes'),
            db.func.count(
                db.case(
                    (Like.likeable_type == LikeableType.COMMENT.value, Like.id),
                    else_=None
                )
            ).label('total_all_comment_likes')
        ).subquery()
        
        # Comment counts subquery
        comment_counts = db.session.query(
            db.func.count(
                db.case(
                    (Comment.commentable_type == CommentableType.POST.value, Comment.id),
                    else_=None
                )
            ).label('total_all_post_comments'),
        ).subquery()

        # Save counts subquery
        save_counts = db.session.query(
            db.func.count(
                db.case(
                    (Save.saveable_type == SaveableType.POST.value, Save.id),
                    else_=None
                )
            ).label('total_all_saved_posts'),
        ).subquery()

        result = db.session.query(
            role_counts.c.total_all_roles,

            permission_counts.c.total_all_permissions,

            user_counts.c.total_all_users,
            user_counts.c.total_admin_users,
            user_counts.c.total_analyst_users,
            user_counts.c.total_user_users,

            follow_counts.c.total_all_follows,

            post_counts.c.total_all_posts,
            post_counts.c.total_admin_posts,
            post_counts.c.total_analyst_posts,
            post_counts.c.total_user_posts,

            like_counts.c.total_all_post_likes,
            like_counts.c.total_all_comment_likes,


            comment_counts.c.total_all_post_comments,

            save_counts.c.total_all_saved_posts,
        ).first()

        result = types.SimpleNamespace(**result._mapping)
        
        return (result, )