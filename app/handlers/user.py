"""
UserHandler
"""
from redis.asyncio import Redis
from starlette import status

from app.exceptions.api_base import APIException
from app.libs.database import RedisPool
from app.serializers.v1.user import UserLogin, LoginResponse


class UserHandler:
    """UserHandler"""

    def __init__(
        self,
        # redis: RedisPool
    ):
        """initialize"""
        # self.redis: Redis = redis.create()

    async def login(self, model: UserLogin) -> LoginResponse:
        """
        Login
        :param model:
        :return:
        """
        return LoginResponse(verified=True, first_login=True)

    async def check_first_login(self, uid: str) -> bool:
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
