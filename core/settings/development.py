"""
Local development Django settings for core project.
"""

from .base import *  # noqa: F403, F401

# SECURITY WARNING: keep the debug turned on in development!
DEBUG = True
SECRET_KEY = "django-insecure-#q!_!"

ALLOWED_HOSTS = ["*"]
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"

# installed apps
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

# Internal IPs
INTERNAL_IPS = ["127.0.0.1"]


# Middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

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
