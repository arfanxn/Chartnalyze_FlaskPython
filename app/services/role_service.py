from app.services import Service
from app.enums.role_enums import RoleName
from app.enums.notification_enums import NotifiableType, Type as NotificationType
from app.models import Role, User, Notification
from app.forms import QueryForm, AssignUserRoleForm
from app.extensions import db
from werkzeug.exceptions import NotFound, Forbidden, Conflict, UnprocessableEntity
from datetime import datetime, timedelta

class RoleService(Service):

    def __init__(self):
        super().__init__()

    def all(self, form: QueryForm) -> tuple[list[Role]]:
        query = Role.query
        if form.joins.data is not None: 
            if 'permissions' in form.joins.data:
                query = query.options(db.joinedload(Role.permissions))
        query = query.order_by(Role.name.asc())
        if (form.keyword.data is not None):
            query = query.options().filter(db.or_(Role.name.like(f'%{form.keyword.data}%'), ))
        roles = query.all()
        if len(roles) == 0: 
            raise NotFound('Roles not found')
        return (roles, )
    
    def show(self, role_identifier: str) -> tuple[Role]:
        role = Role.query\
            .options(db.joinedload(Role.permissions))\
            .filter(
                db.or_(Role.id == role_identifier, Role.name == role_identifier)
            ).first()
        if role is None:
            raise NotFound('Role not found')
        return (role, )
    
    def assign_to_user (self, form: AssignUserRoleForm) -> tuple[Role, User]: 
        user_id = form.user_id.data
        role_name = form.role_name.data

        user = User.query.options(db.joinedload(User.roles))\
            .filter(db.and_(User.id == user_id))\
            .first()
        
        if user is None:
            raise NotFound('User not found')
        elif user.role.name == RoleName.ADMIN.value:
            raise Forbidden('Cannot assign role to admin user')
        
        role = Role.query.filter(Role.name == role_name).first()

        if role is None:
            raise NotFound('Role not found')
        elif role.name == RoleName.ADMIN.value:
            raise UnprocessableEntity({'role_name': ['Cannot assign admin role to user']})
        elif any(r.id == role.id for r in user.roles):
            raise UnprocessableEntity({'role_name': ['User already has this role']})
        
        user.roles = [role]
        db.session.commit()

        return role, user
        
    def request_analyst(self, user_id: str) -> tuple[bool]:
        admin_role = Role.query.filter(Role.name == RoleName.ADMIN.value).first()

        user = User.query.filter(User.id == user_id).first()
        if user is None:
            raise NotFound('User not found')
        user_json = {'id': user.id, 'name': user.name,' email': user.email, 'username': user.username}

        does_exist = db.session.query(
            db.exists().where(
                db.and_(
                    Notification.notifiable_id == admin_role.id,
                    Notification.notifiable_type == NotifiableType.ROLE.value,
                    Notification.type == NotificationType.REQUEST_ANALYST.value,
                    Notification.created_at >= datetime.now() - timedelta(days=30)
                )
            )
        ).scalar()

        if does_exist:
            raise Conflict(
                # the error message should be descriptive enough for the user to understand
                # what they need to do to resolve the issue
                'You have already requested to be an analyst in the last 30 days',
            )
        
        notification = Notification(
            notifiable_id=admin_role.id,    
            notifiable_type=NotifiableType.ROLE.value,
            type=NotificationType.REQUEST_ANALYST.value,
            title='Request Analyst',
            message=f"{user.name} ({user.email}) has requested to be an analyst",
            data={'user': user_json },
        )
        db.session.add(notification)
        db.session.commit()

        return (True,)