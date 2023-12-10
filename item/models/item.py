"""Item models"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment
from company.models import Company
from category.models import Category


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


class ItemAttachment(Attachment):
    """Attachments associated with an item"""

    class Meta:
        verbose_name = "item attachment"
        verbose_name_plural = "item attachments"
