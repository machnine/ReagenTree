"""Item models"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from attachment.models import Attachment
from core.mixins import TimeStampUserMixin

USER = settings.AUTH_USER_MODEL


class Stock(TimeStampUserMixin, models.Model):
    """Stock model for the stocks"""

    CONDITION_CHOICES = [(0, "Unknown"), (1, "Good"), (2, "Unacceptable"), (3, "Requires Attention")]

    item = models.ForeignKey("item.Item", on_delete=models.CASCADE, related_name="stocks", null=True, blank=True)
    inhouse_reagent = models.ForeignKey(
        "item.InhouseReagent", on_delete=models.CASCADE, related_name="stocks", null=True, blank=True
    )
    delivery_date = models.DateField(blank=True, null=True)
    condition = models.PositiveSmallIntegerField(choices=CONDITION_CHOICES, default=0)
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    comments = models.TextField(blank=True, null=True)

    @property
    def source(self):
        """Return the stock source (item or inhouse reagent)"""
        return self.item or self.inhouse_reagent

    @property
    def source_url(self):
        """Return the stock source url"""
        if self.item:
            return reverse("item_detail", args=[self.item.pk])
        elif self.inhouse_reagent:
            return reverse("inhouse_detail", args=[self.inhouse_reagent.pk])
        return "#"

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
        return f"{self.source.name}({self.lot_number})"

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name

    def is_validated(self):
        """Return True if the stock is validated or valiation not required"""
        if self.validations.count() > 0:
            for v in self.validations.all():
                if v.validation.status == "APPROVED" or v.validation.status == "NOT_REQUIRED":
                    return True
        return False

    @property
    def watchlist(self):
        return getattr(self, "watchlist", None)
    
    
    @property
    def storage_days(self):
        """Return the storage time of the stock"""
        return (timezone.now().date() - self.delivery_date).days


    def get_absolute_url(self):
        return reverse("stock_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.item and self.inhouse_reagent:
            raise ValidationError("Stock can only be associated with an item or a reagent")
        if self.item and (self.delivery_date is None):
            raise ValidationError("Item stock must have a delivery date")
        if self.item is None and self.inhouse_reagent is None:
            raise ValidationError("Stock must be associated with an item or a reagent")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ["-delivery_date", "item", "inhouse_reagent", "lot_number"]


class StockEntry(models.Model):
    """Stock Entry model"""

    stock = models.ForeignKey("item.Stock", on_delete=models.CASCADE, related_name="entries")
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_unit = models.ForeignKey("item.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(
        "location.Location", on_delete=models.CASCADE, related_name="stock_entries", blank=True, null=True
    )
    ordinal_number = models.PositiveIntegerField(default=1)
    in_use_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="updated_stock_units")

    def __str__(self):
        return f"{self.stock.source.name}(#{self.ordinal_number})"

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
            if self.stock.item or self.stock.inhouse_reagent:
                self.remaining_quantity = self.stock.source.quantity or 0
                self.remaining_unit = self.stock.source.quantity_unit
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("usage_qr_update", kwargs={"pk": self.pk})

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name


# stock attachments
class StockAttachment(Attachment):
    """Attachments associated with an stock"""

    uploaded_by = models.ForeignKey(USER, on_delete=models.SET_NULL, related_name="stock_attachments", null=True)
