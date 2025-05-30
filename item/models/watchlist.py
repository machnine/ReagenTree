"""Watch list model to monitor stocks"""

from django.conf import settings
from django.db import models
from django.utils import timezone

USER = settings.AUTH_USER_MODEL


class WatchList(models.Model):
    """Watch list model to monitor stocks"""

    stock = models.OneToOneField("Stock", on_delete=models.CASCADE, related_name="watchlist")
    threshold = models.DecimalField(max_digits=10, decimal_places=1)
    threshold_type = models.CharField(max_length=1, choices=[("U", "Unit Based"), ("T", "Time Based")])
    last_checked = models.DateTimeField(null=True)
    notification = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, related_name="created_watchlists", null=True)
    acknowledged = models.DateTimeField(null=True)
    acknowledged_by = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="acknowledged_watchlists", null=True
    )

    def check_and_update(self):
        """Check the stock level and update the watch list accordingly."""
        self.last_checked = timezone.now()
        if not self.notification:
            if self.threshold_type == "U" and self.stock.remaining_stock <= self.threshold:
                self.notification = True
            elif self.threshold_type == "T" and self.stock.storage_days >= self.threshold:
                self.notification = True
        self.save()
    
    def expired_days(self):
        """Return the number of days since the last check."""
        if self.threshold_type == "T":
            return self.stock.storage_days - self.threshold
        return None

    def __str__(self):
        return f"Watch List record for <{self.stock}>"

    class Meta:
        verbose_name = "Watch List"
        verbose_name_plural = "Watch Lists"
        ordering = ["-last_checked"]
