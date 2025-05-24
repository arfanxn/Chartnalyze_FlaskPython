from app.resources import Resource
from datetime import datetime

class WatchedAssetResource(Resource): 
    def __init__(self, model: object):
        self.model = model

    def to_json(self):
        doc = self.model

        data = {
            '_id': doc.get('_id'),
            'user_id': doc.get('user_id'),
            'key': doc.get('key'),
            'name': doc.get('name'),
            'symbol': doc.get('symbol'),
            'order': doc.get('order'),
            'image_url': doc.get('image_url'),
            'created_at': doc.get('created_at'),
            'updated_at': doc.get('updated_at') if doc.get('updated_at') else None,
        }
        
        return data