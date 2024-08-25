"""
WSGI config for portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.apps import apps
from django.conf import settings

try:
    import portal.configs.local
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.configs.dev")
except ImportError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.configs.production")

apps.populate(settings.INSTALLED_APPS)

# NOTE: Need to wait for django apps to load
from portal.main import app # noqa