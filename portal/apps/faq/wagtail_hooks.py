"""
FAQ Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

from .views import FaqCategoryModelAdmin, FaqModelAdmin


@modeladmin_register
class FaqModelAdminGroup(ModelAdminGroup):
    """
    FAQ Model Admin Group
    """
    menu_label = "FAQ"
    menu_icon = "folder-open-inverse"

    items = (
        FaqCategoryModelAdmin,
        FaqModelAdmin,
    )

