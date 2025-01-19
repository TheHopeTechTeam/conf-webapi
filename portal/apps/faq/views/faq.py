"""
FAQ Model Admin
"""
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.faq.models import Faq
from portal.libs.mixins.orderable_mixin import OrderableMixin


class FaqModelAdmin(OrderableMixin, ModelAdmin):
    model = Faq
    menu_label = "FAQs"
    menu_icon = "help"

    list_display = ("question", "category", "answer", "related_link")
    list_filter = ("category", "created_at")

    search_fields = ("question", "answer")
    ordering = ("sort_order",)

    custom_panels = [
        FieldPanel("category"),
        FieldPanel("question"),
        FieldPanel("answer"),
        FieldPanel("related_link"),
    ]

    edit_handler = ObjectList(custom_panels)
