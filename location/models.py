"""Item storage location model."""
from django.db import models


class Location(models.Model):
    """Item storage location model."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """Return string representation of model."""
        return f"{self.name}"
