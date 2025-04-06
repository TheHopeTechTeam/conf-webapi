"""
FCM Device serializers
"""
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class FCMCreate(BaseModel):
    """
    FCM Create
    """
    fcm_token: str = Field(..., description="FCM Token")
    additional_data: Optional[dict] = Field(
        default=None,
        description="Additional data to be sent to the device",
    )

    @field_validator("fcm_token")
    def validate_fcm_token(cls, value: str) -> str:
        """
        Validate FCM token
        :param value:
        :return:
        """
        if not value:
            raise ValueError("FCM token is required")
        return value
