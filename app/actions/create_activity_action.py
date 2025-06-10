from app.actions.action import Action
from app.models import Activity, User
from app.extensions import db
from app.enums.activity_enums import CauserType, SubjectType, Type
from werkzeug.exceptions import InternalServerError
from datetime import datetime

class CreateActivityAction(Action):
    def __init__(self):
        super().__init__()

    def __call__(
            self, 
            causer: object,
            type: str,
            description: str,
            subject: object = None,
            properties: dict = None,
        ) -> tuple[Activity]:
        try:
            activity = Activity()

            activity.type = type
            activity.description = description
            activity.properties = properties

            if isinstance(causer, User):
                activity.causer_id = causer.id
                activity.causer_type = CauserType.USER.value
            elif hasattr(causer, 'id'):
                activity.causer_id = causer.id
                activity.causer_type = causer.__class__.__name__.lower()

            if hasattr(subject, 'id'):
                activity.subject_id = subject.id
                activity.subject_type = subject.__class__.__name__.lower()

            db.session.add(activity)
            db.session.commit()


        except Exception as e:
            db.session.rollback()
            raise InternalServerError(description='Something went wrong', original_exception=e)

        return (activity, )