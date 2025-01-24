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
    name: str = Field(..., description="Name")
    bio: str = Field(..., description="Bio")
    image_url: Optional[str] = Field(None, serialization_alias="imageUrl", description="Image URL")
