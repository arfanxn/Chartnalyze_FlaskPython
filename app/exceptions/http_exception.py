class HttpException(Exception): 
    def __init__(self, message, status, additionals = None):
        super().__init__(message)
        self.status = status
        self.additionals = additionals

