from app.resources import Resource
from app.models import Activity
from sqlalchemy import inspect 

class CandlestickPredictionResource(Resource): 
    def __init__(self, entity: Activity):
        self.entity = entity

    def to_json(self):
        entity = self.entity

        data = {
            'class_id': entity.class_id,
            'class_name': entity.class_name,
            'confidence': entity.confidence,
            'bounding_box': entity.bounding_box
        }

        return data