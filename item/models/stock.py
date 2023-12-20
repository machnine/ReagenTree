"""Item models"""

from django.conf import settings
from django.db import models

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
    remaining_tests = models.PositiveSmallIntegerField(null=True, blank=True)
    remaining_volume = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    remaining_volume_unit = models.CharField(max_length=2, null=True)
    remaining_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    remaining_weight_unit = models.CharField(max_length=2, null=True)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk
            self.remaining_tests = self.item.tests or 0
            self.remaining_volume = self.item.volume or 0
            self.remaining_weight = self.item.weight or 0
            self.remaining_volume_unit = self.item.volume_unit
            self.remaining_weight_unit = self.item.weight_unit
        super().save(*args, **kwargs)

    @property
    def quantity(self) -> dict:
        return self.get_applicable_metric()

    def get_applicable_metric(self) -> dict:
        """Return the applicable metrics for the stock"""
        metrics = [
            {"name": "tests", "value": self.remaining_tests, "unit": ""},
            {
                "name": "volume",
                "value": self.remaining_volume,
                "unit": self.remaining_volume_unit,
            },
            {
                "name": "weight",
                "value": self.remaining_weight,
                "unit": self.remaining_weight_unit,
            },
        ]

        for m in metrics:
            if m["value"]:
                return m
        return {"name": "No Metric", "value": "", "unit": ""}

    def __str__(self):
        return f"[{self.ordinal_number}]{self.item.name} • {self.lot_number}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
