"""
Event Info Wagtail Hooks
"""
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from portal.libs.consts.enums import MenuOrder
from .models import EventSchedule


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

    _help_text = format_html(
        "Color in hex format. e.g. #FFFFFF for white. "
        "Visit <a href='https://www.w3schools.com/colors/colors_picker.asp' target='_blank'>HTML Color Picker</a> for choosing a color."
    )
    custom_panels = [
        FieldPanel("conference"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("start_time"),
        FieldPanel(
            field_name="text_color",
            help_text=_help_text,
            attrs={"placeholder": "#FFFFFF"},
        ),
        FieldPanel(
            field_name="background_color",
            help_text=_help_text,
            attrs={"placeholder": "#FFFFFF"},
        ),
    ]

    edit_handler = ObjectList(custom_panels)
