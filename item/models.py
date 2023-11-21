"""Item models"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from company.models import Company
from category.models import Category
from delivery.models import Delivery
from location.models import Location


class Item(models.Model):
    """Item model the basis for all items"""

    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    manufacturer = models.ForeignKey(
        Company,
        related_name="manufactured_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    supplier = models.ForeignKey(
        Company,
        related_name="supplied_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "product_id"]


class StockItem(models.Model):
    """StockItem model for the stock items"""

    CONDITION_CHOICES = [
        (0, "Unknown"),
        (1, "Good"),
        (2, "Unacceptable"),
        (3, "Requires Attention"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stock_items")
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="stock_items", null=True
    )
    delivery_condition = models.PositiveSmallIntegerField(
        choices=CONDITION_CHOICES, default=0
    )
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField(
        validators=[MinValueValidator(timezone.now().date())]
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="stock_items",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.item.name} - {self.lot_number}"
