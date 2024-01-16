"""Item models"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment
from core.mixins import TimeStampUserMixin

USER = settings.AUTH_USER_MODEL


class Item(TimeStampUserMixin, models.Model):
    """Item model the basis for all items"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cas_number = models.CharField(max_length=20, blank=True, null=True)
    product_id = models.CharField(max_length=100)
    category = models.ForeignKey(
        "category.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    quantity_unit = models.ForeignKey("item.Unit", on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(
        "company.Company", related_name="manufactured_items", on_delete=models.SET_NULL, null=True, blank=True
    )
    supplier = models.ForeignKey(
        "company.Company", related_name="supplied_items", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} [{self.product_id}]"

    @property
    def quantity_display(self):
        """Return the remaining quantity with the unit"""
        if self.quantity:
            quantity = self.quantity.normalize()
            if quantity == quantity.to_integral():
                quantity = int(quantity)
            return f"{quantity} {self.quantity_unit}"
        return f"{self.quantity} {self.quantity_unit}"

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
