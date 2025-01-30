"""
Settings for production.
"""

import os

from .settings import *


SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]] if "WEBSITE_HOSTNAME" in os.environ else []
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["AZURE_POSTGRESQL_NAME"],
        "HOST": os.environ["AZURE_POSTGRESQL_HOST"],
        "USER": os.environ["AZURE_POSTGRESQL_USER"],
        "PASSWORD": os.environ["AZURE_POSTGRESQL_PASSWORD"],
    }
}
