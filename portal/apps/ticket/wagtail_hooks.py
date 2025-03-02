"""
Ticket Wagtail Hooks
"""
from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

from .views import (
    TicketAdmin,
    TicketRegisterDetailAdmin,
    TicketTypeAdmin,
)
from portal.libs.consts.enums import MenuOrder


@modeladmin_register
class TicketModelAdmin(ModelAdminGroup):
    """
    Ticket Model Admin
    """
    menu_label = "Tickets"
    menu_icon = "folder"
    menu_order = MenuOrder.Ticket
    items = (
        TicketTypeAdmin,
        TicketAdmin,
        TicketRegisterDetailAdmin,
    )
