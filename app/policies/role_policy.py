from app.policies.policy import Policy
from app.models import User, Role
from app.enums.permission_enums import PermissionName
from app.enums.role_enums import RoleName
from werkzeug.exceptions import NotFound, Forbidden

class RolePolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, comment: Role):
        return user is not None
    
    def assign_to_user(self, assigner: User, user: User, role: Role):
        return user is not None
    
    def request_analyst(self, user: User):
        return user is not None