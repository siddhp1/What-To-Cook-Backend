"""
Settings for production.
"""

import os

from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]] if "WEBSITE_HOSTNAME" in os.environ else []
CSRF_TRUSTED_ORIGINS = (
    ["https://" + os.environ["WEBSITE_HOSTNAME"]] if "WEBSITE_HOSTNAME" in os.environ else []
)
DEBUG = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": "media",
            "connection_string": os.environ["STORAGE_CONNECTION_STRING"],
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["AZURE_POSTGRESQL_NAME"],
        "HOST": os.environ["AZURE_POSTGRESQL_HOST"],
        "USER": os.environ["AZURE_POSTGRESQL_USER"],
        "PASSWORD": os.environ["AZURE_POSTGRESQL_PASSWORD"],
    }
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = os.environ["MEDIA_URL"]
MEDIA_ROOT = BASE_DIR / "media"
