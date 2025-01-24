"""
Workshop Model Admin
"""
from django.core.handlers.asgi import ASGIRequest
from wagtail.admin.panels import FieldPanel, ObjectList
from wagtail_modeladmin.options import ModelAdmin
from wagtail_modeladmin.views import CreateView

from portal.apps.workshop.forms import WorkshopForm
from portal.apps.workshop.models import Workshop


class WorkshopCreateView(CreateView):
    """
    Workshop Create View
    Note: This class temporary not used
    """

    def get(self, request: ASGIRequest, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().get(request, *args, **kwargs)
        response.headers["Cache-Control"] = "no-cache"
        return response

    def get_form_class(self):
        """

        :return:
        """
        return WorkshopForm


class WorkshopModelAdmin(ModelAdmin):
    """Workshop Model Admin"""
    model = Workshop
    base_url_path = "workshops"
    menu_label = "Workshops"
    menu_icon = "site"

    list_display = ("title", "location", "time_slot")
    list_filter = ("location", "conference")

    search_fields = ("title", "location")
    ordering = ["title"]

    custom_panels = [
        FieldPanel("title"),
        FieldPanel("conference"),
        FieldPanel("location"),
        FieldPanel("instructor"),
        FieldPanel("time_slot"),
        FieldPanel("participants_limit"),
        FieldPanel("image"),
        FieldPanel("description"),
        FieldPanel("slido_url"),
    ]

    edit_handler = ObjectList(custom_panels)

    # create_view_class = WorkshopCreateView
    #
    # def get_create_template(self):
    #     return "wagtailadmin/workshop/create.html"
    #
    # def get_edit_template(self):
    #     return "wagtailadmin/workshop/edit.html"
