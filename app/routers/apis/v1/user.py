"""
User API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers import UserHandler
from app.libs.depends import (
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute


router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.get(
    path="/{uid}",
    status_code=status.HTTP_200_OK
)
@inject
async def get_user(
    uid: str,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> dict:
    """
    Get user
    """
    user = await user_handler.get_user(uid=uid)
    return user



