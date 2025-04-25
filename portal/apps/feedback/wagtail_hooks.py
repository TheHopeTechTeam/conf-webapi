"""
Location Wagtail Hooks
"""
from django.contrib import admin
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import CreateView, EditView

from portal.libs.consts.enums import MenuOrder, FeedbackStatus
from .forms import FeedbackForm
from .models import Feedback


class FeedbackPermission(PermissionHelper):
    """FeedbackPermission"""

    def user_can_create(self, user):
        """
        User can create obj
        :param user:
        :return:
        """
        return False

    def user_can_delete_obj(self, user, obj):
        """
        User can delete obj
        :param user:
        :param obj:
        :return:
        """
        return False


class FeedbackCreateView(CreateView):
    """
    Feedback Create View
    """

    def get_form_class(self):
        """

        :return:
        """
        return FeedbackForm


class FeedbackEditView(EditView):
    """
    Feedback Edit View
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
        return FeedbackForm


@modeladmin_register
class FeedbackModelAdmin(ModelAdmin):
    model = Feedback
    base_url_path = "Feedback"
    menu_label = "Feedback"
    menu_icon = "form"
    menu_order = MenuOrder.Feedback

    list_display = (
        "name",
        "email",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = ("name", "email", "message")
    ordering = ["-created_at"]

    inspect_view_fields = [
        "name",
        "email",
        "message",
        "remark",
        "",
        "created_at",
    ]

    inspect_view_enabled = True

    permission_helper_class = FeedbackPermission

    create_view_class = FeedbackCreateView
    edit_view_class = FeedbackEditView


    @admin.display(description="Status")
    def format_status(self, obj: Feedback):
        """
        Format status
        :param obj:
        :return:
        """
        return FeedbackStatus(obj.status).name.title()
