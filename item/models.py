"""Item models"""

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
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
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_items",
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_items",
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
