"""
Event Info Wagtail Hooks
"""
from zoneinfo import ZoneInfo

from django.contrib import admin
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import CreateView, EditView

from portal.libs.consts.enums import MenuOrder
from .models import EventSchedule

from .forms import EventInfoForm


class EventInfoCreateView(CreateView):
    """
    Workshop Time Slot Create View
    """

    def get_form_class(self):
        """

        :return:
        """
        return EventInfoForm


class EventInfoEditView(EditView):
    """
    Workshop Time Slot Edit View
    """

    def get_context_data(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        return context

    def get_form_class(self):
        """

        :return:
        """
        return EventInfoForm


@modeladmin_register
class EventScheduleModelAdmin(ModelAdmin):
    """
    Event Schedule Model Admin
    """
    model = EventSchedule
    menu_label = "Event Schedules"
    menu_order = MenuOrder.EventInfo
    menu_icon = "calendar"

    list_display = (
        "format_title",
        "format_description",
        "format_time_zone",
        "format_start_time",
        "format_conference",
        "format_color",
    )
    list_filter = ("conference",)

    search_fields = ("title", "description", "conference")

    ordering = ("start_time",)

    inspect_view_fields = [
        "title",
        "description",
        "time_zone",
        "start_time",
        "conference",
        "text_color",
        "background_color",
    ]
    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    create_view_class = EventInfoCreateView
    edit_view_class = EventInfoEditView

    _help_text = format_html(
        "Color in hex format. e.g. #FFFFFF for white. "
        "Visit <a href='https://www.w3schools.com/colors/colors_picker.asp' target='_blank'>HTML Color Picker</a> for choosing a color."
    )
    custom_panels = [
        FieldPanel("conference"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("time_zone"),
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

    @admin.display(description="Title")
    def format_title(self, obj: EventSchedule):
        """
        Format title
        """
        return obj.title

    @admin.display(description="Description")
    def format_description(self, obj: EventSchedule):
        """
        Format description
        """
        return obj.description

    @admin.display(description="Time Zone")
    def format_time_zone(self, obj: EventSchedule):
        """
        Format time zone
        """
        return obj.time_zone

    @admin.display(ordering="start_time", description="Start Time(Converted)")
    def format_start_time(self, obj: EventSchedule):
        """
        Format start time
        """
        start_time = obj.start_time.astimezone(tz=ZoneInfo(obj.time_zone))
        return start_time.strftime('%b %d, %Y, %I:%M %p')

    @admin.display(description="Conference")
    def format_conference(self, obj: EventSchedule):
        """
        Format conference
        """
        return obj.conference

    @admin.display(description="Color")
    def format_color(self, obj):
        """
        Format text color
        """
        if not obj.text_color and not obj.background_color:
            return "N/A"
        if obj.text_color and not obj.background_color:
            return format_html(
                f'<span style="color: {obj.text_color};">'
                f'{obj.text_color}'
                f'</span>'
            )
        if not obj.text_color and obj.background_color:
            return format_html(
                f'<span style="background-color: {obj.background_color}; border-radius: 5px; padding: 5px;">'
                f'{obj.background_color}'
                f'</span>'
            )
        return format_html(
            f'<span style="color: {obj.text_color}; background-color: {obj.background_color}; border-radius: 5px; padding: 5px;">'
            f'text color: {obj.text_color}, background color: {obj.background_color}'
            f'</span>'
        )

