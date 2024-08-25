"""
UserHandler
"""
from datetime import datetime

import pytz
from redis.asyncio import Redis
from starlette import status

from portal.apps.account.models import Account
from portal.exceptions.api_base import APIException
from portal.libs.contexts.api_context import get_api_context, APIContext
from portal.libs.database import RedisPool
from portal.serializers.v1.user import UserLogin, LoginResponse


class UserHandler:
    """UserHandler"""

    def __init__(self):
        """initialize"""
        self.user_context: APIContext = get_api_context()

    async def login(self, model: UserLogin) -> LoginResponse:
        """
        Login
        :param model:
        :return:
        """
        if account := await Account.objects.aget(google_uid=self.user_context.uid):
            account.last_login = datetime.now(tz=pytz.UTC)
            await account.save()
            return LoginResponse(verified=True)
        await Account.objects.acreate(
            google_uid=self.user_context.uid,
            phone_number=self.user_context.token_payload.phone_number,
            auth_provider=self.user_context.token_payload.firebase.sign_in_provider,
            status="active",
            created_at=model.created_at or datetime.now(tz=pytz.UTC),
            last_login=datetime.now(tz=pytz.UTC),
            app_name=model.app_name,
        )
        return LoginResponse(verified=True, first_login=True)

    async def check_first_login(self, uid: str):
        """
        Check first login
        :param uid:
        :return:
        """
        user = await self.get_user(uid=uid)
        # return user.metadata.creation_timestamp == user.metadata.last_sign_in_timestamp

    async def get_user(self, uid: str):
        """
        Get user
        :param uid:
        :return:
        """
