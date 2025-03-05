"""
Location Wagtail Hooks
"""
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Feedback
from portal.libs.consts.enums import MenuOrder


class FeedbackPermission(PermissionHelper):
    """FeedbackPermission"""

    def user_can_create(self, user):
        """
        User can create obj
        :param user:
        :return:
        """
        return False

    def user_can_edit_obj(self, user, obj):
        """
        User can edit obj
        :param user:
        :param obj:
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
        "created_at",
    )

    search_fields = ("name", "email", "message")
    ordering = ["-created_at"]

    inspect_view_fields = [
        "name",
        "email",
        "message",
        "created_at",
    ]

    inspect_view_enabled = True

    permission_helper_class = FeedbackPermission

