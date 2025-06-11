from flask import g, request
from app.actions.action import Action
from app.models import Activity, User
from app.extensions import db
from werkzeug.exceptions import InternalServerError
from datetime import datetime

class CreateActivityAction(Action):
    def __init__(self):
        super().__init__()

    def __call__(
            self, 
            user: User,
            type: str,
            description: str,
            subject: object = None,
            properties: dict = None,
        ) -> tuple[Activity]:
        try:
            activity = Activity()

            activity.user_id = user.id
            activity.user_ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            activity.user_agent = request.headers.get('User-Agent')

            activity.type = type
            activity.description = description
            if properties is not None:
                activity.properties = properties
            if subject is not None:
                if hasattr(subject, 'id'):
                    activity.subject_id = subject.id
                    activity.subject_type = subject.__class__.__name__.lower()

            db.session.add(activity)
            db.session.commit()


        except Exception as e:
            db.session.rollback()
            raise InternalServerError(description='Something went wrong', original_exception=e)

        return (activity, )