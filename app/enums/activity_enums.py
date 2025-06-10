from enum import Enum

class CauserType(Enum):
    USER = 'user'

class SubjectType(Enum):
    USER = 'user'

class Type(Enum): 
    REGISTER = 'register'
    VERIFY_EMAIL = 'verify_email'
    LOGIN = 'login'
    LOGOUT = 'logout'