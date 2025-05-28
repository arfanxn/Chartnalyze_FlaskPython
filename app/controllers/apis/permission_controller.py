from app.middlewares import api_key_verified
from app.services import PermissionService
from app.helpers.response_helpers import create_response_tuple
from app.enums.permission_enums import PermissionName
from app.middlewares import authenticated, authorized, api_key_verified, email_verified
from app.resources import PermissionResource
from flask import Blueprint
from http import HTTPStatus

permission_service = PermissionService()

permission_bp = Blueprint('permission', __name__)

@permission_bp.route('/permissions', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.PERMISSIONS_INDEX.value)
@email_verified
def index():    
    permissions, meta = permission_service.paginate()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Permissions paginated successfully',
        data={ 'permissions' : PermissionResource.collection(permissions), **meta }
    )

@permission_bp.route('/permissions/<string:permission_id>', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.PERMISSIONS_SHOW.value)
@email_verified
def show(permission_id: str):
    permission, = permission_service.show(permission_id=permission_id)
    permission_json = PermissionResource(permission).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Permission found successfully',
        data={'permission': permission_json}
    )
