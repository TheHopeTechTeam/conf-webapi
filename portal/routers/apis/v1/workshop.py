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
from portal.serializers.v1.workshop import WorkshopDetail, WorkshopList, WorkshopBase
from portal.serializers.response_examples import workshop

router = APIRouter(
    dependencies=[
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)

fri_first_st = parser.parse("2025-05-02T14:00:00+08:00")
fri_first_et = parser.parse("2025-05-02T15:20:00+08:00")
fri_second_st = parser.parse("2025-05-02T15:20:00+08:00")
fri_second_et = parser.parse("2025-05-02T16:40:00+08:00")
sat_first_st = parser.parse("2025-05-03T14:00:00+08:00")
sat_first_et = parser.parse("2025-05-03T15:20:00+08:00")
sat_second_st = parser.parse("2025-05-03T15:20:00+08:00")
sat_second_et = parser.parse("2025-05-03T16:40:00+08:00")


@router.get(
    path="/schedules",
    response_model=dict[str, dict[str, list[WorkshopBase]]],
    status_code=status.HTTP_200_OK,
    responses=workshop.WORKSHOP_LIST
)
@inject
async def get_workshop_schedules(
    request: Request,
    response: Response,
    headers: Annotated[HeaderInfo, Header()],
    workshop_handler: WorkshopHandler = Depends(Provide[Container.workshop_handler]),
):
    """

    :param request:
    :param response:
    :param headers:
    :param workshop_handler:
    :return:
    """
    response.headers["Content-Language"] = headers.accept_language
    workshop_obj = await workshop_handler.get_workshop_schedules()
    return workshop_obj


@router.get(
    path="/{workshop_id}",
    response_model=WorkshopDetail,
    status_code=status.HTTP_200_OK
)
@inject
async def get_workshop_detail(
    request: Request,
    response: Response,
    headers: Annotated[HeaderInfo, Header()],
    workshop_id: uuid.UUID,
    workshop_handler: WorkshopHandler = Depends(Provide[Container.workshop_handler]),
) -> WorkshopDetail:
    """

    :param request:
    :param response:
    :param headers:
    :param workshop_id:
    :param workshop_handler:
    :return:
    """
    response.headers["Content-Language"] = headers.accept_language
    return await workshop_handler.get_workshop_detail(workshop_id=workshop_id)


@router.get(
    path="/account/registered",
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
    path="/{workshop_id}/register",
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
    path="/{workshop_id}/unregister",
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
