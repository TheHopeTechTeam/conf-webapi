"""
Workshop Registration Model Admin
"""
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.workshop.models import WorkshopRegistration


class WorkshopRegistrationPermission(PermissionHelper):
    """WorkshopRegistrationPermission"""

    def user_can_create(self, user):
        """

        :param user:
        :return:
        """
        return False

    def user_can_edit_obj(self, user, obj):
        """

        :param user:
        :param obj:
        :return:
        """
        return False

    def user_can_copy_obj(self, user, obj):
        """

        :param user:
        :param obj:
        :return:
        """
        return False


class WorkshopRegistrationModelAdmin(ModelAdmin):
    """Workshop Model Admin"""
    model = WorkshopRegistration
    base_url_path = "workshop-registration"
    menu_label = "Workshop Registration"
    menu_icon = "date"

    list_display = (
        "workshop",
        "account",
        "registered_at",
    )
    list_filter = (
        "workshop",
    )

    search_fields = ("workshop", "account")

    permission_helper_class = WorkshopRegistrationPermission
