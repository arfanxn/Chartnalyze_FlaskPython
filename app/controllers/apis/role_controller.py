from app.enums.permission_enums import PermissionName
from app.middlewares import authenticated, authorized, api_key_verified, email_verified
from app.forms import QueryForm, AssignUserRoleForm
from app.resources import RoleResource  
from app.services import RoleService
from app.helpers.response_helpers import create_response_tuple
from flask import Blueprint, request
from http import HTTPStatus

role_service = RoleService()

role_bp = Blueprint('role', __name__)

@role_bp.route('/roles', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.ROLES_INDEX.value)
@email_verified
def index():
    form = QueryForm(request.args)
    form.try_validate()

    roles, = role_service.index(form=form)
    roles_json = RoleResource.collection(roles)

    return create_response_tuple(status=HTTPStatus.OK, message=f"Roles retrieved successfully", data={'roles': roles_json})

@role_bp.route('/roles/<string:role_id>', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.ROLES_SHOW.value)
@email_verified
def show(role_id: str):
    role, = role_service.show(role_id=role_id)
    role_json = RoleResource(role).to_json()
    return create_response_tuple(status=HTTPStatus.OK, message=f"Role retrieved successfully", data={'role': role_json})

@role_bp.route('/users/<string:user_id>/roles', methods=['PUT'])
@api_key_verified
@authenticated
@authorized(PermissionName.ROLES_UPDATE.value)
@email_verified
def assign_to_user(user_id: str):
    print('==============================')
    print('user_id', user_id)
    form = AssignUserRoleForm(data={user_id: user_id ,**request.form})
    form.user_id.data = user_id
    form.try_validate()

    role_service.assign_to_user(form=form)

    return create_response_tuple(status=HTTPStatus.OK, message=f"Role assigned to user successfully")
    