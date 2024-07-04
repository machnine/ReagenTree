"""This file is used to configure the app name for the requestlog app."""

from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "requestlog"
