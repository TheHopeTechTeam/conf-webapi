"""
Ticket Model Admin
"""
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.ticket.models import Ticket


class TicketAdmin(ModelAdmin):
    """
    Ticket Admin
    """
    model = Ticket
    menu_label = "Tickets"
    menu_icon = "tag"
    list_display = ("title", "ticket_type", "conference")

    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    search_fields = ("title", "ticket_type__name", "conference__name")
    ordering = ["title"]

    custom_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("ticket_type"),
        FieldPanel("conference"),
    ]

    edit_handler = ObjectList(custom_panels)
