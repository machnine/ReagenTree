""" Reagent validation workflow tracking """

from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class ReagentValidation(models.Model):
    """Reagent validation workflow tracking"""

    VALIDATION_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("NOT_REQUIRED", "Not Required"),
    )

    status = models.CharField(max_length=15, choices=VALIDATION_CHOICES, default="PENDING")
    created_by = models.ForeignKey(USER, related_name="validator", on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    authorised_by = models.ForeignKey(USER, on_delete=models.SET_NULL, blank=True, null=True, related_name="authoriser")
    authorised = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.status} - {self.created_by} - {self.created}"

    class Meta:
        ordering = ["-created"]


# specific validation models
class StockValidation(models.Model):
    """model tracking stock validations"""

    validation = models.ForeignKey(ReagentValidation, on_delete=models.CASCADE)
    stock = models.ForeignKey("item.Stock", on_delete=models.CASCADE, related_name="validations")

    class Meta:
        unique_together = ("stock", "validation")
        ordering = ["-validation__created"]
