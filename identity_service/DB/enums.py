from enum import Enum

class UserGender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class UserRole(Enum):
    SUBSCRIBER = "SUBSCRIBER"
    MODERATOR = "MODERATOR"
    TESTER = "TESTER"
    ADMIN = "ADMIN"


class AuthProvider(Enum):
    LOCAL = "LOCAL"
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"
    APPLE = "APPLE"