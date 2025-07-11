from app.repositories.repository import Repository
from app.extensions import db
from app.forms import SavePostForm
from app.models import Post, Comment, Like, Save, User, Role, RoleUser
from app.enums.comment_enums import CommentableType
from app.enums.like_enums import LikeableType
from app.enums.save_enums import SaveableType
from flask import request
from flask_sqlalchemy.query import Query
from werkzeug.exceptions import NotFound
import types
import ulid

class PostRepository(Repository):

    def __init__(self):
        super().__init__()

    def _tuple_to_model(self, post_tuple: tuple[Post, int, int]) -> Post:
        if post_tuple is None:
            return None
        
        post, comment_count, like_count = post_tuple

        post.comment_count = comment_count if comment_count is not None else 0
        post.like_count = like_count if like_count is not None else 0
        return post

    def statistics (self, user_id: str|None = None) -> tuple[list]:
        post_count_sq = db.select(db.func.count(Post.id))\
            .where(Post.user_id == User.id)\
            .correlate_except(Post).scalar_subquery().label('post_count')

        comment_count_sq = db.select(db.func.count(Comment.id))\
            .join(Post, db.and_(
                Post.id == Comment.commentable_id,
                Comment.commentable_type == CommentableType.POST.value
            ))\
            .where(Post.user_id == User.id)\
            .correlate_except(Comment, Post).scalar_subquery().label('comment_count')
        
        like_count_sq = db.select(db.func.count(Like.id))\
            .join(Post, db.and_(
                Post.id == Like.likeable_id,
                Like.likeable_type == LikeableType.POST.value
            ))\
            .where(Post.user_id == User.id)\
            .correlate_except(Like, Post).scalar_subquery().label('like_count')
        
        save_count_sq = db.select(db.func.count(Save.id))\
            .join(Post, db.and_(
                Post.id == Save.saveable_id,
                Save.saveable_type == SaveableType.POST.value
            ))\
            .where(Post.user_id == User.id)\
            .correlate_except(Save, Post).scalar_subquery().label('save_count')

        query = db.session.query(
            post_count_sq,
            comment_count_sq,
            like_count_sq,
            save_count_sq,
        )

        if user_id is not None:
            query = query.filter(User.id == user_id)

        result = query.first()

        if not result:
            raise NotFound('User not found')

        statistics = types.SimpleNamespace(**result._mapping)

        return (statistics,)


    def query(self) -> Query:
        joins = request.args.get('join', '').split(',')
        sorts = request.args.get('sort', '').split(',')
        filter = request.args.get('filter', None)
        title = request.args.get('filter[title]', None)
        body = request.args.get('filter[body]', None)
        role = request.args.get('filter[user.role]', None)

        comment_count_subquery = db.session.query(
                Comment.commentable_id,
                db.func.count(Comment.id).label('comment_count')
            )\
            .group_by(Comment.commentable_id)\
            .subquery()
        
        like_count_subquery = db.session.query(
                Like.likeable_id,
                db.func.count(Like.id).label('like_count')
            )\
            .group_by(Like.likeable_id)\
            .subquery()
        
        query = db.session.query(
                Post,
                comment_count_subquery.c.comment_count,
                like_count_subquery.c.like_count
            )\
            .outerjoin(comment_count_subquery, comment_count_subquery.c.commentable_id == Post.id)\
            .outerjoin(like_count_subquery, like_count_subquery.c.likeable_id == Post.id)

        if 'user' in joins:
            query = query.options(db.joinedload(Post.user))

        if filter is not None:
            query = query.filter(db.or_(
                Post.id == filter,
                Post.title.contains(filter),
                Post.body.contains(filter),
            ))
        else:
            if title is not None:
                query = query.filter(Post.title.contains(title))
            if body is not None:
                query = query.filter(Post.body.contains(body))
            
        if role is not None:
            query = query.join(User).join(RoleUser).join(Role).filter(db.or_(
                Role.id == role,
                Role.name == role,
            ))
        
        if sorts is not None and len(sorts) > 0:
            if '-created_at' in sorts:
                query = query.order_by(Post.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Post.created_at)
        
        return query        

    def paginate(self, user_id: str|None = None) -> tuple[list[Post], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        if user_id is not None:
            query = query.filter(Post.user_id == user_id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        posts = []
        for post_tuple in pagination.items:
            post = self._tuple_to_model(post_tuple)
            posts.append(post)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (posts, meta)
    
    def show (self, post_id: str) -> tuple[Post]:
        post_tuple = self.query()\
            .filter(Post.id == post_id)\
            .first()
        
        post = self._tuple_to_model(post_tuple)
        if post is None:
            raise NotFound('Post not found')

        return (post, )
    
    def store(self, form: SavePostForm, user_id : str) -> tuple[Post]:
        post = Post()
        post.id = ulid.new().str    
        post.user_id = user_id
        post.title = form.title.data
        post.body = form.body.data
        post.generate_slug()
        db.session.add(post)
        return (post, )
    
    def update(self, form: SavePostForm, post_id : str) -> tuple[Post]:
        post, = self.show(post_id=post_id)

        if post is None:
            raise NotFound('Post not found')

        post.title = form.title.data
        post.body = form.body.data
        if post.title != form.title.data:
            post.generate_slug()

        return (post, )

    def destroy(self, post_id: str) -> tuple[bool]:
        affected_rows = Post.query.filter(Post.id == post_id).delete(synchronize_session=False)

        if affected_rows == 0:
            raise NotFound('Post not found')

        return (True, )
