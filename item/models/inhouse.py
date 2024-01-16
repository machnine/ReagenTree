"""define inhouse reagent model and it's associated helper models"""

from django.db import models

from core.mixins import TimeStampUserMixin


class InhouseReagent(TimeStampUserMixin):
    """Inhouse reagent model"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    product_id = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=50)
    components = models.ManyToManyField("item.Stock", through="item.ReagentComponent", related_name="inhouse_reagents")

    def __str__(self):
        """Return string representation of the object"""
        return f"{self.name} ({self.product_id} - {self.lot_number})"

    class Meta:
        unique_together = ["product_id", "lot_number"]


class ReagentComponent(models.Model):
    """Inhouse reagent component model"""

    reagent = models.ForeignKey(InhouseReagent, on_delete=models.CASCADE)
    stock = models.ForeignKey("item.Stock", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    quantity_unit = models.ForeignKey("item.Unit", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """Return string representation of the object"""
        return f"{self.stock} ({self.quantity} {self.quantity_unit})"

    @property
    def quantity_display(self):
        """Return the remaining quantity with the unit"""
        if self.quantity:
            quantity = self.quantity.normalize()
            if quantity == quantity.to_integral():
                quantity = int(quantity)
            return f"{quantity} {self.quantity_unit}"
        return f"{self.quantity} {self.quantity_unit}"
