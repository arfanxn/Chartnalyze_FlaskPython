from app.policies.policy import Policy
from app.models import User, Save
from app.enums.save_enums import SaveableType   

class SavePolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, like: Save):
        return user is not None
    