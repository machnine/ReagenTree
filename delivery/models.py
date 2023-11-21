"""Delivery models."""
from django.db import models
from django.conf import settings


class Delivery(models.Model):
    """Delivery model"""

    delivery_date = models.DateTimeField()
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        formatted_date = self.delivery_date.strftime("%d/%m/%Y %H:%M:%S")
        return f"Received at {formatted_date} by {self.received_by.first_name}"

    class Meta:
        ordering = ["-delivery_date"]
        verbose_name_plural = "deliveries"
