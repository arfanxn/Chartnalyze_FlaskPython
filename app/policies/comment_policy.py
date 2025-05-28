from app.policies.policy import Policy
from app.models import User, Comment
from app.enums.permission_enums import PermissionName

class CommentPolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, comment: Comment):
        return user is not None
    
    def store(self, user: User):
        return user is not None
    
    def destroy(self, user: User, comment: Comment):
        return user.id == comment.user_id or user.has_permissions(PermissionName.COMMENTS_DESTROY.value)