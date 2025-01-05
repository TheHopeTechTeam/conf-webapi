"""
Instructor serializers
"""
from pydantic import BaseModel, Field


class InstructorBase(BaseModel):
    """
    Instructor base model
    """
    name: str = Field(..., title="Name")
    bio: str = Field(..., title="Bio")
    image_url: str = Field(..., title="Image URL")
