"""
Location Wagtail Hooks
"""
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Testimony
from portal.libs.consts.enums import MenuOrder


class TestimonyPermission(PermissionHelper):
    """TestimonyPermission"""

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
class TestimonyModelAdmin(ModelAdmin):
    model = Testimony
    base_url_path = "testimony"
    menu_label = "Testimony"
    menu_icon = "comment"
    menu_order = MenuOrder.Testimony

    list_display = (
        "name",
        "phone_number",
        "share",
        "created_at",
    )
    list_filter = ("share",)

    search_fields = ("name", "phone_number", "message")
    ordering = ["-created_at"]

    inspect_view_fields = [
        "name",
        "phone_number",
        "share",
        "message",
        "created_at",
    ]

    inspect_view_enabled = True

    permission_helper_class = TestimonyPermission

