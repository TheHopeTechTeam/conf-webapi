"""
Account serializers
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    """
    Account
    """
    id: UUID = Field(..., description="ID")
    google_uid: str = Field(..., description="Google UID")
    phone_number: str = Field(..., description="Phone Number")
    email: str = Field(..., description="Email")
    display_name: str = Field(..., description="Display Name")


class AccountDetail(AccountBase):
    """
    Account detail
    """
    ticket_number: str = Field(..., description="Ticket Number")
    ticket_type: str = Field(..., description="Ticket Type")
    belong_church: str = Field(..., description="Belong Church")
    identity: str = Field(..., description="Identity")
