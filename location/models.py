"""Item storage location model."""
from django.conf import settings
from django.db import models


class Location(models.Model):
    """Item storage location model."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_locations",
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_locations",
    )

    def __str__(self):
        """Return string representation of model."""
        return f"{self.name}"

    class Meta:
        """Meta class for Location model."""

        ordering = ["name"]
