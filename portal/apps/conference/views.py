"""
Conference views
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.widgets import AdminDateInput

from .models import Conference


class ConferenceViewSet(ModelViewSet):
    model = Conference
    form_fields = {
        "title": None,
        "description": None,
        "start_date": AdminDateInput,
        "end_date": AdminDateInput,
        "location": None,
    }
    list_display = ["title", "description", "start_date", "end_date", "location"]
    icon = "site"
    menu_label = "Conferences"
    add_to_admin_menu = True
    copy_view_enabled = False
    inspect_view_enabled = True


conference_viewset = ConferenceViewSet(name="conferences")
