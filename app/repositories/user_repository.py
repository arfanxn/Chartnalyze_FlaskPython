from app.models.user import User

class UserRepository:
    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)