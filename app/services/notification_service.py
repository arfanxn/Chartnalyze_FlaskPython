from app.services import Service
from app.models import  Notification
from app.forms import QueryForm
from app.policies import NotificationPolicy
from app.extensions import db
from werkzeug.exceptions import NotFound, Forbidden
from flask import g
from datetime import datetime

notification_policy = NotificationPolicy()

class NotificationService(Service):

    def __init__(self):
        super().__init__()

    def paginate_by_self (self, form: QueryForm) -> tuple[list[Notification], dict]:
        query = Notification.query\
            .order_by(Notification.created_at.desc())\
            .filter(Notification.notifiable_id.in_([g.user.id, g.user.role.id]))
        
        if (form.keyword.data is not None):
            keyword = form.keyword.data
            query = query.filter(
                db.or_(
                    Notification.title.like(f'%{keyword}%'), 
                    Notification.message.like(f'%{keyword}%')
                )
            )

        pagination = query.paginate(
            page=form.page.data,
            per_page=form.per_page.data,
            error_out=False,
        )

        notifications = pagination.items

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        if len(notifications) == 0: 
            raise NotFound('Notifications not found')

        return (notifications, meta)
    
    def show(self, notification_id: str) -> tuple[Notification]:
        query = Notification.query
        query = query.filter(Notification.id == notification_id)
        notification = query.first()
        
        if notification is None:
            raise NotFound('Notification not found')
        
        if not notification_policy.show(user=g.user, notification=notification):
            raise Forbidden('You are not allowed to view this notification')

        return (notification, )

    def toggle_read(self, notification_id: str) -> tuple[Notification, bool]:
        query = Notification.query
        query = query.filter(Notification.id == notification_id)
        notification = query.first()

        if notification is None:
            raise NotFound('Notification not found')
        
        if not notification_policy.toggle_read(user=g.user, notification=notification):
            raise Forbidden('You are not allowed to mark this notification as read')
        
        notification.read_at = None if notification.read_at else datetime.now()
        
        db.session.commit()

        is_read = notification.read_at is not None

        return (notification, is_read)