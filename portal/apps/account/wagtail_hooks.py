"""
Account wagtail hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel, ObjectList

from .models import Account
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class AccountModelAdmin(ModelAdmin):
    model = Account
    base_url_path = "register_accounts"
    menu_label = "Accounts"
    menu_icon = "user"
    menu_order = MenuOrder.Account

    list_display = ("display_name", "phone_number", "email", "is_active", "last_login")
    list_filter = ("is_active", "verified", "is_service")

    search_fields = ("display_name", "phone_number", "email")

    custom_panels = [
        FieldPanel(field_name="display_name"),
        FieldPanel(field_name="phone_number", read_only=True),
        FieldPanel(field_name="email"),
        FieldPanel(field_name="is_active"),
        FieldPanel(field_name="verified", read_only=True),
        FieldPanel(field_name="last_login", read_only=True),
        FieldPanel(field_name="is_service", help_text="是否為服侍"),
    ]

    edit_handler = ObjectList(custom_panels)
