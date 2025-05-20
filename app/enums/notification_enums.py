from enum import Enum

class Type(Enum):
    DEFAULT = 1

class NotifiableType(Enum):
    USER = 'user'
    ROLE = 'role'