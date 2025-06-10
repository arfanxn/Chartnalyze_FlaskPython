from app.policies.policy import Policy
from app.models import User, Activity
from app.enums.permission_enums import PermissionName

class ActivityPolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, activity: Activity):
        return user is not None