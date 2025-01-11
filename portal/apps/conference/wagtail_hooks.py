"""
Conference wagtail hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Conference
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class ConferenceModelAdmin(ModelAdmin):
    model = Conference
    base_url_path = "conferences"
    menu_label = "Conferences"
    menu_icon = "site"
    menu_order = MenuOrder.Conference
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("title", "start_date", "end_date", "location")
    list_filter = ("location",)
    search_fields = ("title", "location")
