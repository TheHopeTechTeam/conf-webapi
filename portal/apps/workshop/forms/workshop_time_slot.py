"""
Workshop forms
"""
import datetime
from zoneinfo import ZoneInfo

from dateutil import parser
from django import forms
from wagtail.admin import widgets
from wagtail.admin.forms import WagtailAdminModelForm

from portal.apps.workshop.models import WorkshopTimeSlot


class WorkshopTimeSlotForm(WagtailAdminModelForm):
    """
    Workshop Time Slot form
    """
    start_datetime = forms.DateTimeField(
        required=True,
        label="Start Date Time",
        widget=widgets.AdminDateTimeInput(
            attrs={"placeholder": "YYYY-MM-DD HH:MM"},
            format="%Y-%m-%d %H:%M",
        ),
        help_text="Please enter UTC time, system will automatically convert to selected time zone, but here only show UTC time",
    )
    end_datetime = forms.DateTimeField(
        required=True,
        label="End Date Time",
        widget=widgets.AdminDateTimeInput(
            attrs={"placeholder": "YYYY-MM-DD HH:MM"},
            format="%Y-%m-%d %H:%M",
        ),
        help_text="Please enter UTC time, system will automatically convert to selected time zone, but here only show UTC time",
    )

    def clean_start_datetime(self):
        """
        Clean start_datetime
        """
        start_datetime = self.cleaned_data.get("start_datetime")
        now = datetime.datetime.now(tz=ZoneInfo("UTC"))
        if not start_datetime:
            raise forms.ValidationError("Start Date and Time is required")
        if start_datetime < now:
            raise forms.ValidationError(
                f"Date and Time should be greater than current Date and Time in UTC time(current: {now.strftime('%Y-%m-%d %H:%M%z')})"
            )
        return start_datetime

    def clean_end_datetime(self):
        """
        Clean end_datetime
        """
        if not self.data.get("start_datetime"):
            raise forms.ValidationError("Start Date and Time is required")
        start_datetime = parser.parse(self.data.get("start_datetime"))
        start_datetime = start_datetime.replace(tzinfo=ZoneInfo("UTC"))
        end_datetime = self.cleaned_data.get("end_datetime")
        if not end_datetime:
            raise forms.ValidationError("End Date and Time is required")
        if end_datetime < start_datetime:
            raise forms.ValidationError("End Date and Time should be greater than Start Date and Time")
        return end_datetime

    class Meta:
        """Meta"""
        model = WorkshopTimeSlot
        fields = [
            "title",
            "time_zone",
            "start_datetime",
            "end_datetime"
        ]
