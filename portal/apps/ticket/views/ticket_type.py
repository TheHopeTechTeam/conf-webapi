"""
Ticket Type Wagtail Model Admin
"""
from wagtail.admin.panels import ObjectList, FieldPanel
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.ticket.models import TicketType


class TicketTypeAdmin(ModelAdmin):
    """
    Ticket Type Admin
    """
    model = TicketType
    menu_label = "Ticket Types"
    menu_icon = "tag"
    list_display = ("name", "description")
    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    search_fields = ("name",)
    ordering = ["name"]

    base_url_path = "ticket_types"

    custom_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]
    edit_handler = ObjectList(custom_panels)
