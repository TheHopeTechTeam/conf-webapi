"""
Instructor Wagtail Hooks
"""
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Instructor
from portal.libs.consts.enums import MenuOrder
from portal.libs.mixins.orderable_mixin import OrderableMixin


@modeladmin_register
class InstructorModelAdmin(OrderableMixin, ModelAdmin):
    """
    Instructor Model Admin
    """
    model = Instructor
    base_url_path = "instructors"
    menu_label = "Instructors"
    menu_icon = "user"
    menu_order = MenuOrder.Instructor

    list_display = ("name", "title", "bio")

    search_fields = ("name", "title", "bio")
    ordering = ("sort_order",)

    custom_panels = [
        FieldPanel("name"),
        FieldPanel("title"),
        FieldPanel("bio"),
        FieldPanel("image"),
    ]

    edit_handler = ObjectList(custom_panels)
