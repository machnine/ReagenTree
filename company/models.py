""" Company models"""
from django.conf import settings
from django.db import models


class Company(models.Model):
    """Company model"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_companies"
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="updated_companies"
    )
    website = models.URLField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        """Return name of company"""
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
