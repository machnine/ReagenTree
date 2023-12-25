"""Delivery models."""
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

from attachment.models import Attachment


class Delivery(models.Model):
    """Delivery model"""

    delivery_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_deliveries",
    )
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_deliveries",
    )
    notes = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        formatted_date = self.delivery_date.strftime("%d/%m/%Y %H:%M:%S")
        return f"Received at {formatted_date} by {self.received_by.first_name} [{self.notes}]"

    @property
    def total_items(self):
        """Return the total number of items in the delivery."""
        return self.stocks.count()

    @property
    def within_one_week(self) -> bool:
        """Return True if the delivery was received within the last week."""
        return self.delivery_date > timezone.now() - timedelta(days=7)

    class Meta:
        ordering = ["-delivery_date"]
        verbose_name = "delivery"
        verbose_name_plural = "deliveries"


class DeliveryAttachment(Attachment):
    """Attachments associated with a delivery"""

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="delivery_attachments",
        null=True,
    )

    class Meta:
        verbose_name = "delivery attachment"
        verbose_name_plural = "delivery attachments"
