"""
Account serializers
"""
from typing import Optional

from pydantic import BaseModel, Field

from portal.libs.consts.enums import LoginMethod
from portal.schemas.mixins import UUIDBaseModel


class AccountLogin(BaseModel):
    """
    Account login
    """
    login_method: LoginMethod = Field(
        default=LoginMethod.FIREBASE,
        serialization_alias="loginMethod",
        description="Login method"
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
    # google_uid: str = Field(..., serialization_alias="googleUid", description="Google UID")
    phone_number: str = Field(..., serialization_alias="phoneNumber", description="Phone Number")
    email: Optional[str] = Field(default=None, description="Email")
    display_name: Optional[str] = Field(default=None, serialization_alias="displayName", description="Display Name")


class AccountDetail(AccountBase):
    """
    Account detail
    """
    ticket_number: Optional[str] = Field(default=None, serialization_alias="ticketNumber", description="Ticket Number")
    ticket_type: Optional[str] = Field(default=None, serialization_alias="ticketType", description="Ticket Type")
    belong_church: Optional[str] = Field(default=None, serialization_alias="belongChurch", description="Belong Church")
    identity: Optional[str] = Field(default=None, description="Identity")


class AccountUpdate(BaseModel):
    """
    Account update
    """
    display_name: str = Field(..., serialization_alias="displayName", description="Display Name")
    email: str = Field(..., description="Email")
