"""
Event Info Serializer
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from portal.schemas.mixins import UUIDBaseModel


class EventScheduleBase(UUIDBaseModel):
    """
    Event Schedule Base
    """
    title: str = Field(..., description="Title")
    description: Optional[str] = Field(None, description="Description")
    start_time: datetime = Field(..., serialization_alias="startTime", description="Start Time")


class EventScheduleList(BaseModel):
    """
    Event Schedule List
    """
    schedules: list[EventScheduleBase] = Field(..., title="Schedules")

