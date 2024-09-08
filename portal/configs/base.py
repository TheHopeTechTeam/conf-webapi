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

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c46c63fqn26&64=#iq@t=fg8=uxknk24y7ifo+h)nqmf2n^ec@"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []

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
    # wagtail end
    # apps
    "portal.apps.account",
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
    # wagtail end
]

ROOT_URLCONF = "portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Wagtail settings
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

WAGTAIL_SITE_NAME = "The Hope Conference Portal"
WAGTAILADMIN_BASE_URL = "/cms"


# ------------------------------------------------------------------------------
# Environment variables

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

# [Google Cloud]
try:
    google_certificate_path: PosixPath = Path("env/google_certificate.json")
    GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(google_certificate_path.read_text())
except Exception:
    google_certificate_path: PosixPath = Path("/etc/secrets/google_certificate.json")
    GOOGLE_FIREBASE_CERTIFICATE: dict = json.loads(google_certificate_path.read_text())
