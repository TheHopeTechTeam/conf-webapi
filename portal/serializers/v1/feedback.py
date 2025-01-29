"""
Feedback serializers
"""
from pydantic import BaseModel, Field

from portal.schemas.mixins import UUIDBaseModel


class FeedbackCreate(BaseModel):
    """
    FeedbackCreate
    """
    name: str = Field(..., description="Name of the feedback")
    # email: Optional[str] = Field(None, description="Email of the feedback")
    message: str = Field(
        ...,
        description="Message of the feedback",
        max_length=200
    )


class FeedbackCreateResponse(UUIDBaseModel):
    """
    FeedbackCreateResponse
    """
