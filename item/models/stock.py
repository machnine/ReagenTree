"""Item models"""
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Stock(models.Model):
    """Stock model for the stocks"""

    CONDITION_CHOICES = [
        (0, "Unknown"),
        (1, "Good"),
        (2, "Unacceptable"),
        (3, "Requires Attention"),
    ]

    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="stocks")
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=1)
    remaining_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True)
    delivery_date = models.DateTimeField(null=True, blank=True)  # for now
    delivery_condition = models.PositiveSmallIntegerField(
        choices=CONDITION_CHOICES, default=0
    )
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    location = models.ForeignKey(
        "location.Location",
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
    total_count = models.PositiveIntegerField(
        default=1
    )  # total number of stocks created in bulk
    in_use_date = models.DateField(blank=True, null=True)

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

    @property
    def remaining_quantity_display(self):
        """Return the remaining quantity with the unit"""
        if self.remaining_quantity:
            quantity = self.remaining_quantity.normalize()
            if quantity == quantity.to_integral():
                quantity = int(quantity)
            return f"{quantity} {self.remaining_unit}"
        return f"{self.remaining_quantity} {self.remaining_unit}"

    @property
    def validations(self):
        """Return the validation for the stock"""
        return StockValidation.objects.filter(stock=self)

    def __str__(self):
        return f"[{self.ordinal_number}]{self.item.name} • {self.lot_number}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["-created", "-ordinal_number"]


class StockValidation(models.Model):
    """model tracking stock validations"""

    stock = models.ForeignKey(
        "Stock", on_delete=models.CASCADE, related_name="validations"
    )
    validation = models.ForeignKey("ReagentValidation", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("stock", "validation")
