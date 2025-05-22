from app.resources import Resource
from app.models import Media
from app.config import Config

class MediaResource(Resource): 
    def __init__(self, model: Media):
        self.model = model

    def to_json(self):
        data = {
            'id': self.id,
            'model_id': self.model_id,
            'model_type': self.model_type,
            'collection_name': self.collection_name,
            'name': self.name,
            'file_name': self.file_name,
            'mime_type': self.mime_type,
            'disk': self.disk,
            'size': self.size,
            'data': self.data,
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

        return data