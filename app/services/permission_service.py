from app.services import Service
from app.forms import QueryForm
from app.models import Permission
from app.extensions import db
from werkzeug.exceptions import NotFound
from http import HTTPStatus

class PermissionService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (self, form: QueryForm) -> tuple[list[Permission], dict]:
        query = Permission.query
        if form.joins.data is not None: 
            if 'roles' in form.joins.data:
                query = query.options(db.joinedload(Permission.roles))
        query = query.order_by(Permission.name.asc())
        if (form.keyword.data is not None):
            query = query.filter(
                db.or_(Permission.name.like(f'%{form.keyword.data}%'), )    
            )

        pagination = query.paginate(
            page=form.page.data,
            per_page=form.per_page.data,
            error_out=False,
        )

        permissions = pagination.items

        if len(permissions) == 0: 
            raise NotFound('Permissions not found')

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (permissions, meta)
    
    def show(self, permission_id: str) -> tuple[Permission]:
        permission = Permission.query\
            .options(db.joinedload(Permission.roles))\
            .filter_by(id=permission_id).first()
        if permission is None:
            raise NotFound('Permission not found')
        return (permission, )