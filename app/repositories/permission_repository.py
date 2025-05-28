from app.repositories.repository import Repository
from app.extensions import db
from app.models import Permission
from flask import request
from flask_sqlalchemy.query import Query
from flask_query_builder.querying import QueryBuilder, AllowedFilter

class PermissionRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        joins = request.args.get('join', '').split(',')

        query = Permission.query

        if 'roles' in joins:
            query = query.options(db.joinedload(Permission.roles))

        query = QueryBuilder(Permission, query=query)\
            .allowed_filters([
                AllowedFilter.partial('name'),
            ]
            )\
            .allowed_sorts(['name', 'created_at'])\
            .query

        return query        
    
    def paginate(self) -> tuple[list[Permission], dict]: 
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        notifications = []
        for notification in pagination.items:
            notifications.append(notification)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (notifications, meta)

    def show (self, permission_id : str) -> tuple[Permission]:
        notification = self.query().filter(Permission.id == permission_id).first()
        return (notification, )