"""Item storage location model."""
from django.db import models

from core.mixins import TimeStampUserMixin


class Room(models.Model):
    """Room model."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return string representation of model."""
        return f"{self.name}"

    class Meta:
        """Meta class for Room model."""

        ordering = ["name"]


class Location(TimeStampUserMixin, models.Model):
    """Item storage location model."""

    name = models.CharField(max_length=100, unique=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name="locations", null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """Return string representation of model."""
        return f"{self.name}"

    @property
    def stock_items(self):
        """Return the stock items for the location."""
        stock_entries = self.stock_entries.all()
        return {stock_entry.stock for stock_entry in stock_entries if stock_entry.remaining_quantity > 0}

    class Meta:
        """Meta class for Location model."""

        ordering = ["name"]
