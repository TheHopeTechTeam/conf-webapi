"""
Serializers for User model
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """
    User login
    """
    created_at: Optional[datetime] = Field(default=None, description="Created at")
    app_name: str = Field(default="DEFAULT", description="App name")


class LoginResponse(BaseModel):
    """
    Login response
    """
    id: UUID = Field(..., description="ID")
    verified: bool = Field(default=False, description="Verified")
    first_login: bool = Field(default=False, description="First login")
