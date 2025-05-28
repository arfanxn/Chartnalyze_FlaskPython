from app.repositories.repository import Repository
from app.extensions import db
from app.forms import StoreCommentForm
from app.models import Comment, Comment, Like
from flask import request
from flask_sqlalchemy.query import Query
from werkzeug.exceptions import NotFound
import ulid

class CommentRepository(Repository):

    def __init__(self):
        super().__init__()

    def _tuple_to_model(self, comment_tuple: tuple[Comment, int]) -> Comment:
        if comment_tuple is None:
            return None
        comment, like_count = comment_tuple
        comment.like_count = like_count if like_count is not None else 0
        return comment

    def query(self) -> Query:
        joins = request.args.get('join', '').split(',')
        sorts = request.args.get('sort', '').split(',')
        body = request.args.get('filter[body]', None)
        
        like_count_subquery = db.session.query(
                Like.likeable_id,
                db.func.count(Like.id).label('like_count')
            )\
            .group_by(Like.likeable_id)\
            .subquery()
        
        query = db.session.query(
                Comment,
                like_count_subquery.c.like_count
            )\
            .outerjoin(like_count_subquery, like_count_subquery.c.likeable_id == Comment.id)
        
        if len(joins) > 0:
            if 'user' in joins:
                query = query.options(db.joinedload(Comment.user))
        
        if body is not None: 
            query = query.filter(Comment.body.contains(body))
        
        if len(sorts) > 0:
            if '-created_at' in sorts:
                query = query.order_by(Comment.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Comment.created_at)
        
        return query        

    def paginate(self, user_id: str|None = None, commentable_id: str|None = None) -> tuple[list[Comment], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        if user_id is not None:
            query = query.filter(Comment.user_id == user_id)
        if commentable_id is not None:
            query = query.filter(Comment.commentable_id == commentable_id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        comments = []
        for comment_tuple in pagination.items:
            comment = self._tuple_to_model(comment_tuple)
            comments.append(comment)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (comments, meta)
    
    def show (self, comment_id: str) -> tuple[Comment]:
        comment_tuple = self.query()\
            .filter(Comment.id == comment_id)\
            .first()
        
        comment = self._tuple_to_model(comment_tuple)
        if comment is None:
            raise NotFound('Comment not found')

        return (comment, )
    
    def store(self, form: StoreCommentForm, user_id: str, commentable_id : str, commentable_type: str) -> tuple[Comment]:
        comment = Comment()
        comment.id = ulid.new().str    
        comment.user_id = user_id
        comment.commentable_id = commentable_id
        comment.commentable_type = commentable_type
        comment.parent_id = form.parent_id.data
        comment.body = form.body.data
        db.session.add(comment)
        return (comment, )

    def destroy(self, comment: Comment) -> tuple[bool]:
        db.session.delete(comment)
        return (True, )
