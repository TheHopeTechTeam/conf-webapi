"""
Event Info Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel, ObjectList

from .models import EventSchedule
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class EventScheduleModelAdmin(ModelAdmin):
    """
    Event Schedule Model Admin
    """
    menu_label = "Event Schedules"
    menu_order = MenuOrder.EventInfo
    # menu_icon = "folder-open-inverse"
    model = EventSchedule

    list_display = ("title", "description", "start_time", "conference")
    list_filter = ("conference",)

    search_fields = ("title", "description", "conference")

    inspect_view_fields = [
        "title",
        "description",
        "start_time",
        "conference",
    ]
    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    custom_panels = [
        FieldPanel("conference"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("start_time"),
    ]

    edit_handler = ObjectList(custom_panels)
