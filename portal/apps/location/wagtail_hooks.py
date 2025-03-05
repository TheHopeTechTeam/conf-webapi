"""
Location Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Location
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class LocationModelAdmin(ModelAdmin):
    model = Location
    base_url_path = "locations"
    menu_label = "Locations"
    menu_icon = "thumbtack"
    menu_order = MenuOrder.Location
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("name", "address", "floor", "room_number", "latitude", "longitude")
    search_fields = ("name", "address", "floor", "room_number")
    ordering = ["name"]
