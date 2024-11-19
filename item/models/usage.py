""" track uage of stocks """
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from item.models.unit import Unit

USER = settings.AUTH_USER_MODEL


class Usage(models.Model):
    """Usage model to track usage of stock entries"""

    stock_entry = models.ForeignKey("item.StockEntry", on_delete=models.CASCADE, related_name="usages")
    used_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    used_date = models.DateTimeField(auto_now_add=True)
    used_unit = models.ForeignKey("item.Unit", on_delete=models.SET_NULL, null=True)
    used_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)

    # Method to update Stock entry after usage
    def save(self, *args, **kwargs):
        """Update stock entry after usage"""

        # Check if stock entry unit is valid
        if not Unit.objects.filter(symbol=self.stock_entry.remaining_unit).exists():
            raise ValueError("Stock's remaining unit must be specified.")

        # Update remaining quantity
        if self.stock_entry.remaining_unit != self.used_unit:
            used_quantity = self.convert_quantity(
                self.used_quantity, self.used_unit.symbol, self.stock_entry.remaining_unit.symbol
            )
        else:
            used_quantity = self.used_quantity

        # Use a transaction to ensure that these operations are atomic
        with transaction.atomic():
            if used_quantity <= self.stock_entry.remaining_quantity:
                self.stock_entry.remaining_quantity -= used_quantity
            else:
                # Optionally handle this situation (e.g., logging, user notification)
                self.stock_entry.remaining_quantity = 0
            # Update in_use_date if this is the first usage
            if self.__class__.objects.filter(stock_entry=self.stock_entry).count() == 0:
                self.stock_entry.in_use_date = timezone.now().date()
            self.stock_entry.save()

            super().save(*args, **kwargs)

    @classmethod
    def convert_quantity(cls, quantity, from_unit, to_unit):
        """Convert quantity from one unit to another"""
        # Conversion rates with 'ml' and 'mg' as base units
        volumes = {"μl": Decimal("0.001"), "ml": Decimal("1"), "dl": Decimal("10"), "L": Decimal("1000")}
        masses = {"μg": Decimal("0.001"), "mg": Decimal("1"), "g": Decimal("1000"), "kg": Decimal("1000000")}

        if from_unit in volumes and to_unit in volumes:
            return quantity * volumes[from_unit] / volumes[to_unit]
        elif from_unit in masses and to_unit in masses:
            return quantity * masses[from_unit] / masses[to_unit]
        else:
            raise ValueError("Incompatible units for conversion")
