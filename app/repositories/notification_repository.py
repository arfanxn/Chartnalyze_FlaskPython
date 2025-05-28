from app.repositories.repository import Repository
from app.extensions import db
from app.models import Notification
from flask import request
from flask_sqlalchemy.query import Query
from flask_query_builder.querying import QueryBuilder, AllowedFilter
from datetime import datetime

class NotificationRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        filter = request.args.get('filter', None)
        query = Notification.query

        if filter is not None:
            query = query.filter(db.or_(
                    Notification.title.contains(filter),
                    Notification.message.contains(filter)
                ))

        query = QueryBuilder(Notification, query=query)\
            .allowed_filters([
                AllowedFilter.partial('title'),
                AllowedFilter.partial('message')
            ]
            )\
            .allowed_sorts(['created_at'])\
            .query

        return query        
    
    def paginate(self, notifiable_ids: list[str]|None = None) -> tuple[list[Notification], dict]: 
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        if notifiable_ids is not None:
            query = query.filter(Notification.notifiable_id.in_(notifiable_ids))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        notifications = []
        for notification in pagination.items:
            notifications.append(notification)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (notifications, meta)

    def show (self, notification_id : str) -> tuple[Notification]:
        notification = self.query().filter(Notification.id == notification_id).first()
        return (notification,)
        
    def toggle_read(self, notification: Notification) -> tuple[bool]:
        notification.read_at = None if notification.read_at else datetime.now()
        is_read = notification.read_at is not None
        return (is_read, )