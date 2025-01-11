"""
Account serializers
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AccountLogin(BaseModel):
    """
    Account login
    """
    created_at: Optional[datetime] = Field(
        default=None,
        description="(Optional) Created at"
    )
    app_name: str = Field(
        default="DEFAULT",
        description="(Optional) App name"
    )
    firebase_token: str = Field(
        ...,
        description="Firebase token",
        frozen=True
    )


class LoginResponse(BaseModel):
    """
    Login response
    """
    id: UUID = Field(..., description="ID")
    verified: bool = Field(default=False, description="Verified")
    first_login: bool = Field(default=False, description="First login")


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


class AccountUpdate(BaseModel):
    """
    Account update
    """
    display_name: str = Field(..., description="Display Name")
    email: str = Field(..., description="Email")
