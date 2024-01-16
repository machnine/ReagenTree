"""Item models"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment
from core.mixins import TimeStampUserMixin
from item.mixins import QuantityDisplayMixin

USER = settings.AUTH_USER_MODEL


class Item(TimeStampUserMixin, QuantityDisplayMixin, models.Model):
    """Item model the basis for all items"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cas_number = models.CharField(max_length=20, blank=True, null=True)
    product_id = models.CharField(max_length=100)
    category = models.ForeignKey(
        "category.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    manufacturer = models.ForeignKey(
        "company.Company", related_name="manufactured_items", on_delete=models.SET_NULL, null=True, blank=True
    )
    supplier = models.ForeignKey(
        "company.Company", related_name="supplied_items", on_delete=models.SET_NULL, null=True, blank=True
    )

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.name} [{self.product_id}]"

    @property
    def remaining_stock(self):
        """Return the remaining stock"""
        remaining_stock = 0
        for stock in self.stocks.all():
            remaining_stock += stock.remaining_stock
        return remaining_stock

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "product_id"]


class ItemAttachment(Attachment):
    """Attachments associated with an item"""

    uploaded_by = models.ForeignKey(USER, on_delete=models.SET_NULL, related_name="item_attachments", null=True)
