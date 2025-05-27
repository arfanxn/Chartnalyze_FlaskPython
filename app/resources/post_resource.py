from app.resources import Resource
from app.models import Post, User
from sqlalchemy import inspect  # Add this import
from app.config import Config

class PostResource(Resource): 
    def __init__(self, entity: Post):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'id': entity.id,
            'user_id': entity.user_id,
            'title': entity.title if entity.title is not None else None,
            'slug': entity.slug,
            'body': entity.body,
            'created_at': entity.created_at.isoformat(),
            'updated_at': entity.updated_at.isoformat() if entity.updated_at is not None else None,
        }

        if hasattr(entity, 'comment_count') and entity.comment_count is not None:
            data['comment_count'] = entity.comment_count
    
        if hasattr(entity, 'like_count') and entity.like_count is not None:
            data['like_count'] = entity.like_count

        ins = inspect(entity)

        if 'user' not in ins.unloaded:
            from app.resources import UserResource
            data['user']  = UserResource(entity.user).to_json()
        
        if 'comments' not in ins.unloaded:
            from app.resources import CommentResource
            data['comments']  = CommentResource.collection(entity.comments) 

        if 'likes' not in ins.unloaded:
            from app.resources import LikeResource
            data['likes']  = LikeResource.collection(entity.likes)

        if 'images' not in ins.unloaded:
            images = entity.images    
            data['image_urls']  = []
            for image in images:
                data['image_urls'].append(f"{Config.APP_URL}/public/images/posts/{image.file_name}")

        return data