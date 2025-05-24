from app.policies.policy import Policy
from app.models import User, Notification

class NotificationPolicy(Policy):

    def __init__(self):
        super().__init__()

    def index(self, user: User):
        return user is not None

    def show(self, user: User, notification: Notification):
        return user.id == notification.notifiable_id or\
                user.role.id == notification.notifiable_id

    def toggle_read(self, user: User, notification: Notification):
        return self.show(user, notification)