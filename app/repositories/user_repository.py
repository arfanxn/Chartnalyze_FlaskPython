from app.repositories.repository import Repository
from app.extensions import db
from app.models import User
from flask import request
from flask_sqlalchemy.query import Query

class UserRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        sorts = request.args.get('sort', '').split(',')
        joins = request.args.get('join', '').split(',')
        filter = request.args.get('filter', None)
        name = request.args.get('filter[name]', None)
        email = request.args.get('filter[email]', None)
        username = request.args.get('filter[username]', None)

        query = db.session.query(User)

        if filter is not None:
            if filter is not None:
                query = query.filter(db.or_(
                    User.name.contains(filter),
                    User.email.contains(filter),
                    User.username.contains(filter)
                ))
            else:
                if name is not None:
                    query = query.filter(User.name.contains(name))
                if email is not None:
                    query = query.filter(User.email.contains(email))
                if username is not None:
                    query = query.filter(User.username.contains(username))
    
        if sorts is not None and len(sorts) > 0:
            if '-name' in sorts:
                query = query.order_by(User.name.desc())
            elif 'name' in sorts:
                query = query.order_by(User.name)
            if '-email' in sorts:
                query = query.order_by(User.email.desc())
            elif 'email' in sorts:
                query = query.order_by(User.email)
            if '-created_at' in sorts:
                query = query.order_by(User.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(User.created_at)
        
        if 'roles' in joins:
            query = query.options(db.joinedload(User.roles))

        return query        
    
    def paginate(self) -> tuple[list[User], dict]: 
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        users = []
        for user in pagination.items:
            users.append(user)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (users, meta)

    def show (self, user_identifier : str) -> tuple[User]:
        user = self.query().filter(db.or_(
            User.id == user_identifier,
            User.email == user_identifier,
            User.username == user_identifier
        )).first()
        return (user, )