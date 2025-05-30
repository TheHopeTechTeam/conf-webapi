"""
Ticket Model Admin
"""
from django.contrib import admin
from django.utils.html import format_html
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
    list_display = (
        "title",
        "ticket_type",
        "conference",
        "format_color",
    )

    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    search_fields = ("title", "ticket_type__name", "conference__name")
    ordering = ["title"]

    _help_text = format_html(
        "Color in hex format. e.g. #FFFFFF for white. "
        "Visit <a href='https://www.w3schools.com/colors/colors_picker.asp' target='_blank'>HTML Color Picker</a> for choosing a color."
    )
    custom_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("ticket_type"),
        FieldPanel("conference"),
        FieldPanel(
            field_name="text_color",
            help_text=_help_text,
            attrs={"placeholder": "#FFFFFF"},
        ),
        FieldPanel(
            field_name="background_color",
            help_text=_help_text,
            attrs={"placeholder": "#FFFFFF"},
        ),
    ]

    edit_handler = ObjectList(custom_panels)

    @admin.display(description="Color")
    def format_color(self, obj):
        """
        Format text color
        """
        if not obj.text_color and not obj.background_color:
            return "N/A"
        if obj.text_color and not obj.background_color:
            return format_html(
                f'<span style="color: {obj.text_color};">'
                f'{obj.text_color}'
                f'</span>'
            )
        if not obj.text_color and obj.background_color:
            return format_html(
                f'<span style="background-color: {obj.background_color}; border-radius: 5px; padding: 5px;">'
                f'{obj.background_color}'
                f'</span>'
            )
        return format_html(
            f'<span style="color: {obj.text_color}; background-color: {obj.background_color}; border-radius: 5px; padding: 5px;">'
            f'text color: {obj.text_color}, background color: {obj.background_color}'
            f'</span>'
        )
