from app.policies import LikePolicy
from app.repositories import LikeRepository
from app.services import Service
from app.models import Like, Comment, Post
from app.extensions import db
from app.enums.like_enums import LikeableType
from werkzeug.exceptions import NotFound

like_policy = LikePolicy()
like_repository = LikeRepository()

class LikeService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (self, user_id: str|None = None, likeable_id: str|None = None, likeable_type: str|None = None) -> tuple[list[Like], dict]:
        likes, meta = like_repository.paginate(user_id=user_id, likeable_id=likeable_id, likeable_type=likeable_type)
        return (likes, meta)
    
    def show(self, like_id: str) -> tuple[Like]:
        like, = like_repository.show(like_id=like_id)
        if like is None:
            raise NotFound('Like not found')
        return (like, )
    
    def toggle(self, user_id: str, likeable_id: str, likeable_type: str) -> tuple[bool]:
        if likeable_type is LikeableType.COMMENT.value:
            likeable = Comment.query.filter(Comment.id == likeable_id).first()
            if likeable is None: 
                raise NotFound('Comment not found')
        elif likeable_type is LikeableType.POST.value:
            likeable = Post.query.filter(Post.id == likeable_id).first()
            if likeable is None: 
                raise NotFound('Post not found')
        else:
            raise NotFound('Likeable not found')

        is_liked, = like_repository.toggle(
            user_id=user_id, 
            likeable_id=likeable_id, 
            likeable_type=likeable_type
        )
        db.session.commit()
        return (is_liked, )