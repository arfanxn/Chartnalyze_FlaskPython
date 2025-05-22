class Resource: 
    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        return getattr(self.data, attr)

    def to_json(self):
        raise NotImplementedError

    @classmethod
    def collection(cls, resources):
        return [cls(item).to_json() for item in resources]