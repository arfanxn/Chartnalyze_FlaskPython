from app.resources import Resource

class PriceHistoryResource(Resource): 
    def __init__(self, entity: object):
        self.entity = entity

    def to_json(self):
        doc = self.entity

        data = {
            'id': doc.get('_id').__str__(),
            'symbol': doc.get('symbol'),
            'price_usd': doc.get('price_usd'),
            'scraped_at': doc.get('scraped_at'),
            'created_at': doc.get('created_at'),
        }
        
        if doc.get('updated_at') is not None:
            data['updated_at'] = doc.get('updated_at')

        return data