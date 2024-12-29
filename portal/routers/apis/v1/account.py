"""
Account API Router
"""
import uuid
import random
from typing import Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Response, Depends
from fastapi.params import Header
from starlette import status

from portal.containers import Container
from portal.libs.depends import (
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from portal.route_classes import LogRoute
from portal.serializers.base import HeaderInfo
from portal.serializers.v1.account import AccountBase, AccountDetail
from dateutil import parser



router = APIRouter(
    dependencies=[
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.get(
    path="/account/{account_id}",
    response_model=AccountDetail,
    status_code=status.HTTP_200_OK
)
@inject
async def get_account(
    request: Request,
    response: Response,
    headers: Annotated[HeaderInfo, Header()],
    account_id: uuid.UUID,
) -> dict:
    """
    Get an account
    """
    response.headers["Content-Language"] = headers.accept_language
    ticket_numbers = [str(f"TH{random.randint(100000, 999999)}") for _ in range(3)]
    ticket_types = ["REGULAR", "CREATIVE", "ALL ACCESS", "LEADERSHIP"]
    return AccountDetail(
        id=account_id,
        google_uid="google_uid",
        phone_number="phone_number",
        email="email",
        display_name="Dummy",
        ticket_number=random.choice(ticket_numbers),
        ticket_type=random.choice(ticket_types),
        belong_church="The Hope",
        identity="會眾",
    )
