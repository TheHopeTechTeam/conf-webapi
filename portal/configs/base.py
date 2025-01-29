"""
Django settings for portal project.

Generated by "django-admin startproject" using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import json
import os
from pathlib import Path, PosixPath

import environ
from google.oauth2 import service_account

env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, None),
    DJANGO_SECURE_SSL_REDIRECT=(str, "off"),
    DJANGO_ALLOWED_HOSTS=(str, "*"),
    DATABASE_URL=(str, "postgres://none"),
    CACHE_URL=(str, "rediscache://none")
)  # set default values and casting
# Set the project base directory
PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent
# BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ENV: str = env(var="ENV", default="dev")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c46c63fqn26&64=#iq@t=fg8=uxknk24y7ifo+h)nqmf2n^ec@"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env("DEBUG")

# ------------------------------------------------------------------------------
# Environment variables

APP_NAME: str = "conf-webapi"

REDIS_URL: str = env(var="REDIS_URL", default="redis://localhost:6379/0")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# [CORS]
CORS_ALLOWED_ORIGINS: list = env("CORS_ALLOWED_ORIGINS", default="*").split(",")
CORS_ALLOW_ORIGINS_REGEX: str = env("CORS_ALLOW_ORIGINS_REGEX", default=None)

# [Database]
DATABASE_HOST: str = env("DATABASE_HOST", default="localhost")
DATABASE_USER: str = env("DATABASE_USER", default="postgres")
DATABASE_PASSWORD: str = env("DATABASE_PASSWORD", default="")
DATABASE_PORT: str = env("DATABASE_PORT", default="5432")
DATABASE_NAME: str = env("DATABASE_NAME", default="postgres")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": DATABASE_HOST,
        "NAME": DATABASE_NAME,
        "PASSWORD": DATABASE_PASSWORD,
        "PORT": f"{DATABASE_PORT}",
        "USER": DATABASE_USER,
        "TEST": {
            "NAME": DATABASE_NAME
        }
    }
}

# [Django]
# [[Cross Site Request Forgery]]
env_csrf_trusted_origins = env("CSRF_TRUSTED_ORIGINS", default=None)
CSRF_COOKIE_DOMAIN: str = env("CSRF_COOKIE_DOMAIN", default=None)
CSRF_TRUSTED_ORIGINS: list = env_csrf_trusted_origins.split(",") if env_csrf_trusted_origins else []

# [Google Cloud]
## Set the default storage settings if the Google Cloud credentials are available using the GOOGLE_APPLICATION_CREDENTIALS environment variable.
DEFAULT_STORAGE = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
}
FIREBASE_STORAGE_LOCATION: str = APP_NAME
try:
    path = "env/google_certificate.json"
    google_certificate_path: PosixPath = Path(path)
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path)
    GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(google_certificate_path.read_text())
    FIREBASE_STORAGE_BUCKET: str = f"{GS_CREDENTIALS.project_id}.appspot.com"
    DEFAULT_STORAGE = {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": FIREBASE_STORAGE_BUCKET,
            "location": FIREBASE_STORAGE_LOCATION,
            "credentials": GS_CREDENTIALS,
        },
    }
except FileNotFoundError:
    path = "/etc/secrets/google_certificate.json"
    google_certificate_path: PosixPath = Path(path)
    try:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path)
        GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(google_certificate_path.read_text())
        FIREBASE_STORAGE_BUCKET: str = f"{GS_CREDENTIALS.project_id}.appspot.com"
        DEFAULT_STORAGE = {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": FIREBASE_STORAGE_BUCKET,
                "location": FIREBASE_STORAGE_LOCATION,
                "credentials": GS_CREDENTIALS,
            },
        }
    except Exception as e:
        from logging import getLogger

        logger = getLogger(APP_NAME)
        logger.warning(f"Failed to load Google Firebase certificate: {e}")
        GOOGLE_FIREBASE_CERTIFICATE = {}
        FIREBASE_STORAGE_BUCKET = ""

# ------------------------------------------------------------------------------

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # wegtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "wagtail_modeladmin",
    # wagtail end
    # auditlog
    "auditlog",
    # apps
    "portal.apps.account",
    "portal.apps.conference",
    "portal.apps.event_info",
    "portal.apps.faq",
    "portal.apps.feedback",
    "portal.apps.home",
    "portal.apps.instructor",
    "portal.apps.language",
    "portal.apps.location",
    "portal.apps.search",
    "portal.apps.testimony",
    "portal.apps.ticket",
    "portal.apps.workshop"
    # apps end
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # wagtail
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # auditlog
    "auditlog.middleware.AuditlogMiddleware",
]

ROOT_URLCONF = "portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "portal.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if ENV != "prod" else "INFO",
    },
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": DEFAULT_STORAGE,
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
    # "staticfiles": {
    #     "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    # },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Wagtail settings

WAGTAIL_SITE_NAME = "The Hope Conference Portal"
WAGTAILADMIN_BASE_URL = "/cms"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']

# Wagtail file size limits
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 2.5 * 1024 * 1024  # 2.5MB

# Auditlog settings
AUDITLOG_TWO_STEP_MIGRATION = True
AUDITLOG_USE_TEXT_CHANGES_IF_JSON_IS_NOT_PRESENT = True
