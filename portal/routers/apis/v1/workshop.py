"""
Workshop API Router
"""
import random
import uuid
from typing import Annotated

from dateutil import parser
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Response, Depends
from fastapi.params import Header
from starlette import status

from portal.containers import Container
from portal.handlers import WorkshopHandler
from portal.libs.depends import (
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from portal.route_classes import LogRoute
from portal.serializers.base import HeaderInfo
from portal.serializers.v1.instructor import InstructorBase
from portal.serializers.v1.workshop import WorkshopDetail, WorkshopList

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
    workshop_handler: WorkshopHandler = Depends(Provide[Container.workshop_handler]),
) -> WorkshopList:
    """

    :param request:
    :param response:
    :param headers:
    :param workshop_handler:
    :return:
    """
    response.headers["Content-Language"] = headers.accept_language
    workshop_list: WorkshopList = await workshop_handler.get_workshop_list()
    return workshop_list


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
        # conference="2025 The Hope Conference",
        instructor=InstructorBase(
            name="Instructor 1",
            bio="lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua "
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure "
                "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat "
                "non proident sunt in culpa qui officia deserunt mollit anim id est laborum",
        ),
        participants_limit=random.choice([30, 40, 50, 60]),
        is_full=random.choice([True, True, True, True, True, False, False, False, False, False])
    )


@router.get(
    path="/workshop/account/registered",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, bool],
    dependencies=[check_access_token],
    responses={
        status.HTTP_200_OK: {
            "description": "Get registered workshops",
            "content": {
                "application/json": {
                    "example": {
                        uuid.uuid4().hex: True,
                        uuid.uuid4().hex: False,
                        uuid.uuid4().hex: True,
                    }
                }
            }
        }
    }
)
@inject
async def get_registered_workshops(
    request: Request,
    response: Response,
    workshop_handler: WorkshopHandler = Depends(Provide[Container.workshop_handler]),
) -> dict[str, bool]:
    """

    :param request:
    :param response:
    :param workshop_handler:
    :return:
    """
    return await workshop_handler.get_registered_workshops()


@router.post(
    path="/workshop/{workshop_id}/register",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[check_access_token]
)
@inject
async def register_workshop(
    request: Request,
    response: Response,
    workshop_id: uuid.UUID,
    workshop_handler: WorkshopHandler = Depends(Provide[Container.workshop_handler]),
) -> None:
    """

    :param request:
    :param response:
    :param workshop_id:
    :param workshop_handler:
    :return:
    """
    await workshop_handler.register_workshop(workshop_id=workshop_id)


@router.post(
    path="/workshop/{workshop_id}/unregister",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[check_access_token]
)
@inject
async def unregister_workshop(
    request: Request,
    response: Response,
    workshop_id: uuid.UUID,
    workshop_handler: WorkshopHandler = Depends(Provide[Container.workshop_handler]),
) -> None:
    """

    :param request:
    :param response:
    :param workshop_id:
    :param workshop_handler:
    :return:
    """
    await workshop_handler.unregister_workshop(workshop_id=workshop_id)
