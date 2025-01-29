"""
Enums for the application
"""
from enum import IntEnum


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
