""" track uage of stocks """
from django.conf import settings
from django.db import models
from item.models import Stock


class Usage(models.Model):
    """Usage model to track usage of stocks"""

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    used_tests = models.PositiveIntegerField(default=0)
    used_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    used_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_date = models.DateTimeField(auto_now_add=True)
    usage_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    # Method to update Stock after usage
    def save(self, *args, **kwargs):
        """Update stock after usage"""
        if self.used_tests <= self.stock.remaining_tests:
            self.stock.remaining_tests -= self.used_tests
        if self.used_volume <= self.stock.remaining_volume:
            self.stock.remaining_volume -= self.used_volume
        if self.used_weight <= self.stock.remaining_weight:
            self.stock.remaining_weight -= self.used_weight

        self.stock.save()
        super().save(*args, **kwargs)
