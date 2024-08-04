"""
Authenticators for the app
"""
from fastapi import Depends

from app.exceptions.auth import UnauthorizedException
from app.libs.auth import AccessTokenAuth
from app.libs.contexts.api_context import APIContext, set_api_context


async def check_access_token(
    access_token: APIContext = Depends(AccessTokenAuth())
) -> APIContext:
    """

    :param access_token:
    :return:
    """
    if not access_token:
        raise UnauthorizedException()
    set_api_context(access_token)
    return access_token

