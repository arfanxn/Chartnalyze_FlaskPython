from app.middlewares import api_key_verified, authenticated, authorized, email_verified
from app.services import DashboardService 
from app.helpers.response_helpers import create_response_tuple
from app.enums.permission_enums import PermissionName
from flask import Blueprint
from http import HTTPStatus

dashboard_service = DashboardService()

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.DASHBOARD_INDEX.value)
@email_verified
def dashboard():
    result, = dashboard_service.index()
    result_json = result.__dict__

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Dashboard data retrieved successfully',
        data={ **result_json }
    )
