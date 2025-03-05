"""
Enums for the application
"""
from enum import Enum, IntEnum


class MenuOrder(IntEnum):
    """
    Menu order
    """
    Account = 100
    Language = 101
    Conference = 102
    EventInfo = 103
    Location = 104
    Instructor = 105
    Workshop = 106
    Ticket = 107
    FAQ = 108
    Testimony = 109
    Feedback = 110


class LoginMethod(Enum):
    """
    Login method
    """
    # PASSWORD = "password"
    # GOOGLE = "google"
    # FACEBOOK = "facebook"
    # APPLE = "apple"
    FIREBASE = "firebase"

class Provider(Enum):
    """
    Provider
    """
    FIREBASE = "firebase"

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]



class Gender(IntEnum):
    """
    Gender
    """
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2
    OTHER = 3

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]
