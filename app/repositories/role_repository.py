from app.repositories.repository import Repository
from app.extensions import db
from app.models import Role, User
from flask import request
from flask_sqlalchemy.query import Query
from flask_query_builder.querying import QueryBuilder, AllowedFilter, AllowedSort
from werkzeug.exceptions import NotFound, Forbidden
from sqlalchemy import text

class RoleRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        sorts = request.args.get('sort', '').split(',')
        joins = request.args.get('join', '').split(',')

        query = Role.query

        query = QueryBuilder(Role, query=query)\
            .allowed_filters([
                AllowedFilter.partial('name'),
            ])\
            .query
    
        if sorts is not None and len(sorts) > 0:
            if '-name' in sorts:
                query = query.order_by(Role.name.desc())
            elif 'name' in sorts:
                query = query.order_by(Role.name)
            if '-created_at' in sorts:
                query = query.order_by(Role.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Role.created_at)
        
        if 'permissions' in joins:
            query = query.options(db.joinedload(Role.permissions))

        return query        
    
    def paginate(self) -> tuple[list[Role], dict]: 
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        roles = []
        for role in pagination.items:
            roles.append(role)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (roles, meta)

    def show (self, role_identifier : str) -> tuple[Role]:
        role = self.query().filter(db.or_(
            Role.id == role_identifier,
            Role.name == role_identifier
        )).first()
        return (role, )
    