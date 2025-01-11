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
    Location = 103
    Instructor = 104
    Workshop = 105
    Ticket = 106
