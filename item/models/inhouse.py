"""define inhouse reagent model and it's associated helper models"""

from django.db import models

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
    
    def get_class_name(self):
        return self.__class__.__name__

    class Meta:
        unique_together = ["product_id", "lot_number"]


class ReagentComponent(QuantityDisplayMixin, models.Model):
    """Inhouse reagent component model"""

    reagent = models.ForeignKey(InhouseReagent, on_delete=models.CASCADE)
    stock = models.ForeignKey("item.Stock", on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the object"""
        return f"{self.stock} ({self.quantity_display})"
