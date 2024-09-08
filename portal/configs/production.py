"""
Configuration for production environment.
"""
from .base import *

DEBUG = env("DJANGO_DEBUG", default=False)

# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if env("DJANGO_SECRET_KEY", default=None):
    SECRET_KEY = env("DJANGO_SECRET_KEY")
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print(
        "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
    )
    from django.core.management.utils import get_random_secret_key

    SECRET_KEY = get_random_secret_key()
