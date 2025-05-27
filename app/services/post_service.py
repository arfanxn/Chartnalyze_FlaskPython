from app.repositories import PostRepository
from app.services import Service
from app.forms import SavePostForm
from app.models import Post, Media
from app.config import Config
from app.extensions import db
from app.helpers.file_helpers import get_file_extension, get_file_size   
from app.enums.media_enums import ModelType
from flask import g 
from werkzeug.exceptions import InternalServerError
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound
import ulid
import os

post_repository = PostRepository()

class PostService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (self) -> tuple[list[Post], dict]:
        posts, meta = post_repository.paginate()
        return (posts, meta)
    
    def paginate_by_user (self, user_id: str) -> tuple[list[Post], dict]: 
        posts, meta = post_repository.paginate(user_id=user_id)
        return (posts, meta)
    
    def show(self, post_id: str) -> tuple[Post]:
        post, = post_repository.show(post_id=post_id)
        if post is None:
            raise NotFound('Post not found')
        return (post, )
    
    def store(self, form: SavePostForm, images: list[FileStorage]|None = None) -> tuple[Post]:
        try: 
            user_id = g.user.id

            post, = post_repository.store(form=form, user_id=user_id)

            medias = []
            if images is not None:
                for image in images:
                    image_file_name = ulid.new().str + get_file_extension(file=image)

                    media = Media()
                    media.model_id = post.id
                    media.model_type = ModelType.POST.value
                    media.collection_name = 'post_images'
                    media.name = image.filename
                    media.file_name = image_file_name 
                    media.mime_type = image.mimetype
                    media.size = get_file_size(file=image)

                    image.save(os.path.join(Config.UPLOAD_FOLDER, 'images/posts', image_file_name))

                    medias.append(media)

            db.session.bulk_save_objects(medias)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InternalServerError('Post creation failed')

        return (post, )
    
    def update(self, form: SavePostForm, post_id: str) -> tuple[Post]:
        post, = post_repository.update(form=form, post_id=post_id)
        db.session.commit()
        return (post, )
    
    def destroy (self, post_id: str) -> tuple[bool]:
        post_repository.destroy(post_id=post_id)
        db.session.commit()
        return (True, )