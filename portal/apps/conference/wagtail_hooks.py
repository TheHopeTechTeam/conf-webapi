"""
Conference wagtail hooks
"""
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from portal.libs.consts.enums import MenuOrder
from .models import Conference


@modeladmin_register
class ConferenceModelAdmin(ModelAdmin):
    """
    Conference Model Admin
    """
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_removed=False)

    model = Conference
    base_url_path = "conferences"
    menu_label = "Conferences"
    menu_icon = "site"
    menu_order = MenuOrder.Conference

    list_display = ("title", "start_date", "end_date", "location")
    list_filter = ("location",)

    search_fields = ("title", "location")

    inspect_view_fields = [
        "title",
        "description",
        "start_date",
        "end_date",
        "location",
        "instructors",
    ]
    inspect_view_fields_exclude = ["is_removed"]
    inspect_view_enabled = True

    custom_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("location"),
        FieldPanel(
            field_name="instructors",
            help_text=format_html(
                "Multiple instructors can be selected by holding down the <strong>Ctrl (Windows)</strong> "
                "or <strong>⌘ (Mac)</strong> and clicking on the instructors."
            )
        ),
    ]

    edit_handler = ObjectList(custom_panels)
