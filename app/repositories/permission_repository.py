from app.repositories.repository import Repository
from app.extensions import db
from app.models import Permission, Role, PermissionRole
from flask import request
from flask_sqlalchemy.query import Query
from flask_query_builder.querying import QueryBuilder, AllowedFilter, AllowedSort
from sqlalchemy import text

class PermissionRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        sorts = request.args.get('sort', '').split(',')
        joins = request.args.get('join', '').split(',')

        query = Permission.query

        query = QueryBuilder(Permission, query=query)\
            .allowed_filters([
                AllowedFilter.partial('name'),
            ]
            )\
            .query
    
        if sorts is not None and len(sorts) > 0:
            if '-name' in sorts:
                query = query.order_by(Permission.name.desc())
            elif 'name' in sorts:
                query = query.order_by(Permission.name)
            if '-created_at' in sorts:
                query = query.order_by(Permission.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Permission.created_at)
        
        if 'roles' in joins:
            query = query.options(db.joinedload(Permission.roles))

        return query        
    
    def paginate(self) -> tuple[list[Permission], dict]: 
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        permissions = []
        for permission in pagination.items:
            permissions.append(permission)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (permissions, meta)

    def show (self, permission_id : str) -> tuple[Permission]:
        permission = self.query().filter(Permission.id == permission_id).first()
        return (permission, )