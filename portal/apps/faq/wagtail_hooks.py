"""
FAQ Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

from .views import FaqCategoryModelAdmin, FaqModelAdmin
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class FaqModelAdminGroup(ModelAdminGroup):
    """
    FAQ Model Admin Group
    """
    menu_label = "FAQ"
    menu_order = MenuOrder.FAQ
    menu_icon = "folder-open-inverse"

    items = (
        FaqCategoryModelAdmin,
        FaqModelAdmin,
    )

