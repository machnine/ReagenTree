"""Item storage location model."""
from django.db import models

from core.mixins import TimeStampUserMixin


class Location(TimeStampUserMixin, models.Model):
    """Item storage location model."""

    ROOM_CHOICES = [
        (0, "Unknown"),
        (1, "Main Lab"),
        (2, "Gel Lab"),
        (3, "Cold Room"),
        (4, "Freezer Room"),
        (5, "FACS Lab"),
        (6, "Store Room"),
        (7, "Wash Room"),
    ]
    name = models.CharField(max_length=100, unique=True)
    room = models.PositiveSmallIntegerField(choices=ROOM_CHOICES, default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        """Return string representation of model."""
        return f"{self.name}"

    @property
    def room_name(self):
        """Return the room name."""
        room_dict = dict(self.ROOM_CHOICES)
        return room_dict.get(self.room)

    @property
    def stock_items(self):
        """Return the stock items for the location."""
        stock_entries = self.stock_entries.all()
        return {stock_entry.stock for stock_entry in stock_entries if stock_entry.remaining_quantity > 0}

    class Meta:
        """Meta class for Location model."""

        ordering = ["name"]
