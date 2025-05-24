class Resource: 
    def __init__(self, entity):
        self.entity = entity

    def __getattr__(self, attr):
        return getattr(self.entity, attr)

    def to_json(self):
        raise NotImplementedError

    @classmethod
    def collection(cls, entities):
        return [cls(entity).to_json() for entity in entities]