from app.repositories.repository import Repository
from app.extensions import db
from app.models import Post, Follow, User
from flask import request
from flask_sqlalchemy.query import Query
from flask_query_builder.querying import QueryBuilder, AllowedFilter, AllowedSort
from werkzeug.exceptions import NotFound
from slugify import slugify
from sqlalchemy.orm import aliased
import ulid

class FollowRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        follower_name = request.args.get('filter[follower.name]', None)
        followed_name = request.args.get('filter[followed.name]', None)
        joins = request.args.get('join', '').split(',')
        sorts = request.args.get('sort', '').split(',')

        Follower = aliased(User)
        Followed = aliased(User)

        query = db.session.query(Follow)

        if 'follower' in joins:
            query = query.options(db.joinedload(Follow.follower)).join(Follower, Follow.follower_id == Follower.id)

            if follower_name is not None:
                query = query.filter(Follower.name.contains(follower_name))

            if '-follower.name' in sorts:
                query = query.order_by(Follower.name.desc())
            elif 'follower.name' in sorts:
                query = query.order_by(Follower.name)
        if 'followed' in joins:
            query = query.options(db.joinedload(Follow.followed)).join(Followed, Follow.followed_id == Followed.id)

            if followed_name is not None:
                query = query.filter(Followed.name.contains(followed_name))

            if '-followed.name' in sorts:
                query = query.order_by(Followed.name.desc())
            elif 'followed.name' in sorts:
                query = query.order_by(Followed.name)

        return query        
    
    def paginate_followers_of(self, followed_id: str) -> tuple[list[Follow], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query().filter(Follow.followed_id == followed_id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        follows = []
        for follow in pagination.items:
            follows.append(follow)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (follows, meta)

    def paginate_followeds_of(self, follower_id: str) -> tuple[list[Follow], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query().filter(Follow.follower_id == follower_id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        follows = []
        for follow in pagination.items:
            follows.append(follow)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (follows, meta)
    
    def toggle_follow(self, follower_id: str, followed_id: str) -> tuple[bool]:
        follow = Follow.query.filter(
            db.and_(Follow.follower_id == follower_id, Follow.followed_id == followed_id)
        ).first()

        if follow is None:
            follow = Follow()
            follow.follower_id = follower_id
            follow.followed_id = followed_id
            db.session.add(follow)
            is_following = True
        else: 
            db.session.delete(follow)
            is_following = False

        return (is_following, )