"""
Workshop forms
"""
import datetime
from zoneinfo import ZoneInfo

from dateutil import parser
from django import forms
from django.utils.html import format_html
from wagtail.admin import widgets
from wagtail.admin.forms import WagtailAdminModelForm

from .models import EventSchedule


class EventInfoForm(WagtailAdminModelForm):
    """
    Event Info form
    """
    start_time = forms.DateTimeField(
        required=True,
        label="Start Time",
        widget=widgets.AdminDateTimeInput(
            attrs={"placeholder": "YYYY-MM-DD HH:MM"},
            format="%Y-%m-%d %H:%M",
        ),
        help_text=format_html(
            "Please enter UTC time, system will automatically convert to selected time zone, but here only show UTC time. "
            "<br>Vist <a href='https://www.timeanddate.com/worldclock/converter.html' target='_blank'>Time Zone Converter</a> for converting time zone."
        ),
    )
    _help_text = format_html(
        "Color in hex format. e.g. #FFFFFF for white. "
        "Visit <a href='https://www.w3schools.com/colors/colors_picker.asp' target='_blank'>HTML Color Picker</a> for choosing a color."
    )
    text_color = forms.CharField(
        required=False,
        label="Text Color",
        widget=forms.TextInput(attrs={"placeholder": "#FFFFFF"}),
        help_text=_help_text,
    )
    background_color = forms.CharField(
        required=False,
        label="Background Color",
        widget=forms.TextInput(attrs={"placeholder": "#FFFFFF"}),
        help_text=_help_text,
    )

    def clean_start_time(self):
        """
        Clean start time
        """
        start_time = self.cleaned_data.get("start_time")
        now = datetime.datetime.now(tz=ZoneInfo("UTC"))
        if not start_time:
            raise forms.ValidationError("Start Date and Time is required")
        if start_time < now:
            raise forms.ValidationError(
                f"Date and Time should be greater than current Date and Time in UTC time(current: {now.strftime('%Y-%m-%d %H:%M%z')})"
            )
        return start_time

    class Meta:
        """Meta"""
        model = EventSchedule
        fields = [
            "conference",
            "title",
            "description",
            "time_zone",
            "start_time",
            "text_color",
            "background_color",
        ]
