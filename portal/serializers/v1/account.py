"""
Account serializers
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from portal.schemas.mixins import UUIDBaseModel


class AccountLogin(BaseModel):
    """
    Account login
    """
    created_at: Optional[datetime] = Field(
        default=None,
        serialization_alias="createdAt",
        description="(Optional) Created at"
    )
    app_name: str = Field(
        default="DEFAULT",
        serialization_alias="appName",
        description="(Optional) App name"
    )
    firebase_token: str = Field(
        ...,
        serialization_alias="firebaseToken",
        description="Firebase token",
        frozen=True
    )


class LoginResponse(UUIDBaseModel):
    """
    Login response
    """
    verified: bool = Field(
        default=False,
        description="Verified"
    )
    first_login: bool = Field(
        default=False,
        serialization_alias="firstLogin",
        description="First login"
    )


class AccountBase(UUIDBaseModel):
    """
    Account
    """
    google_uid: str = Field(..., serialization_alias="googleUid", description="Google UID")
    phone_number: str = Field(..., serialization_alias="phoneNumber", description="Phone Number")
    email: str = Field(..., description="Email")
    display_name: str = Field(..., serialization_alias="displayName", description="Display Name")


class AccountDetail(AccountBase):
    """
    Account detail
    """
    ticket_number: str = Field(..., serialization_alias="ticketNumber", description="Ticket Number")
    ticket_type: str = Field(..., serialization_alias="ticketType", description="Ticket Type")
    belong_church: str = Field(..., serialization_alias="belongChurch", description="Belong Church")
    identity: str = Field(..., description="Identity")


class AccountUpdate(BaseModel):
    """
    Account update
    """
    display_name: str = Field(..., serialization_alias="displayName", description="Display Name")
    email: str = Field(..., description="Email")
