from app.resources import Resource

class WatchedAssetResource(Resource): 
    def __init__(self, entity: object):
        self.entity = entity

    def to_json(self):
        doc = self.entity

        data = {
            'id': doc.get('_id').__str__(),
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