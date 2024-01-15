"""Item models"""
from django.conf import settings
from django.db import models

from attachment.models import Attachment
from item.models.validation import StockValidation


class Stock(models.Model):
    """Stock model for the stocks"""

    CONDITION_CHOICES = [
        (0, "Unknown"),
        (1, "Good"),
        (2, "Unacceptable"),
        (3, "Requires Attention"),
    ]

    item = models.ForeignKey(
        "item.Item", on_delete=models.CASCADE, related_name="stocks"
    )
    delivery_date = models.DateField()
    condition = models.PositiveSmallIntegerField(choices=CONDITION_CHOICES, default=0)
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
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
    comments = models.TextField(blank=True, null=True)

    @property
    def validations(self):
        """Return the validation for the stock"""
        return StockValidation.objects.filter(stock=self).order_by(
            "-validation__created"
        )

    @property
    def entries(self):
        """Return the entries for the stock"""
        return StockEntry.objects.filter(stock=self)

    @property
    def is_empty(self):
        """Return True if the stock is empty"""
        if self.remaining_stock == 0:
            return True
        return False

    @property
    def remaining_stock(self):
        """Return the remaining stock"""
        remaining_stock = 0
        for entry in self.entries.all():
            remaining_stock += entry.remaining_quantity
        return remaining_stock

    def __str__(self):
        return f"{self.item.name} - {self.lot_number}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["-delivery_date", "item", "lot_number"]


class StockEntry(models.Model):
    """Stock Entry model"""

    stock = models.ForeignKey(
        "item.Stock", on_delete=models.CASCADE, related_name="entries"
    )
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=1)
    remaining_unit = models.ForeignKey(
        "item.Unit", on_delete=models.SET_NULL, null=True, blank=True
    )
    location = models.ForeignKey(
        "location.Location",
        on_delete=models.CASCADE,
        related_name="stock_entries",
        blank=True,
        null=True,
    )
    ordinal_number = models.PositiveIntegerField(default=1)
    in_use_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_stock_units",
    )

    def __str__(self):
        return f"{self.stock.item.name} - Entry {self.ordinal_number}"

    class Meta:
        unique_together = ("stock", "ordinal_number")
        verbose_name = "Stock Entry"
        verbose_name_plural = "Stock Entries"
        ordering = ["ordinal_number"]

    @property
    def remaining_quantity_display(self):
        """Return the remaining quantity with the unit"""
        if self.remaining_quantity:
            quantity = self.remaining_quantity.normalize()
            if quantity == quantity.to_integral():
                quantity = int(quantity)
            return f"{quantity} {self.remaining_unit}"
        return f"{self.remaining_quantity} {self.remaining_unit}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is not in the database yet.
            # Otherwise it would have had a pk
            self.remaining_quantity = self.stock.item.quantity or 0
            self.remaining_unit = self.stock.item.quantity_unit
        super().save(*args, **kwargs)


# stock attachments
class StockAttachment(Attachment):
    """Attachments associated with an stock"""

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="stock_attachments",
        null=True,
    )
