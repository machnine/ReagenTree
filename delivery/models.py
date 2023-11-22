"""Delivery models."""
from django.conf import settings
from django.db import models


class Delivery(models.Model):
    """Delivery model"""

    delivery_date = models.DateTimeField()
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_deliveries",
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_deliveries",
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_deliveries",
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        formatted_date = self.delivery_date.strftime("%d/%m/%Y %H:%M:%S")
        return f"Received at {formatted_date} by {self.received_by.first_name} [{self.notes}]"

    class Meta:
        ordering = ["-delivery_date"]
        verbose_name_plural = "deliveries"
