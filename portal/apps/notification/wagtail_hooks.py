"""
Notification Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import CreateView, EditView

from .forms import NotificationForm
from .models import Notification
from portal.libs.consts.enums import MenuOrder


class NotificationCreateView(CreateView):
    """
    Notification Create View
    """

    def get_form_class(self):
        """

        :return:
        """
        return NotificationForm


class NotificationEditView(EditView):
    """
    Notification Edit View
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
        return NotificationForm


@modeladmin_register
class NotificationModelAdmin(ModelAdmin):
    """
    ModelAdmin for Notification
    """
    model = Notification
    base_url_path = "notification"
    menu_label = "Notification"
    menu_icon = "mail"
    menu_order = MenuOrder.Notification

    list_display = (
        "title",
        "type",
        "created_at"
    )
    list_filter = ("type",)

    search_fields = ("title", "message")
    ordering = ["-created_at"]

    inspect_view_fields = [
        "title",
        "message",
        "type",
        "created_at",
    ]

    inspect_view_enabled = True

    create_view_class = NotificationCreateView
    edit_view_class = NotificationEditView
