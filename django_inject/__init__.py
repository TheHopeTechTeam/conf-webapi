"""
Inject Django into the current process.
"""
import os

from django.apps import apps
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.configs.dev")
apps.populate(settings.INSTALLED_APPS)

__all__ = [
    "settings"
]
