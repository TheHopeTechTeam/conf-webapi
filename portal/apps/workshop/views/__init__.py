"""
Top-level package for views.
"""
from .workshop import WorkshopModelAdmin
from .workshop_registration import WorkshopRegistrationModelAdmin
from .workshop_time_slot import WorkshopTimeSlotModelAdmin


__all__ = [
    "WorkshopModelAdmin",
    "WorkshopRegistrationModelAdmin",
    "WorkshopTimeSlotModelAdmin",
]
