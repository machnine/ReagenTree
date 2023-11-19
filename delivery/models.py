"""Delivery models."""
from django.db import models
from django.conf import settings


class Delivery(models.Model):
    """Delivery model"""

    # Delivery condition choices
    GOOD = 1
    UNACCEPTABLE = 2
    REQUIRES_ATTENTION = 3
    DELIVERY_CONDITION_CHOICES = [
        (GOOD, "Good"),
        (UNACCEPTABLE, "Unacceptable"),
        (REQUIRES_ATTENTION, "Requires Attention"),
    ]

    delivery_date = models.DateField()
    condition = models.SmallIntegerField(choices=DELIVERY_CONDITION_CHOICES)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        condition_display = dict(self.DELIVERY_CONDITION_CHOICES).get(
            self.condition, "Unknown"
        )
        return f"Delivery on {self.delivery_date} - Condition: {condition_display}"
