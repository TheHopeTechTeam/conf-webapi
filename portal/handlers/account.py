"""
AccountHandler
"""
import uuid
from datetime import datetime

import pytz
from starlette import status

from portal.apps.account.models import Account
from portal.exceptions.api_base import APIException
from portal.libs.contexts.api_context import get_api_context, APIContext
from portal.serializers.v1.account import AccountLogin, AccountUpdate, LoginResponse


class AccountHandler:
    """AccountHandler"""

    def __init__(self):
        """initialize"""
        self._api_context: APIContext = get_api_context()

    async def login(self, model: AccountLogin) -> LoginResponse:
        """
        Login
        :param model:
        :return:
        """
        if account := await Account.objects.aget(google_uid=self._api_context.uid):
            account.last_login = datetime.now(tz=pytz.UTC)
            await account.asave()
            return LoginResponse(id=account.id, verified=True)
        account_obj: Account = await Account.objects.acreate(
            google_uid=self._api_context.uid,
            phone_number=self._api_context.token_payload.phone_number,
            auth_provider=self._api_context.token_payload.firebase.sign_in_provider,
            status="active",
            created_at=model.created_at or datetime.now(tz=pytz.UTC),
            last_login=datetime.now(tz=pytz.UTC),
            app_name=model.app_name,
        )
        return LoginResponse(id=account_obj.id, verified=True, first_login=True)

    async def check_first_login(self, uid: str):
        """
        Check first time login
        :param uid:
        :return:
        """
        # account = await self.get_account(uid=uid)
        # return user.metadata.creation_timestamp == user.metadata.last_sign_in_timestamp

    async def get_account(self, uid: str):
        """
        Get user
        :param uid:
        :return:
        """
        if uid != self._api_context.uid:
            raise APIException(status_code=status.HTTP_403_FORBIDDEN, message="Forbidden")
        if account := self._api_context.account:
            return account
        account = await Account.objects.aget(google_uid=uid)
        return account

    async def update_account(self, account_id: uuid.UUID, model: AccountUpdate):
        """
        Update account
        :param account_id:
        :param model:
        :return:
        """
        if account_id != self._api_context.account.id:
            raise APIException(status_code=status.HTTP_403_FORBIDDEN, message="Forbidden")
        account = await Account.objects.aget(id=account_id)
        account.email = model.email
        account.display_name = model.display_name
        await account.asave()
        return None
