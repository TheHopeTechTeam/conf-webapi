"""
Ticket router
"""
import numpy as np
import pandas as pd
import phonenumbers
import pytz
from dateutil import parser
from fastapi import APIRouter, Request, UploadFile
from firebase_admin import auth
from firebase_admin.auth import PhoneNumberAlreadyExistsError

from portal.apps.account.models import Account
from portal.apps.ticket.models import TicketRegisterDetail, Ticket
from portal.libs.logger import logger
from portal.libs.utils.async_worker import concurrency_worker

router = APIRouter()


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
        tasks = [create_or_get_firebase_user(record["參加人電話"]) for record in records]
        user_records = await concurrency_worker(tasks)
        for record, user_record in zip(records, user_records):
            if not user_record:
                continue
            record.setdefault("google_uid", user_record.uid)
            record.setdefault("phone_number", user_record.phone_number)

        pre_convert_records = {row["phone_number"]: {**row} for _, row in pd.DataFrame(records).iterrows()}
        # bulk create account
        account_objs = [
            Account(
                google_uid=record["google_uid"],
                phone_number=record["phone_number"]
            )
            for record in records if "google_uid" in record
        ]
        account_results = await Account.objects.abulk_create(objs=account_objs, ignore_conflicts=True)
        # bulk create ticket register detail
        ticket_register_detail_objs = [
            await create_ticket_register_detail_obj(account, pre_convert_records)
            for account in account_results
        ]
        result = await TicketRegisterDetail.objects.abulk_create(objs=ticket_register_detail_objs, ignore_conflicts=True)
        logger.info(f"result count: {len(result)}")
        # return HttpResponse(
        #     f"""
        #     <div>成功新增 {len(result)} 筆資料</div>
        #     <a href="/cms/{TicketRegisterDetailAdmin.base_url_path}">返回</a>
        #     """
        # )
    except Exception as e:
        logger.error(e)


async def create_or_get_firebase_user(phone_number: str):
    """

    :param phone_number:
    :return:
    """
    parse_phone_num = phonenumbers.parse(number=f"+{phone_number}")
    international_number = phonenumbers.format_number(parse_phone_num, phonenumbers.PhoneNumberFormat.E164)
    try:
        user_record = auth.create_user(phone_number=international_number)
    except PhoneNumberAlreadyExistsError:
        user_record = auth.get_user_by_phone_number(international_number)
    except Exception as e:
        logger.warning(f"international_number: {international_number}")
        logger.warning(f"Error creating user: {e}")
        return None
    return user_record


async def create_ticket_register_detail_obj(account: Account, pre_convert_records: dict) -> TicketRegisterDetail:
    """

    :param account:
    :param pre_convert_records:
    :return:
    """
    record = pre_convert_records.get(account.phone_number)
    tickets = Ticket.objects.filter(title__contains=record["票券名稱"])
    utc8_registered_at = parser.parse(record["報名時間(GTM+8)"])
    registered_at = pytz.timezone("Asia/Taipei").localize(utc8_registered_at)
    utc_registered_at = registered_at.astimezone(pytz.utc)
    account_obj = await Account.objects.filter(phone_number=account.phone_number).afirst()
    return TicketRegisterDetail(
        ticket_number=record["票號"],
        ticket=await tickets.afirst(),
        account=account_obj,
        belong_church=record["所屬教會"],
        identity=record["所屬教會身份"],
        registered_at=utc_registered_at,
    )
