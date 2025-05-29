from app.repositories.repository import Repository
from app.extensions import db
from app.models import Like
from flask import request
from flask_sqlalchemy.query import Query
from werkzeug.exceptions import NotFound

class LikeRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        joins = request.args.get('join', '').split(',')
        sorts = request.args.get('sort', '').split(',')
        
        query = Like.query
        
        if len(joins) > 0:
            if 'user' in joins:
                query = query.options(db.joinedload(Like.user))
            if 'likeable' in joins:
                query = query.options(db.joinedload(Like.likeable_post))
                query = query.options(db.joinedload(Like.likeable_comment))
        
        if len(sorts) > 0:
            if '-created_at' in sorts:
                query = query.order_by(Like.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Like.created_at)
        
        return query        

    def paginate(self, user_id: str|None = None, likeable_id: str|None = None, likeable_type: str|None = None) -> tuple[list[Like], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        if user_id is not None:
            query = query.filter(Like.user_id == user_id)
        if likeable_id is not None:
            query = query.filter(Like.likeable_id == likeable_id)
        if likeable_type is not None:
            query = query.filter(Like.likeable_type == likeable_type)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        likes = []
        for like in pagination.items:
            likes.append(like)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (likes, meta)
    
    def show (self, like_id: str) -> tuple[Like]:
        like = self.query()\
            .filter(Like.id == like_id)\
            .first()
        if like is None:
            raise NotFound('Like not found')

        return (like, )
    
    def toggle(self, user_id : str, likeable_id: str, likeable_type: str) -> tuple[bool]:
        like = Like.query\
            .filter(
                Like.user_id == user_id,
                Like.likeable_id == likeable_id, 
                Like.likeable_type == likeable_type
            ).first()
        
        if like is None:
            like = Like()
            like.user_id = user_id
            like.likeable_id = likeable_id
            like.likeable_type = likeable_type
            db.session.add(like)
            is_liked = True
        else:
            db.session.delete(like)
            is_liked = False

        return (is_liked, )