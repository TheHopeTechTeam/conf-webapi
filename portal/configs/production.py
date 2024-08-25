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

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(";")

CACHES = {"default": {**env.cache(), "KEY_PREFIX": "dex-portal"}}

DATABASES = {"default": env.db()}

google_certificate_path: PosixPath = Path("/etc/secrets/google_certificate.json")
GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(google_certificate_path.read_text())
