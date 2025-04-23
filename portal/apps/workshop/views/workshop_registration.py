"""
Workshop Registration Model Admin
"""
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin
from wagtailautocomplete.edit_handlers import AutocompletePanel

from portal.apps.workshop.models import WorkshopRegistration


class WorkshopRegistrationPermission(PermissionHelper):
    """WorkshopRegistrationPermission"""

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

    search_fields = ("workshop", "account", "account__phone_number")

    permission_helper_class = WorkshopRegistrationPermission

    custom_panels = [
        FieldPanel("workshop"),
        AutocompletePanel(field_name="account"),
    ]

    edit_handler = ObjectList(custom_panels)
