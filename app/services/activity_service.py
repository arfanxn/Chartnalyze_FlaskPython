from app.policies import ActivityPolicy
from app.repositories import ActivityRepository
from app.services import Service
from app.models import Activity
from flask import g 
from werkzeug.exceptions import NotFound, Forbidden

activity_policy = ActivityPolicy()
activity_repository = ActivityRepository()

class ActivityService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (
        self, 
        user_id: str|None = None,
        subject_id: str|None = None, 
    ) -> tuple[list[Activity], dict]:
        activities, meta = activity_repository.paginate(
            user_id=user_id,
            subject_id=subject_id,
        )
        return (activities, meta)
    
    def show(self, activity_id: str) -> tuple[Activity]:
        activity, = activity_repository.show(activity_id=activity_id)
        if activity is None:
            raise NotFound('Activity not found')
        activity_policy.show(user=g.user, activity=activity)
        return (activity, )