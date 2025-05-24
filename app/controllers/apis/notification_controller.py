from app.middlewares import api_key_verified, authenticated, authorized, email_verified
from app.resources import NotificationResource
from app.services import NotificationService 
from app.forms import QueryForm
from app.helpers.response_helpers import create_response_tuple
from flask import Blueprint, request, g
from http import HTTPStatus

notification_service = NotificationService()

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/users/self/notifications', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index():
    form = QueryForm(request.args)
    form.try_validate()

    notifications, meta = notification_service.paginate_by_self(form=form)
    notifications_json = NotificationResource.collection(notifications)
    notifications_pagination = {'notifications': notifications_json, **meta}

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Notifications paginated successfully',
        data={ **notifications_pagination }
    )

@notification_bp.route('/users/self/notifications/<string:notification_id>', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def self_show (notification_id: str):
    notification, = notification_service.show(notification_id=notification_id)
    notification_json = NotificationResource(notification).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Notification found successfully',
        data={'notification': notification_json}
    )

@notification_bp.route('/users/self/notifications/<string:notification_id>/toggle-read', methods=['PATCH'])
@api_key_verified
@authenticated
@email_verified
def self_toggle_read (notification_id: str):
    notification, is_read = notification_service.toggle_read(notification_id=notification_id)
    notification_json = NotificationResource(notification).to_json()

    message = 'Notification marked as read' if is_read else 'Notification marked as unread'

    return create_response_tuple(
        status=HTTPStatus.OK,
        message=message,
        data={'notification': notification_json} 
    )