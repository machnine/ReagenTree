""" track uage of stocks """
from decimal import Decimal
from django.conf import settings
from django.db import models, transaction

from item.models.unit import Unit


class Usage(models.Model):
    """Usage model to track usage of stocks"""

    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    used_quantity = models.DecimalField(max_digits=10, decimal_places=1)
    used_date = models.DateTimeField(auto_now_add=True)
    used_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True)
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    # Method to update Stock after usage
    def save(self, *args, **kwargs):
        """Update stock after usage"""
        # Check if stock unit is valid
        if not Unit.objects.filter(symbol=self.stock.remaining_unit).exists():
            raise ValueError("Stock's remaining unit must be specified.")

        # Update remaining quantity
        if self.stock.remaining_unit != self.used_unit:
            used_quantity = self.convert_quantity(
                self.used_quantity,
                self.used_unit.symbol,
                self.stock.remaining_unit.symbol,
            )
        else:
            used_quantity = self.used_quantity

        # Use a transaction to ensure that these operations are atomic
        with transaction.atomic():
            if used_quantity <= self.stock.remaining_quantity:
                self.stock.remaining_quantity -= used_quantity
            else:
                # Optionally handle this situation (e.g., logging, user notification)
                self.stock.remaining_quantity = 0
            self.stock.save()

            super().save(*args, **kwargs)

    @classmethod
    def convert_quantity(cls, quantity, from_unit, to_unit):
        """Convert quantity from one unit to another"""
        # Conversion rates with 'ml' and 'mg' as base units
        volumes = {
            "μl": Decimal("0.001"),
            "ml": Decimal("1"),
            "dl": Decimal("10"),
            "L": Decimal("1000"),
        }
        masses = {
            "μg": Decimal("0.001"),
            "mg": Decimal("1"),
            "g": Decimal("1000"),
            "kg": Decimal("1000000"),
        }

        if from_unit in volumes and to_unit in volumes:
            return quantity * volumes[from_unit] / volumes[to_unit]
        elif from_unit in masses and to_unit in masses:
            return quantity * masses[from_unit] / masses[to_unit]
        else:
            raise ValueError("Incompatible units for conversion")
