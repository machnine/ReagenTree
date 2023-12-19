""" track uage of stock items """
from django.conf import settings
from django.db import models
from item.models import StockItem


class Usage(models.Model):
    """Usage model to track usage of stock items"""
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    used_tests = models.PositiveIntegerField(default=0)
    used_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    used_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_date = models.DateTimeField(auto_now_add=True)
    usage_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    # Method to update StockItem after usage
    def save(self, *args, **kwargs):
        if self.used_tests:
            self.stock_item.remaining_tests -= self.used_tests
        if self.used_volume:
            self.stock_item.remaining_volume -= self.used_volume
        if self.used_weight:
            self.stock_item.remaining_weight -= self.used_weight
        self.stock_item.save()
        super().save(*args, **kwargs)
