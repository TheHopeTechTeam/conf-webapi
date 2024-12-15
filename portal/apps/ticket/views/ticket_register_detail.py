"""
Ticket Register Detail Model Admin
"""
from django.contrib import admin
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.ticket.models import TicketRegisterDetail


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
