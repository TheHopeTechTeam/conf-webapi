"""
Ticket Register Detail Model Admin
"""
from django.contrib import admin
from wagtail.admin.panels import ObjectList, FieldPanel
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin
from wagtail_modeladmin.views import CreateView, EditView
from wagtailautocomplete.edit_handlers import AutocompletePanel

from portal.apps.ticket.models import TicketRegisterDetail


class TicketRegisterDetailPermission(PermissionHelper):
    """TicketRegisterDetailPermission"""

    def user_can_copy_obj(self, user, obj):
        """

        :param user:
        :param obj:
        :return:
        """
        return False


class TicketRegisterDetailCreateView(CreateView):
    """
    Ticket Register Detail Create View

    Solution: https://stackoverflow.com/questions/73288952/initialize-request-in-get-edit-handler-in-modeladmin-class-in-wagtail
    """
    def setup(self, request, *args, **kwargs):
        """
        Setup
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        super().setup(request, *args, **kwargs)
        self.edit_handler = self.get_edit_handler()

    def get_edit_handler(self):
        """
        Get edit handler
        :return:
        """
        custom_panels = [
            FieldPanel(field_name="ticket_number"),
            FieldPanel(field_name="ticket"),
            AutocompletePanel(field_name="account"),
            FieldPanel(field_name="belong_church"),
            FieldPanel(field_name="identity"),
            FieldPanel(field_name="registered_at"),
            FieldPanel(field_name="order_person_name"),
            FieldPanel(field_name="order_person_phone_number"),
            FieldPanel(field_name="order_person_email"),
            FieldPanel(field_name="remark")
        ]
        edit_handler = ObjectList(custom_panels)
        return edit_handler.bind_to_model(self.model_admin.model)


class TicketRegisterDetailEditView(EditView):
    """
    Ticket Register Detail Edit View
    """

    def setup(self, request, *args, **kwargs):
        """
        Setup
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        super().setup(request, *args, **kwargs)
        self.edit_handler = self.get_edit_handler()

    def get_edit_handler(self):
        """
        Get edit handler
        :return:
        """
        custom_panels = [
            FieldPanel(field_name="ticket_number", read_only=True),
            FieldPanel(field_name="ticket", read_only=True),
            AutocompletePanel(field_name="account"),
            FieldPanel(field_name="belong_church"),
            FieldPanel(field_name="identity"),
            FieldPanel(field_name="registered_at", read_only=True),
            FieldPanel(field_name="order_person_name", read_only=True),
            FieldPanel(field_name="order_person_phone_number", read_only=True),
            FieldPanel(field_name="order_person_email", read_only=True),
            FieldPanel(field_name="remark")
        ]
        edit_handler = ObjectList(custom_panels)
        return edit_handler.bind_to_model(self.model_admin.model)


class TicketRegisterDetailAdmin(ModelAdmin):
    """
    Ticket Register Detail Model Admin
    """
    model = TicketRegisterDetail
    base_url_path = "ticket_register_details"
    menu_label = "Ticket Register Detail"
    menu_icon = "folder-open-inverse"

    list_filter = ("ticket", "ticket__ticket_type", "identity")
    list_display = (
        "format_ticket_number",
        "format_ticket",
        # "format_ticket_type",
        "format_account_display_name",
        "format_account_phone_number",
        "format_belong_church",
        "format_identity"
    )

    search_fields = ("ticket_number",)
    ordering = ["registered_at"]

    inspect_view_fields = [
        "ticket_number",
        "ticket",
        "account",
        "belong_church",
        "identity",
        "registered_at",
        "unregistered_at",
        "order_person_name",
        "order_person_phone_number",
        "order_person_email",
        "remark"
    ]

    create_view_class = TicketRegisterDetailCreateView
    edit_view_class = TicketRegisterDetailEditView

    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    index_template_name = "modeladmin/ticket/ticket_register_details/index.html"

    permission_helper_class = TicketRegisterDetailPermission

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
