"""
Instructor Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Instructor


@modeladmin_register
class InstructorModelAdmin(ModelAdmin):
    model = Instructor
    base_url_path = "instructors"
    menu_label = "Instructors"
    menu_icon = "user"
    menu_order = 205
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("name", "bio")
    search_fields = ("name", "bio")
    ordering = ["name"]
