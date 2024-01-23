"""Item storage location model."""
from django.db import models
from django.urls import reverse

from core.mixins import TimeStampUserMixin


class Room(models.Model):
    """Room model."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return string representation of model."""
        return f"{self.name}"

    class Meta:
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

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name
    
    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["name"]
