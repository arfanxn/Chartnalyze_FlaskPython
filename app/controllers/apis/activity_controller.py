from app.enums.activity_enums import CauserType, SubjectType, Type
from app.enums.permission_enums import PermissionName
from app.services import ActivityService
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, authorized, api_key_verified, email_verified
from app.resources import ActivityResource
from flask import Blueprint, request, g
from http import HTTPStatus

activity_service = ActivityService()

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/activities', methods=['GET'])
@api_key_verified
@authenticated
@authorized(PermissionName.ACTIVITIES_INDEX.value)
@email_verified
def index():
    activities, meta = activity_service.paginate()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Activities paginated successfully',
        data={'activities': ActivityResource.collection(activities), **meta}
    )

@activity_bp.route('/users/<string:user_id>/activities', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_causer_user_self(user_id: str):
    activities, meta = activity_service.paginate(causer_id=user_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Activities paginated successfully',
        data={'activities': ActivityResource.collection(activities), **meta}
    )

@activity_bp.route('/activities/<string:activity_id>', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def show(activity_id: str):
    activity, = activity_service.show(activity_id=activity_id)
    activity_json = ActivityResource(activity).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Activity found successfully',
        data={'activity': activity_json}
    )
