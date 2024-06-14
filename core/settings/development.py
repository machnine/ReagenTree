"""
Local development Django settings for core project.
"""

from .base import *

# SECURITY WARNING: keep the debug turned on in development!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Overriding database settings, if necessary
# DATABASES = ...

# Local development static and media files handling
# STATICFILES_DIRS, MEDIA_ROOT, etc. can be adjusted if needed

# Ensure CSRF and Session cookies work correctly in development
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# You might want to disable these for local development
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"

# Logging for development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    },
}


INSTALLED_APPS += ["django_extensions"]
