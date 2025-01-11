"""
Workshop Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

from portal.libs.consts.enums import MenuOrder
from .views import (
    WorkshopModelAdmin,
    WorkshopTimeSlotModelAdmin,
)


@modeladmin_register
class WorkshopModelAdminGroup(ModelAdminGroup):
    """
    Workshop Model Admin Group
    """
    menu_label = "Workshop"
    menu_icon = "date"
    menu_order = MenuOrder.Workshop
    items = (
        WorkshopTimeSlotModelAdmin,
        WorkshopModelAdmin,
    )
