"""Category models."""
from django.db import models

from core.mixins import TimeStampUserMixin


class Category(TimeStampUserMixin):
    """Category model."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return category name."""
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
