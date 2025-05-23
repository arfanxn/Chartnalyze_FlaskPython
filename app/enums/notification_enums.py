from enum import Enum

class Type(Enum):
    DEFAULT = 1
    REQUEST_ANALYST = 2

class NotifiableType(Enum):
    USER = 'user'
    ROLE = 'role'