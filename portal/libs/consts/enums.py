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
    Notification = 111


class Rendition(Enum):
    """
    Rendition
    """
    ORIGINAL = "original"
    MAX_100x100 = "max-100x100"
    MAX_200x200 = "max-200x200"
    MAX_300x300 = "max-300x300"
    MAX_400x400 = "max-400x400"
    MAX_500x500 = "max-500x500"
    MAX_600x600 = "max-600x600"
    MAX_700x700 = "max-700x700"
    MAX_800x800 = "max-800x800"
    MAX_900x900 = "max-900x900"
    MAX_1000x1000 = "max-1000x1000"

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


class FeedbackStatus(IntEnum):
    """
    Feedback status
    """
    PENDING = 0
    REVIEW = 1
    DISCUSSION = 2
    ACCEPTED = 3
    DONE = 4
    REJECTED = 5
    ARCHIVED = 6

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]


class NotificationMethod(IntEnum):
    """
    Notification method
    """
    UNKNOWN = 0
    PUSH = 1
    EMAIL = 2
    SMS = 3

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]


class NotificationType(IntEnum):
    """
    Notification type
    """
    INDIVIDUAL = 0
    MULTIPLE = 1
    # SYSTEM = 2

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]


class NotificationStatus(IntEnum):
    """
    Notification status
    """
    PENDING = 0
    SENT = 1
    FAILED = 2

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]


class NotificationHistoryStatus(IntEnum):
    """
    Notification history status
    """
    PENDING = 0
    SUCCESS = 1
    FAILED = 2

    @classmethod
    def choices(cls):
        """

        :return:
        """
        return [(key.value, key.name.title()) for key in cls]
