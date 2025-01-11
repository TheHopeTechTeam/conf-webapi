"""
Instructor serializers
"""
from typing import Optional

from pydantic import Field

from portal.schemas.mixins import UUIDBaseModel


class InstructorBase(UUIDBaseModel):
    """
    Instructor base model
    """
    name: str = Field(..., title="Name")
    bio: str = Field(..., title="Bio")
    image_url: Optional[str] = Field(None, title="Image URL")
