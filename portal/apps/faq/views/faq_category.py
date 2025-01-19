"""
FAQ Category Model Admin
"""
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin

from portal.apps.faq.models import FaqCategory
from portal.libs.mixins.orderable_mixin import OrderableMixin


class FaqCategoryModelAdmin(OrderableMixin, ModelAdmin):
    model = FaqCategory
    menu_label = "FAQ Categories"
    menu_icon = "tag"

    list_display = ("name", "description")
    list_filter = ("created_at",)

    search_fields = ("name", "description")
    ordering = ("sort_order",)

    custom_panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    edit_handler = ObjectList(custom_panels)
