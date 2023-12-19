"""Item models"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from attachment.models import Attachment
from company.models import Company
from category.models import Category


class Item(models.Model):
    """Item model the basis for all items"""

    VOLUME_UNITS = [("l", "l"), ("ml", "ml"), ("μl", "μl")]
    WEIGHT_UNITS = [("kg", "kg"), ("g", "g"), ("mg", "mg"), ("μg", "μg")]

    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    tests = models.PositiveSmallIntegerField(null=True, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volume_unit = models.CharField(
        max_length=2, choices=VOLUME_UNITS, null=True, blank=True
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight_unit = models.CharField(
        max_length=2, choices=WEIGHT_UNITS, null=True, blank=True
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

    def clean(self):
        metrics = [self.tests, self.volume, self.weight]
        if sum(value is not None for value in metrics) > 1:
            raise ValidationError(
                "Only one of 'tests', 'volume', or 'weight' can be set."
            )

    def get_applicable_metric(self):
        """Return the metrics that are applicable to the item"""
        if self.tests:
            return "tests", self.tests, ""
        if self.volume:
            return "volume", self.volume, self.volume_unit
        if self.weight:
            return "weight", self.weight, self.weight_unit
        return None, None, None

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "product_id"]


class ItemAttachment(Attachment):
    """Attachments associated with an item"""

    class Meta:
        verbose_name = "item attachment"
        verbose_name_plural = "item attachments"
