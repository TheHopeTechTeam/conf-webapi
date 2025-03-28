"""
FCM Device serializers
"""
from pydantic import BaseModel, Field


class FCMCreate(BaseModel):
    """
    FCM Create
    """
    data: dict = Field(..., description="")
