from app.policies.policy import Policy
from app.models import User, Like, Comment, Post
from app.enums.like_enums import LikeableType   
from werkzeug.exceptions import NotFound

class LikePolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, like: Like):
        return user is not None
    