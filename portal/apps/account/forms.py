"""
Account forms
"""
import phonenumbers
from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from .models import Account
from portal.libs.consts.enums import Gender


class AccountForm(WagtailAdminModelForm):
    """
    Account form
    """
    display_name = forms.CharField(
        required=True,
        label="Display Name",
        widget=forms.TextInput(attrs={"placeholder": "Display Name"}),
    )
    phone_number = forms.CharField(
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "Phone Number (+XXXXXXXXXXXXXX)"}),
        help_text="Phone number(Use International format starting with +)",
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
    )
    gender = forms.ChoiceField(
        required=False,
        label="Gender",
        choices=Gender.choices,
        widget=forms.Select(),
    )
    is_active = forms.BooleanField(
        required=False,
        label="Is Active",
        initial=True,
        widget=forms.CheckboxInput(attrs={"placeholder": "Is Active"}),
    )
    verified = forms.BooleanField(
        required=False,
        label="Verified",
        initial=False,
        widget=forms.CheckboxInput(attrs={"placeholder": "Verified"}),
        disabled=True,
    )
    last_login = forms.DateTimeField(
        required=False,
        label="Last Login",
        widget=forms.TextInput(attrs={"placeholder": "Last Login"}),
        disabled=True,
    )
    is_service = forms.BooleanField(
        required=False,
        label="Is Service",
        initial=False,
        widget=forms.CheckboxInput(attrs={"placeholder": "Is Service"}),
        help_text="是否為服事人員(會眾不需選)",
    )
    remark = forms.CharField(
        required=False,
        label="Remark",
        widget=forms.Textarea(attrs={"placeholder": "Remark"}),
    )


    def clean_phone_number(self):
        """
        Clean phone number
        :return:
        """
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Phone number must start with +")
        try:
            parse_phone_num = phonenumbers.parse(number=phone_number)
            if not phonenumbers.is_valid_number(parse_phone_num):
                raise ValueError()
            if not phonenumbers.is_possible_number(parse_phone_num):
                raise ValueError()
            phonenumbers.format_number(parse_phone_num, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            raise forms.ValidationError("Phone number is not international format")
        return phone_number


    class Meta:
        """Meta"""
        model = Account
        fields = [
            "display_name",
            "phone_number",
            "email",
            "gender",
            "is_active",
            "verified",
            "last_login",
            "is_service",
            "remark"
        ]
