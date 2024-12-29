"""
Workshop Wagtail Hooks
"""
from django.core.handlers.asgi import ASGIRequest
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register, CreateView

from .forms import WorkshopForm
from .models import Workshop


class WorkshopCreateView(CreateView):

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

    def post(self, request: ASGIRequest, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().post(request, *args, **kwargs)
        return response

    def get_context_data(self, form=None, **kwargs):
        """

        :param form:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(form=form, **kwargs)
        # temp_form: WorkshopForm = context["form"]
        return context

    def get_form_class(self):
        """

        :return:
        """
        return WorkshopForm


@modeladmin_register
class WorkshopModelAdmin(ModelAdmin):
    model = Workshop
    base_url_path = "workshops"
    menu_label = "Workshops"
    menu_icon = "site"
    menu_order = 206
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ("title",)
    list_filter = ("location", "conference")
    search_fields = ("title", "location")
    ordering = ["title"]

    create_view_class = WorkshopCreateView

    def get_create_template(self):
        return "wagtailadmin/workshop/create.html"

    def get_edit_template(self):
        return "wagtailadmin/workshop/edit.html"
