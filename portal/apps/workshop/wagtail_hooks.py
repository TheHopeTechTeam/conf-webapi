"""
Workshop Wagtail Hooks
"""
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Workshop


@modeladmin_register
class WorkshopModelAdmin(ModelAdmin):
    model = Workshop
    base_url_path = "workshops"
    menu_label = "Workshops"
    menu_icon = "site"
    menu_order = 206
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("title",)
    list_filter = ("location", "conference")
    search_fields = ("title", "location")
    ordering = ["title"]

    custom_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("conference"),
        FieldPanel("location"),
        FieldPanel("instructor")
    ]
    edit_handler = ObjectList(custom_panels)
