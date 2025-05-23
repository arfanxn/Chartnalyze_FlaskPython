from app.services import Service
from app.helpers.mail_helpers import send_mail
from app.models import Role, User, Permission
from app.forms import QueryForm, AssignUserRoleForm
from app.extensions import db
from app.exceptions import HttpException, ValidationException
from http import HTTPStatus

class RoleService(Service):

    def __init__(self):
        super().__init__()

    def index(self, form: QueryForm) -> tuple[list[Role]]:
        query = Role.query
        if form.joins.data is not None: 
            if 'permissions' in form.joins.data:
                query = query.options(db.joinedload(Role.permissions))
        query = query.order_by(Role.name.asc())
        if (form.keyword.data is not None):
            query = query.options().filter(db.or_(Role.name.like(f'%{form.keyword.data}%'), ))
        roles = query.all()
        if len(roles) == 0: 
            raise HttpException(message='Roles not found', status=HTTPStatus.NOT_FOUND)
        return (roles, )
    
    def show(self, role_id: str) -> tuple[Role]:
        role = Role.query.options(db.joinedload(Role.permissions)).filter_by(id=role_id).first()
        if role is None:
            raise HttpException(message='Role not found', status=HTTPStatus.NOT_FOUND)
        return (role, )
    
    def assign_to_user (self, form: AssignUserRoleForm) -> tuple[Role, User]: 
        user_id = form.user_id.data
        role_id = form.role_id.data

        user = User.query.options(db.joinedload(User.roles))\
            .filter(
                db.and_(User.id == user_id)
            ).first()
        
        if user is None:
            raise HttpException(message='User not found', status=HTTPStatus.NOT_FOUND)
        
        role = Role.query.filter(Role.id == role_id).first()

        if role is None:
            raise HttpException(message='Role not found', status=HTTPStatus.NOT_FOUND)

        if any(r.id == role.id for r in user.roles):
            raise ValidationException(message='User already has this role', errors={'role_id': ['User already has this role']})
        
        user.roles = [role]
        db.session.commit()

        return role, user
        