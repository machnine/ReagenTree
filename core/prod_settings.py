"""
Django production settings for core project.
"""
from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["reagentree.oxfordgenes.com", "212.71.238.112"]

# CSRF settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_TRUSTED_ORIGINS = [
    "http://reagentree.oxfordgenes.com",
    "https://reagentree.oxfordgenes.com",
]

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
