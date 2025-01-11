"""
Location serializers
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from portal.schemas.mixins import UUIDBaseModel


class LocationBase(UUIDBaseModel):
    name: str = Field(..., title="Location name")
    address: Optional[str] = Field(None, title="Location address")
    floor: Optional[str] = Field(None, title="Location floor")
    room_number: Optional[str] = Field(None, title="Location room number")
    image_url: Optional[str] = Field(None, title="Location image URL")
