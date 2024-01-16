""" Item model mixins """
from django.db import models


class QuantityDisplayMixin(models.Model):
    """Mixin to store and display quantity and unit"""

    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    quantity_unit = models.ForeignKey("item.Unit", on_delete=models.SET_NULL, null=True)

    @property
    def quantity_display(self):
        """Return the quantity with unit"""
        unit = self.quantity_unit or ""
        quantity = self.quantity or ""
        if quantity:
            quantity = quantity.normalize()
            if quantity == quantity.to_integral():
                quantity = int(quantity)
        return f"{quantity} {unit}"

    class Meta:
        abstract = True
