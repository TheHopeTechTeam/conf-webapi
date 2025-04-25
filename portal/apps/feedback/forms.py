"""
Feedback forms
"""
from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from portal.libs.consts.enums import FeedbackStatus
from .models import Feedback


class FeedbackForm(WagtailAdminModelForm):
    """
    Feedback form
    """
    name = forms.CharField(
        label="Name",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Full Name"}),
        disabled=True
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(attrs={"placeholder": "Email Address"}),
        disabled=True
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"placeholder": "Feedback Message"}),
        disabled=True
    )
    remark = forms.CharField(
        required=False,
        label="Remark",
        widget=forms.Textarea(attrs={"placeholder": "Remark"}),
    )
    status = forms.ChoiceField(
        label="Status",
        choices=[(status.value, status.name.title()) for status in FeedbackStatus],
        widget=forms.Select(attrs={"placeholder": "Feedback Status"}),
    )


    class Meta:
        """Meta"""
        model = Feedback
        fields = [
            "name",
            "email",
            "message",
            "remark",
            "status",
        ]
