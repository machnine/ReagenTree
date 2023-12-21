"""Item models"""
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


from delivery.models import Delivery
from location.models import Location

from .item import Item


class Stock(models.Model):
    """Stock model for the stocks"""

    CONDITION_CHOICES = [
        (0, "Unknown"),
        (1, "Good"),
        (2, "Unacceptable"),
        (3, "Requires Attention"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stocks")
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=1)
    remaining_quantity_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="stocks", null=True
    )
    delivery_condition = models.PositiveSmallIntegerField(
        choices=CONDITION_CHOICES, default=0
    )
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="stocks",
        blank=True,
        null=True,
    )
    created = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_stock",
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_stock",
    )
    ordinal_number = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would have a pk
            self.remaining_quantity = self.item.quantity or 0
            # set the same created timestamp for stocks created in bulk
            # remove the microseconds from the timestamp
            dt = timezone.now()
            self.created = dt - timedelta(microseconds=dt.microsecond)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.ordinal_number}]{self.item.name} • {self.lot_number}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
