from app.repositories.repository import Repository
from app.models import Media

class MediaRepository(Repository):

    def __init__(self):
        super().__init__()

    def first_by_model_id_and_model_type_and_collection_name_or_new\
        (self, model_id: str, model_type: str, collection_name: str) -> (Media | None):
        media = Media.query.filter(
            Media.model_id == model_id,
            Media.model_type == model_type,
            Media.collection_name == collection_name
        ).first()

        if media is None:
            media = Media()
            media.model_id = model_id
            media.model_type = model_type
            media.collection_name = collection_name
            
        return media