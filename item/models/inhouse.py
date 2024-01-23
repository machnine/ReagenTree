"""define inhouse reagent model and it's associated helper models"""

from django.db import models
from django.urls import reverse

from core.mixins import TimeStampUserMixin
from item.mixins import QuantityDisplayMixin


class InhouseReagent(TimeStampUserMixin, QuantityDisplayMixin, models.Model):
    """Inhouse reagent model"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "category.Category", on_delete=models.SET_NULL, null=True, related_name="inhouse_reagents"
    )
    product_id = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    components = models.ManyToManyField("item.Stock", through="item.ReagentComponent", related_name="inhouse_reagents")

    def __str__(self):
        """Return string representation of the object"""
        return f"{self.name} ({self.product_id} - {self.lot_number})"

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name
    
    def get_absolute_url(self):
        return reverse("inhouse_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Inhouse reagents"
        verbose_name = "Inhouse reagent"
        unique_together = ["product_id", "lot_number"]
        ordering = ["name"]


class ReagentComponent(QuantityDisplayMixin, models.Model):
    """Inhouse reagent component model"""

    reagent = models.ForeignKey(InhouseReagent, on_delete=models.CASCADE)
    stock = models.ForeignKey("item.Stock", on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the object"""
        return f"{self.stock} ({self.quantity_display})"
