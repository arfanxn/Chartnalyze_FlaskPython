from app.policies.policy import Policy
from app.models import User, Post
from app.enums.permission_enums import PermissionName

class PostPolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, post: Post):
        return user is not None
    
    def store(self, user: User):
        return user is not None

    def update(self, user: User, post: Post):
        return user.id == post.user_id
    
    def destroy(self, user: User, post: Post):
        return user.id == post.user_id or\
            user.has_permissions(PermissionName.POSTS_DESTROY.value)