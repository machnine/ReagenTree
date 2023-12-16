"""Item models"""

from django.conf import settings
from django.db import models
from django.utils import timezone

from delivery.models import Delivery
from location.models import Location

from .item import Item


class StockItem(models.Model):
    """StockItem model for the stock items"""

    CONDITION_CHOICES = [
        (0, "Unknown"),
        (1, "Good"),
        (2, "Unacceptable"),
        (3, "Requires Attention"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stockitems")
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="stockitems", null=True
    )
    delivery_condition = models.PositiveSmallIntegerField(
        choices=CONDITION_CHOICES, default=0
    )
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="stockitems",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
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

    def __str__(self):
        return f"{self.item.name} - {self.lot_number}"
