from app.resources import Resource
from app.models import Comment, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class CommentResource(Resource): 
    def __init__(self, entity: Comment):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'user_id': entity.user_id,
            'commentable_id': entity.commentable_id,
            'commentable_type': entity.commentable_type,
            'parent_id': entity.parent_id if entity.parent_id else None,
            'body': entity.body,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        if hasattr(entity, 'like_count') and entity.like_count is not None:
            data['like_count'] = entity.like_count

        ins = inspect(entity)

        if 'user' not in ins.unloaded:
            from app.resources import UserResource
            data['user']  = UserResource(entity.user).to_json()

        if 'commentable_post' not in ins.unloaded:
            from app.resources import PostResource
            data['commentable'] = PostResource(entity.commentable).to_json()  if entity.commentable is not None else None
        
        if 'parent' not in ins.unloaded:
            data['parent']  = CommentResource(entity.parent).to_json() if entity.parent is not None else None

        if 'children' not in ins.unloaded:
            data['children']  = CommentResource.collection(entity.children)

        if 'likes' not in ins.unloaded:
            from app.resources import LikeResource
            data['likes']  = LikeResource.collection(entity.likes)

        return data