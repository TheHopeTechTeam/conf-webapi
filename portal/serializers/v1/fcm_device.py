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
    data: Optional[dict] = Field(default=None, description="")
