"""
User API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers import UserHandler
from app.libs.depends import (
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.user import UserLogin, LoginResponse

router = APIRouter(
    dependencies=[
        check_access_token,
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.post(
    path="/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
@inject
async def login(
    model: UserLogin,
    user_handler: UserHandler = Depends(Provide[Container.user_handler]),
) -> LoginResponse:
    """
    Login
    """
    return await user_handler.login(model=model)


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



