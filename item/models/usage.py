""" track uage of stocks """
from django.conf import settings
from django.db import models
from item.models import Stock


class Usage(models.Model):
    """Usage model to track usage of stocks"""

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    used_quantity = models.DecimalField(max_digits=10, decimal_places=1)
    used_date = models.DateTimeField(auto_now_add=True)
    used_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True)
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    # Method to update Stock after usage
    def save(self, *args, **kwargs):
        """Update stock after usage"""
        if self.used_quantity <= self.stock.remaining_quantity:
            self.stock.remaining_quantity -= self.used_quantity

        self.stock.save()
        super().save(*args, **kwargs)
