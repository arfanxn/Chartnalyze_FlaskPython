from app.policies import SavePolicy
from app.repositories import SaveRepository
from app.services import Service
from app.models import Save, Comment, Post
from app.extensions import db
from app.enums.save_enums import SaveableType
from werkzeug.exceptions import NotFound

save_policy = SavePolicy()
save_repository = SaveRepository()

class SaveService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (self, user_id: str|None = None, saveable_id: str|None = None, saveable_type: str|None = None) -> tuple[list[Save], dict]:
        saves, meta = save_repository.paginate(user_id=user_id, saveable_id=saveable_id, saveable_type=saveable_type)
        return (saves, meta)
    
    def show(self, save_id: str) -> tuple[Save]:
        save, = save_repository.show(save_id=save_id)
        if save is None:
            raise NotFound('Save not found')
        return (save, )
    
    def toggle(self, user_id: str, saveable_id: str, saveable_type: str) -> tuple[bool]:
        if saveable_type is SaveableType.POST.value:
            saveable = Post.query.filter(Post.id == saveable_id).first()
            if saveable is None: 
                raise NotFound('Post not found')
        else:
            raise NotFound('Saveable not found')

        is_saved, = save_repository.toggle(
            user_id=user_id, 
            saveable_id=saveable_id, 
            saveable_type=saveable_type
        )
        db.session.commit()
        return (is_saved, )