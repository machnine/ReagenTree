""" Company models"""
from django.db import models

from core.mixins import TimeStampUserMixin


class Company(TimeStampUserMixin):
    """Company model"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        """Return name of company"""
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
