"""
Account wagtail hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import CreateView, EditView

from portal.libs.consts.enums import MenuOrder
from .forms import AccountForm
from .models import Account


class AccountCreateView(CreateView):
    """
    Account Create View
    """

    def get_form_class(self):
        """

        :return:
        """
        return AccountForm


class AccountEditView(EditView):
    """
    Account Edit View
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
        return AccountForm


@modeladmin_register
class AccountModelAdmin(ModelAdmin):
    model = Account
    base_url_path = "register_accounts"
    menu_label = "Accounts"
    menu_icon = "user"
    menu_order = MenuOrder.Account

    list_display = ("display_name", "phone_number", "email", "is_active", "last_login")
    list_filter = ("is_active", "verified", "is_service")

    search_fields = ("display_name", "phone_number", "email")

    edit_view_class = AccountEditView
    create_view_class = AccountCreateView
