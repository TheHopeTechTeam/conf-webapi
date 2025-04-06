"""
Notification forms
"""
from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from portal.libs.consts.enums import (NotificationType)
from .models import Notification


class NotificationForm(WagtailAdminModelForm):
    """
    Notification form
    """
    title = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={"placeholder": "Notification Title"}),
    )
    message = forms.CharField(
        required=True,
        label="Message",
        widget=forms.Textarea(attrs={"placeholder": "Notification Message"}),
    )
    type = forms.ChoiceField(
        required=True,
        label="Type",
        choices=[(NotificationType.MULTIPLE.value, NotificationType.MULTIPLE.name.title())],
        widget=forms.Select(attrs={"placeholder": "Notification Type"}),
    )


    class Meta:
        """Meta"""
        model = Notification
        fields = [
            "title",
            "message",
            "type"
        ]
