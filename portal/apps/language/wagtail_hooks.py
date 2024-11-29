"""
Language Wagtail Hooks
"""
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import Language


@modeladmin_register
class LanguageModelAdmin(ModelAdmin):
    model = Language
    base_url_path = "languages"
    menu_label = "Languages"
    menu_icon = "site"
    menu_order = 201
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")
    ordering = ["name"]

    _help_test = mark_safe(
        """
        <a target="_blank" href="http://www.lingoes.net/en/translator/langcode.htm">Click here to find the language code and name</a>.
        """
    )

    custom_panels = [
        FieldPanel(field_name="name", help_text=_help_test),
        FieldPanel(field_name="code", help_text=_help_test),
        FieldPanel(field_name="is_active"),
    ]
    edit_handler = ObjectList(custom_panels)
