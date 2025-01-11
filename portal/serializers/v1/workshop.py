"""
Workshop serializers
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from portal.serializers.v1.instructor import InstructorBase
from portal.serializers.v1.location import LocationBase


class WorkshopBase(BaseModel):
    """
    Workshop
    """
    id: UUID = Field(..., description="ID")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    location: LocationBase = Field(..., description="Location")
    start_datetime: datetime = Field(..., description="Start Date and Time")
    end_datetime: datetime = Field(..., description="End Date and Time")


class WorkshopDetail(WorkshopBase):
    """
    Workshop detail
    """
    # conference: str = Field(..., description="Conference")
    instructor: InstructorBase = Field(..., description="Instructor")
    participants_limit: int = Field(..., description="Participants Limit")
    is_full: bool = Field(..., description="The number of participants has reached the upper limit")



class WorkshopList(BaseModel):
    """
    Workshop list
    """
    workshops: list[WorkshopBase] = Field(..., description="Workshops")
