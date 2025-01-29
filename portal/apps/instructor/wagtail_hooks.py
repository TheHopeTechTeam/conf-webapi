"""
Instructor Wagtail Hooks
"""
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Instructor
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class InstructorModelAdmin(ModelAdmin):
    model = Instructor
    base_url_path = "instructors"
    menu_label = "Instructors"
    menu_icon = "user"
    menu_order = MenuOrder.Instructor
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("name", "bio")
    search_fields = ("name", "bio")
    ordering = ["name"]

    custom_panels = [
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("bio"),
        FieldPanel("image"),
    ]

    edit_handler = ObjectList(custom_panels)
