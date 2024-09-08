"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
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
from portal.main import app  # noqa
