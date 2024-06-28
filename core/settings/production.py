"""
Django production settings for core project.
"""

import os

from .base import *  # noqa: F403, F401

DEBUG = False

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY")

# Allowed hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# CSRF settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 15  # 15 minutes
SESSION_COOKIE_SECURE = True

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {"class": "logging.FileHandler", "filename": os.getenv("DJANGO_LOG", "debug.log")},
    },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": "WARNING"},
    },
}
