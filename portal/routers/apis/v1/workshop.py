"""
Workshop API Router
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
from portal.serializers.v1.workshop import WorkshopBase, WorkshopDetail, WorkshopList
from dateutil import parser

router = APIRouter(
    dependencies=[
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)

fri_first_st = parser.parse("2025-05-02T14:00:00+08:00")
fri_first_et = parser.parse("2025-05-02T15:20:00+08:00")
fri_second_st = parser.parse("2025-05-02T15:00:00+08:00")
fri_second_et = parser.parse("2025-05-02T16:20:00+08:00")
sat_first_st = parser.parse("2025-05-03T14:00:00+08:00")
sat_first_et = parser.parse("2025-05-03T15:20:00+08:00")
sat_second_st = parser.parse("2025-05-03T15:00:00+08:00")
sat_second_et = parser.parse("2025-05-03T16:20:00+08:00")


@router.get(
    path="/workshop/list",
    response_model=WorkshopList,
    status_code=status.HTTP_200_OK
)
@inject
async def get_workshop_list(
    request: Request,
    response: Response,
    headers: Annotated[HeaderInfo, Header()],
) -> dict:
    """

    :param request:
    :param response:
    :param headers:
    :return:
    """
    response.headers["Content-Language"] = headers.accept_language
    return WorkshopList(
        workshops=[
            WorkshopBase(
                id=uuid.uuid4(),
                title="Workshop 1",
                description="Workshop 1 description",
                location="2F 201 Room",
                start_datetime=fri_first_st,
                end_datetime=fri_first_et
            ),
            WorkshopBase(
                id=uuid.uuid4(),
                title="Workshop 11",
                description="Workshop 11 description",
                location="2F 203 Room",
                start_datetime=fri_first_st,
                end_datetime=fri_first_et
            ),
            WorkshopBase(
                id=uuid.uuid4(),
                title="Workshop 2",
                description="Workshop 2 description",
                location="2F 202 Room",
                start_datetime=fri_second_st,
                end_datetime=fri_second_et
            ),
            WorkshopBase(
                id=uuid.uuid4(),
                title="Workshop 3",
                description="Workshop 3 description",
                location="3F 301 Room",
                start_datetime=sat_first_st,
                end_datetime=sat_first_et
            ),
            WorkshopBase(
                id=uuid.uuid4(),
                title="Workshop 4",
                description="Workshop 4 description",
                location="3F 302 Room",
                start_datetime=sat_second_st,
                end_datetime=sat_second_et
            ),

        ]
    )


@router.get(
    path="/workshop/{workshop_id}",
    response_model=WorkshopDetail,
    status_code=status.HTTP_200_OK
)
@inject
async def get_workshop_detail(
    request: Request,
    response: Response,
    headers: Annotated[HeaderInfo, Header()],
    workshop_id: uuid.UUID,
) -> dict:
    """

    :param request:
    :param response:
    :param headers:
    :param workshop_id:
    :return:
    """
    response.headers["Content-Language"] = headers.accept_language
    return WorkshopDetail(
        id=workshop_id,
        title="Workshop 1",
        description="Workshop 1 description",
        location="2F 201 Room",
        start_datetime=fri_first_st,
        end_datetime=fri_first_et,
        conference="2025 The Hope Conference",
        instructor="Instructor 1",
        participants_limit=random.choice([30, 40, 50, 60]),
        is_full=random.choice([True, True, True, True, True, False, False, False, False, False])
    )
