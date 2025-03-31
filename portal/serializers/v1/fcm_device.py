"""
FCM Device serializers
"""
from typing import Optional

from pydantic import BaseModel, Field


class FCMCreate(BaseModel):
    """
    FCM Create
    """
    fcm_token: str = Field(..., description="FCM Token")
    additional_data: Optional[dict] = Field(
        default=None,
        description="Additional data to be sent to the device",
    )
