from app.enums.permission_enums import PermissionName
from app.middlewares import authenticated, authorized, api_key_verified, email_verified
from app.forms import AssignUserRoleForm
from app.resources import RoleResource  
from app.services import RoleService
from app.helpers.response_helpers import create_response_tuple
from flask import Blueprint, request, g
from http import HTTPStatus

role_service = RoleService()

role_bp = Blueprint('role', __name__)

@role_bp.route('/roles', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.ROLES_INDEX.value)
@email_verified
def index():
    roles, meta = role_service.paginate()

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message=f"Roles paginated successfully",
        data={'roles': RoleResource.collection(roles), **meta}
    )

@role_bp.route('/roles/<string:role_identifier>', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.ROLES_SHOW.value)
@email_verified
def show(role_identifier: str):
    role, = role_service.show(role_identifier=role_identifier)
    return create_response_tuple(
        status=HTTPStatus.OK,
        message=f"Role retrieved successfully", 
        data={'role': RoleResource(role).to_json()}
    )

@role_bp.route('/users/<string:user_id>/roles', methods=['PUT'])
@api_key_verified
@authenticated
@authorized(PermissionName.ROLES_UPDATE.value)
@email_verified
def assign_to_user(user_id: str):
    form = AssignUserRoleForm(request.form)
    form.user_id.data = user_id
    form.try_validate()

    role_service.assign_to_user(form=form)

    return create_response_tuple(status=HTTPStatus.OK, message=f"Role assigned to user successfully")

@role_bp.route('/users/self/request-analyst', methods=['POST'])
@api_key_verified
@authenticated
@email_verified
def self_request_analyst():
    user_id = g.user.id 

    role_service.request_analyst(user_id=user_id)

    return create_response_tuple(status=HTTPStatus.OK, message=f"Analyst request sent successfully")