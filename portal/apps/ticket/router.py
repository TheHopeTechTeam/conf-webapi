"""
Ticket router
"""
import numpy as np
import pandas as pd
import phonenumbers
import pytz
from dateutil import parser
from django.conf import settings
from fastapi import APIRouter, Request, UploadFile
from firebase_admin import auth
from firebase_admin.auth import PhoneNumberAlreadyExistsError, UserRecord
from pydantic import BaseModel

from portal.apps.account.models import Account, AccountAuthProvider
from portal.apps.ticket.models import TicketRegisterDetail, Ticket
from portal.libs.consts.enums import Provider, Gender
from portal.libs.logger import logger
from portal.libs.utils.async_worker import concurrency_worker

router = APIRouter()


class UserInfo(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }
    firebase_user: UserRecord
    exist: bool
    wrong_phone_number: bool


@router.post(
    path="/ticket_register_detail/upload_csv"
)
async def upload_csv(
    request: Request,
    csv_file: UploadFile
):
    """

    :param request:
    :param csv_file:
    :return:
    """
    try:
        raw_df = pd.read_csv(csv_file.file)
        raw_df = raw_df.replace({np.nan: None})
        records = raw_df.to_dict(orient="records")
        # logger.info("record count: %s", len(records))
        # records = records[0:3]
        # create firebase user
        tasks = [create_or_get_firebase_user(str(int(record["參加人電話"]))) for record in records]
        user_infos: list[UserInfo] = await concurrency_worker(tasks)
        for record, user_info in zip(records, user_infos):
            if not user_info:
                continue
            record.setdefault("user_info", user_info)

        pre_convert_records = {row["user_info"].firebase_user.phone_number: {**row} for _, row in pd.DataFrame(records).iterrows()}
        # bulk create account
        account_results = await bulk_create_account_objs(records)
        # bulk create account auth
        await bulk_create_account_auth(records)
        # bulk create ticket register detail
        ticket_register_detail_objs = [
            await create_ticket_register_detail_obj(account, pre_convert_records)
            for account in account_results
        ]
        result = await TicketRegisterDetail.objects.abulk_create(objs=ticket_register_detail_objs, ignore_conflicts=True)
        logger.info(f"result count: {len(result)}")
    except Exception as e:
        logger.error(e)


async def create_or_get_firebase_user(phone_number: str) -> UserInfo:
    """

    :param phone_number:
    :return:
    """
    parse_phone_num = phonenumbers.parse(number=f"+{phone_number}")
    international_number = phonenumbers.format_number(parse_phone_num, phonenumbers.PhoneNumberFormat.E164)
    try:
        user_record = auth.create_user(phone_number=international_number)
        return UserInfo(firebase_user=user_record, exist=False, wrong_phone_number=False)
    except PhoneNumberAlreadyExistsError:
        user_record = auth.get_user_by_phone_number(international_number)
        return UserInfo(firebase_user=user_record, exist=True, wrong_phone_number=False)
    except Exception as e:
        user_record = auth.get_user_by_phone_number(settings.FIREBASE_TEST_PHONE_NUMBER)
        return UserInfo(firebase_user=user_record, exist=False, wrong_phone_number=True)


async def create_ticket_register_detail_obj(account: Account, pre_convert_records: dict) -> TicketRegisterDetail:
    """

    :param account:
    :param pre_convert_records:
    :return:
    """
    record = pre_convert_records.get(account.phone_number)
    user_info: UserInfo = record["user_info"]
    ticket = await Ticket.objects.filter(title__contains=record["票券名稱"]).afirst()
    utc8_registered_at = parser.parse(record["報名時間(GTM+8)"])
    registered_at = pytz.timezone("Asia/Taipei").localize(utc8_registered_at)
    utc_registered_at = registered_at.astimezone(pytz.utc)
    account_obj = await Account.objects.filter(phone_number=account.phone_number).afirst()
    remark = ""
    if user_info.exist:
        remark += f"------\n參加人: {record.get('參加人姓名')}\n參加人電話: {str(int(record.get('參加人電話')))}\n(訂購人可能買兩張以上票券)\n"
    if user_info.wrong_phone_number:
        remark += f"------\n錯誤電話號碼: {str(int(record.get('參加人電話')))}"

    return TicketRegisterDetail(
        ticket_number=record.get("票號"),
        ticket=ticket,
        account=account_obj,
        belong_church=record.get("所屬教會"),
        identity=record.get("所屬教會身份"),
        registered_at=utc_registered_at,
        order_person_name=record.get("訂購人姓名"),
        order_person_phone_number=str(int(record.get("訂購人電話"))),
        order_person_email=record.get("訂購人Email"),
        remark=remark
    )


async def bulk_create_account_objs(records: list[dict]) -> list[Account]:
    """

    :param records:
    :return:
    """
    account_objs = []
    for record in records:
        user_info = record["user_info"]
        firebase_user: UserRecord = user_info.firebase_user
        if "男" in record.get("性別"):
            gender = Gender.MALE
        elif "女" in record.get("性別"):
            gender = Gender.FEMALE
        else:
            gender = Gender.UNKNOWN
        account_obj = Account(
            phone_number=firebase_user.phone_number,
            display_name=record.get("參加人姓名"),
            gender=gender.value
        )
        account_objs.append(account_obj)
    account_results = await Account.objects.abulk_create(objs=account_objs, ignore_conflicts=True)
    return account_results


async def bulk_create_account_auth(records: list[dict]):
    """

    :param records:
    :return:
    """
    account_auth_objs = []
    for record in records:
        user_info: UserInfo = record["user_info"]
        firebase_user: UserRecord = user_info.firebase_user
        account_obj = await Account.objects.filter(phone_number=firebase_user.phone_number).afirst()
        account_auth_objs.append(
            AccountAuthProvider(
                account=account_obj,
                provider=Provider.FIREBASE.value,
                provider_id=firebase_user.uid
            )
        )
    await AccountAuthProvider.objects.abulk_create(objs=account_auth_objs, ignore_conflicts=True)
