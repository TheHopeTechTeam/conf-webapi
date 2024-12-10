"""
Ticket Register Detail Model Admin
"""
import numpy as np
import pandas as pd
import phonenumbers
import pytz
from dateutil import parser
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from firebase_admin import auth
from firebase_admin.auth import PhoneNumberAlreadyExistsError
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.account.models import Account
from portal.apps.ticket.models import TicketRegisterDetail, Ticket
from portal.libs.logger import logger


def upload_csv(request: WSGIRequest):
    if request.method == "POST" and request.FILES["csv_file"]:
        try:
            csv_file = request.FILES["csv_file"]
            raw_df = pd.read_csv(csv_file)
            raw_df = raw_df.replace({np.nan: None})
            records = raw_df.to_dict(orient="records")
            records = records[0:3]
            # create firebase user
            for record in records:
                user_record = create_or_get_firebase_user(record["參加人電話"])
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
                for record in records
            ]
            account_results = Account.objects.bulk_create(objs=account_objs, ignore_conflicts=True)
            # bulk create ticket register detail
            ticket_register_detail_objs = [
                create_ticket_register_detail_obj(account, pre_convert_records)
                for account in account_results
            ]
            result = TicketRegisterDetail.objects.bulk_create(objs=ticket_register_detail_objs, ignore_conflicts=True)
            return HttpResponse(
                f"""
                <div>成功新增 {len(result)} 筆資料</div>
                <a href="/cms/{TicketRegisterDetailAdmin.base_url_path}">返回</a>
                """
            )
        except Exception as e:
            logger.error(e)
            return HttpResponse(f"Error uploading file: {e}")
    return redirect("index")


def get_international_phone_number(phone_number: str):
    """

    :param phone_number:
    :return:
    """
    parse_phone_num = phonenumbers.parse(number=f"+{phone_number}")
    international_number = phonenumbers.format_number(parse_phone_num, phonenumbers.PhoneNumberFormat.E164)
    return international_number


def create_or_get_firebase_user(phone_number: str):
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
        logger.warning(f"Error creating user: {e}")
        return None
    return user_record


def create_ticket_register_detail_obj(account: Account, pre_convert_records: dict) -> TicketRegisterDetail:
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
    account_obj = Account.objects.filter(phone_number=account.phone_number).first()
    return TicketRegisterDetail(
        ticket_number=record["票號"],
        ticket=tickets.first(),
        account=account_obj,
        belong_church=record["所屬教會"],
        identity=record["所屬教會身份"],
        registered_at=utc_registered_at,
    )


class TicketRegisterDetailPermission(PermissionHelper):
    """TicketRegisterDetailPermission"""

    def user_can_create(self, user):
        """

        :param user:
        :return:
        """
        return False

    def user_can_edit_obj(self, user, obj):
        """

        :param user:
        :param obj:
        :return:
        """
        return False

    def user_can_copy_obj(self, user, obj):
        """

        :param user:
        :param obj:
        :return:
        """
        return False


class TicketRegisterDetailAdmin(ModelAdmin):
    """
    Ticket Register Detail Model Admin
    """
    model = TicketRegisterDetail
    menu_label = "Ticket Register Detail"
    menu_icon = "folder-open-inverse"

    list_filter = ("ticket",)
    list_display = (
        "format_ticket_number",
        "format_ticket",
        "format_ticket_type",
        "format_account_display_name",
        "format_account_phone_number",
        "format_belong_church",
        "format_identity"
    )

    search_fields = ("ticket",)
    ordering = ["ticket"]

    index_template_name = "modeladmin/ticket/ticket_register_details/index.html"

    permission_helper_class = TicketRegisterDetailPermission

    base_url_path = "ticket_register_details"

    def get_queryset(self, request):
        """
        Get queryset
        """
        return super(TicketRegisterDetailAdmin, self).get_queryset(request)

    @admin.display(description="票號")
    def format_ticket_number(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.ticket_number

    @admin.display(description="票券名稱")
    def format_ticket(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.ticket

    @admin.display(description="票券分類")
    def format_ticket_type(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.ticket.ticket_type

    @admin.display(description="名稱")
    def format_account_display_name(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.account.display_name

    @admin.display(description="電話")
    def format_account_phone_number(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.account.phone_number

    @admin.display(description="所屬教會")
    def format_belong_church(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.belong_church

    @admin.display(description="身份")
    def format_identity(self, obj: TicketRegisterDetail):
        """

        :param obj:
        :return:
        """
        return obj.get_identity_display()
