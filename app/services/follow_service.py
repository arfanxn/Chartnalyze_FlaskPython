from app.repositories import FollowRepository
from app.services import Service
from app.models import Follow, User
from app.extensions import db
from werkzeug.exceptions import NotFound, BadRequest

follow_repository = FollowRepository()

class FollowService(Service):

    def __init__(self):
        super().__init__()

    def paginate_followers_of (self, followed_id: str) -> tuple[list[Follow], dict]: 
        return follow_repository.paginate_followers_of(followed_id=followed_id)

    def paginate_followeds_of (self, follower_id: str) -> tuple[list[Follow], dict]: 
        return follow_repository.paginate_followeds_of(follower_id=follower_id)
    
    def toggle_follow(self, follower_id: str, followed_id: str) -> tuple[bool]:
        if follower_id == followed_id:
            raise BadRequest('You cannot follow yourself')
        
        if User.query.filter(
            db.or_(User.id == follower_id,User.id == followed_id)
        ).count() != 2:
            raise NotFound('User not found')

        is_following, = follow_repository.toggle_follow(follower_id=follower_id, followed_id=followed_id)
        db.session.commit() 

        return (is_following, )
