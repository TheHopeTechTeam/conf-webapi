"""
AccountHandler
"""
import uuid
from datetime import datetime

import pytz
from django.db import IntegrityError
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status

from portal.apps.account.models import Account, AccountAuthProvider
from portal.apps.ticket.models import TicketRegisterDetail, Ticket, TicketType
from portal.exceptions.api_base import APIException
from portal.handlers import AuthHandler
from portal.libs.consts.enums import Provider, LoginMethod
from portal.libs.contexts.api_context import get_api_context, APIContext
from portal.libs.logger import logger
from portal.schemas.auth import FirebaseTokenPayload
from portal.serializers.v1.account import AccountLogin, AccountUpdate, LoginResponse, AccountDetail


class AccountHandler:
    """AccountHandler"""

    def __init__(self):
        """initialize"""
        try:
            self._api_context: APIContext = get_api_context()
        except Exception:
            self._api_context = None

    @staticmethod
    async def verify_login_token(token: str) -> FirebaseTokenPayload:
        """
        Verify login token
        :param token:
        :return:
        """
        auth_handler = AuthHandler()
        scheme, credentials = get_authorization_scheme_param(token)
        try:
            return await auth_handler.verify_firebase_token(token=credentials)
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            raise APIException(status_code=status.HTTP_401_UNAUTHORIZED, message="Unauthorized")

    async def login(self, model: AccountLogin) -> LoginResponse:
        """
        Login
        :param model:
        :return:
        """
        match model.login_method:
            case LoginMethod.FIREBASE:
                return await self.firebase_login(model=model)
            case _:
                raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid login method")

    async def firebase_login(self, model: AccountLogin) -> LoginResponse:
        """
        Firebase login
        :param model:
        :return:
        """
        token_payload: FirebaseTokenPayload = await self.verify_login_token(model.firebase_token)
        account_exists = await AccountAuthProvider.objects.filter(provider_id=token_payload.user_id).aexists()
        now = datetime.now(tz=pytz.UTC)
        if account_exists:
            auth_provider_obj: AccountAuthProvider = await AccountAuthProvider.objects.aget(provider_id=token_payload.user_id)
            auth_provider_obj.extra_data = token_payload.model_dump(
                exclude={"name", "email", "phone_number", "exp", "iat", "user_id"}
            )
            account: Account = await Account.objects.aget(id=auth_provider_obj.account_id)
            account.verified = True
            account.last_login = now
            await auth_provider_obj.asave()
            await account.asave()
            return LoginResponse(id=account.id, verified=True)
        try:
            account_obj: Account = await Account.objects.acreate(
                phone_number=token_payload.phone_number,
                is_active=True,
                verified=True,
                last_login=now,
            )
        except IntegrityError as e:
            if f"Key (phone_number)=({token_payload.phone_number}) already exists." not in str(e):
                logger.error(f"Error creating account: {e}")
                raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")
            account_obj: Account = await Account.objects.aget(phone_number=token_payload.phone_number)
            account_obj.verified = True
            account_obj.last_login = now
            await account_obj.asave()
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")

        try:
            await AccountAuthProvider.objects.acreate(
                account=account_obj,
                provider=Provider.FIREBASE.value,
                provider_id=token_payload.user_id,
                extra_data=token_payload.model_dump(
                    exclude={"name", "email", "phone_number", "exp", "iat", "user_id"}
                )
            )
        except Exception as e:
            logger.error(f"Error creating account provider: {e}")
            await account_obj.adelete(soft=False)
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")
        return LoginResponse(id=account_obj.id, verified=True, first_login=True)

    async def check_first_login(self, uid: str):
        """
        Check first time login
        :param uid:
        :return:
        """
        # account = await self.get_account(uid=uid)
        # return user.metadata.creation_timestamp == user.metadata.last_sign_in_timestamp

    async def get_account(self, account_id: uuid.UUID) -> AccountDetail:
        """
        Get account
        :param account_id:
        :return:
        """
        if account_id != self._api_context.account.id:
            raise APIException(status_code=status.HTTP_403_FORBIDDEN, message="Forbidden")
        account_obj = await Account.objects.aget(id=account_id)
        ticket_register_detail_obj = await TicketRegisterDetail.objects.filter(account=account_obj).afirst()
        if not ticket_register_detail_obj:
            return AccountDetail(
                id=account_obj.id,
                email=account_obj.email,
                phone_number=account_obj.phone_number,
                display_name=account_obj.display_name
            )
        ticket_obj = await Ticket.objects.filter(id=ticket_register_detail_obj.ticket_id).afirst()
        ticket_type_obj = await TicketType.objects.filter(id=ticket_obj.ticket_type_id).afirst()
        account = AccountDetail(
            id=account_obj.id,
            email=account_obj.email,
            phone_number=account_obj.phone_number,
            display_name=account_obj.display_name,
            ticket_number=ticket_register_detail_obj.ticket_number,
            ticket_type=ticket_type_obj.name,
            belong_church=ticket_register_detail_obj.belong_church,
            identity=ticket_register_detail_obj.identity
        )
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

    async def delete_account(self, account_id: uuid.UUID):
        """
        Delete account
        :param account_id:
        :return:
        """
        if account_id != self._api_context.account.id:
            raise APIException(status_code=status.HTTP_403_FORBIDDEN, message="Forbidden")
        account = await Account.objects.aget(id=account_id)
        await account.adelete()
        return None
