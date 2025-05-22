class Resource: 
    def __init__(self, model):
        self.model = model

    def __getattr__(self, attr):
        return getattr(self.model, attr)

    def to_json(self):
        raise NotImplementedError

    @classmethod
    def collection(cls, models):
        return [cls(model).to_json() for model in models]