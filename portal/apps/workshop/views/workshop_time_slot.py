"""
Workshop Time Slot Model Admin
"""
from argparse import ZERO_OR_MORE
from zoneinfo import ZoneInfo

from django.contrib import admin
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin
from wagtail_modeladmin.views import CreateView, EditView

from portal.apps.workshop.forms.workshop_time_slot import WorkshopTimeSlotForm
from portal.apps.workshop.models import WorkshopTimeSlot


class WorkshopTimeSlotCreateView(CreateView):
    """
    Workshop Time Slot Create View
    """

    def get_form_class(self):
        """

        :return:
        """
        return WorkshopTimeSlotForm


class WorkshopTimeSlotEditView(EditView):
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
        return WorkshopTimeSlotForm


class WorkshopTimeSlotModelAdmin(ModelAdmin):
    """
    Workshop Time Slot Model Admin
    """
    model = WorkshopTimeSlot
    base_url_path = "workshop-time-slots"
    menu_label = "Workshop Time Slots"
    menu_icon = "date"

    list_display = (
        "title",
        "time_zone",
        "format_start_datetime",
        "format_end_datetime",
    )

    search_fields = ("title",)
    ordering = ["start_datetime"]

    inspect_view_fields = [
        "title",
        "time_zone",
        "start_datetime",
        "end_datetime",
    ]
    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    create_view_class = WorkshopTimeSlotCreateView
    edit_view_class = WorkshopTimeSlotEditView

    custom_panels = [
        FieldPanel("title"),
        FieldPanel("time_zone"),
        FieldPanel("start_datetime"),
        FieldPanel("end_datetime"),
    ]

    edit_handler = ObjectList(custom_panels)


    @admin.display(description="Start Date Time(Converted)")
    def format_start_datetime(self, obj: WorkshopTimeSlot):
        """

        :param obj:
        :return:
        """
        start_datetime = obj.start_datetime.astimezone(tz=ZoneInfo(obj.time_zone))
        return start_datetime.strftime('%b %d, %Y, %I:%M %p')

    @admin.display(description="End Date Time(Converted)")
    def format_end_datetime(self, obj: WorkshopTimeSlot):
        """

        :param obj:
        :return:
        """
        end_datetime = obj.end_datetime.astimezone(tz=ZoneInfo(obj.time_zone))
        return end_datetime.strftime('%b %d, %Y, %I:%M %p')
