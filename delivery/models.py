"""Delivery models."""
from django.db import models
from django.conf import settings


class Delivery(models.Model):
    """Delivery model"""

    delivery_date = models.DateField()
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Delivery on {self.delivery_date}"
