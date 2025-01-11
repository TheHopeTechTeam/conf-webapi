"""
Account wagtail hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Account
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class AccountModelAdmin(ModelAdmin):
    model = Account
    base_url_path = "register_accounts"
    menu_label = "Accounts"
    menu_icon = "user"
    menu_order = MenuOrder.Account
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("display_name", "phone_number", "email", "status")
    list_filter = ("status",)
    search_fields = ("display_name", "phone_number", "email")
