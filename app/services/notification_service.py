from app.repositories import NotificationRepository
from app.services import Service
from app.models import  Notification
from app.policies import NotificationPolicy
from app.extensions import db
from werkzeug.exceptions import NotFound, Forbidden
from flask import g

notification_repository = NotificationRepository()
notification_policy = NotificationPolicy()

class NotificationService(Service):

    def __init__(self):
        super().__init__()

    def paginate (self, notifiable_ids: list[str]|None = None) -> tuple[list[Notification], dict]:
        notifications, meta = notification_repository.paginate(notifiable_ids=notifiable_ids)
        return (notifications, meta)
    
    def show(self, notification_id: str) -> tuple[Notification]:
        notification, = notification_repository.show(notification_id=notification_id)
        
        if notification is None:
            raise NotFound('Notification not found')
        
        if not notification_policy.show(user=g.user, notification=notification):
            raise Forbidden('You are not allowed to view this notification')

        return (notification, )

    def toggle_read(self, notification_id: str) -> tuple[Notification, bool]:
        notification, = notification_repository.show(notification_id=notification_id)

        if notification is None:
            raise NotFound('Notification not found')
        
        if not notification_policy.toggle_read(user=g.user, notification=notification):
            raise Forbidden('You are not allowed to mark this notification as read')
        
        is_read, = notification_repository.toggle_read(notification=notification)
        
        db.session.commit()

        return (notification, is_read)