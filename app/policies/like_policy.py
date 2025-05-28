from app.policies.policy import Policy
from app.models import User, Like

class LikePolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, like: Like):
        return user is not None
    
    def store(self, user: User):
        return user is not None
    
    def destroy(self, user: User, like: Like):
        return user.id == like.user_id